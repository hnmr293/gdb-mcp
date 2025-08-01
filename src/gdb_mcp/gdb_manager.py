#!/usr/bin/env python3
"""GDB process management for MCP server."""

import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


class GDBSession:
    """Represents a single GDB debugging session."""
    
    def __init__(self, session_id: str, timeout: int = 300):
        self.id = session_id
        self.timeout = timeout  # Session idle timeout in seconds
        self.created = datetime.now()
        self.last_activity = datetime.now()
        self.process: Optional[asyncio.subprocess.Process] = None
        self.reader_task: Optional[asyncio.Task] = None
        self.timeout_task: Optional[asyncio.Task] = None
        self.output_queue: asyncio.Queue = asyncio.Queue()
        self._lock = asyncio.Lock()
        
    async def start(self):
        """Start the GDB process in MI mode."""
        cmd = ["gdb", "--interpreter=mi2"]
            
        logger.info(f"Starting GDB session {self.id} with command: {' '.join(cmd)}")
        
        self.process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Start output reader task
        self.reader_task = asyncio.create_task(self._read_output())
        
        # Start timeout monitoring task
        self.timeout_task = asyncio.create_task(self._monitor_timeout())
        
        # Wait for GDB to initialize
        await asyncio.sleep(0.1)
        
    async def _read_output(self):
        """Read output from GDB process."""
        if not self.process or not self.process.stdout:
            return
            
        try:
            while True:
                line = await self.process.stdout.readline()
                if not line:
                    break
                    
                decoded = line.decode('utf-8', errors='replace').strip()
                if decoded:
                    await self.output_queue.put(decoded)
                    logger.debug(f"GDB output: {decoded}")
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error reading GDB output: {e}")
            
    async def _monitor_timeout(self):
        """Monitor session timeout and close if idle."""
        try:
            while True:
                await asyncio.sleep(10)  # Check every 10 seconds
                
                idle_time = (datetime.now() - self.last_activity).total_seconds()
                if idle_time > self.timeout:
                    logger.info(f"Session {self.id} timed out after {idle_time:.1f} seconds")
                    # Session will be cleaned up by the manager
                    break
                    
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error in timeout monitor: {e}")
    
    async def send_command(self, command: str) -> Dict[str, Any]:
        """Send a command to GDB and collect response."""
        if not self.process or self.process.returncode is not None:
            raise RuntimeError("GDB process is not running")
            
        # Update last activity time
        self.last_activity = datetime.now()
            
        async with self._lock:
            # Clear output queue
            while not self.output_queue.empty():
                try:
                    self.output_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
                    
            # Send command
            logger.info(f"Sending command to GDB: {command}")
            if self.process.stdin:
                self.process.stdin.write(f"{command}\n".encode())
                await self.process.stdin.drain()
            else:
                raise RuntimeError("GDB stdin is not available")
            
            # Collect output
            output_lines = []
            result = None
            
            try:
                # Wait for response with timeout
                timeout_task = asyncio.create_task(asyncio.sleep(5))
                
                while True:
                    get_task = asyncio.create_task(self.output_queue.get())
                    done, pending = await asyncio.wait(
                        {get_task, timeout_task},
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    
                    if timeout_task in done:
                        # Timeout
                        for task in pending:
                            task.cancel()
                        break
                        
                    line = await get_task
                    output_lines.append(line)
                    
                    # Check for result record
                    if line.startswith('^'):
                        result = self._parse_mi_result(line)
                        # Continue reading to get (gdb) prompt
                        
                    # Check for prompt
                    if line == '(gdb)':
                        for task in pending:
                            task.cancel()
                        break
                        
            except Exception as e:
                logger.error(f"Error reading GDB response: {e}")
                
            return {
                "result": result,
                "output": '\n'.join(output_lines)
            }
            
    def _parse_mi_result(self, line: str) -> Dict[str, Any]:
        """Parse MI result record."""
        if line.startswith('^done'):
            return {"status": "done", "data": line[5:].strip()}
        elif line.startswith('^running'):
            return {"status": "running"}
        elif line.startswith('^connected'):
            return {"status": "connected"}
        elif line.startswith('^error'):
            # Extract error message
            msg_start = line.find('msg="')
            if msg_start >= 0:
                msg_start += 5
                msg_end = line.find('"', msg_start)
                if msg_end >= 0:
                    return {"status": "error", "message": line[msg_start:msg_end]}
            return {"status": "error", "message": line[6:].strip()}
        elif line.startswith('^exit'):
            return {"status": "exit"}
        else:
            return {"status": "unknown", "data": line}
            
    async def close(self):
        """Close the GDB session."""
        # Cancel timeout monitoring
        if self.timeout_task:
            self.timeout_task.cancel()
            try:
                await self.timeout_task
            except asyncio.CancelledError:
                pass
                
        # Cancel output reader
        if self.reader_task:
            self.reader_task.cancel()
            try:
                await self.reader_task
            except asyncio.CancelledError:
                pass
                
        if self.process:
            if self.process.returncode is None:
                # Send quit command
                try:
                    if self.process.stdin:
                        self.process.stdin.write(b"quit\n")
                        await self.process.stdin.drain()
                    await asyncio.wait_for(self.process.wait(), timeout=2)
                except Exception:
                    # Force terminate if quit doesn't work
                    self.process.terminate()
                    await asyncio.wait_for(self.process.wait(), timeout=2)
                    
            self.process = None


class GDBManager:
    """Manages multiple GDB sessions."""
    
    def __init__(self):
        self.sessions: Dict[str, GDBSession] = {}
        self._lock = asyncio.Lock()
        self._cleanup_task: Optional[asyncio.Task] = None
        
    async def start(self):
        """Start the GDB manager."""
        self._cleanup_task = asyncio.create_task(self._cleanup_timed_out_sessions())
        
    async def _cleanup_timed_out_sessions(self):
        """Periodically check and clean up timed out sessions."""
        try:
            while True:
                await asyncio.sleep(30)  # Check every 30 seconds
                
                async with self._lock:
                    timed_out = []
                    for session_id, session in self.sessions.items():
                        idle_time = (datetime.now() - session.last_activity).total_seconds()
                        if idle_time > session.timeout:
                            timed_out.append(session_id)
                            
                # Close timed out sessions outside the lock
                for session_id in timed_out:
                    try:
                        logger.info(f"Cleaning up timed out session: {session_id}")
                        await self.close_session(session_id)
                    except Exception as e:
                        logger.error(f"Error cleaning up session {session_id}: {e}")
                        
        except asyncio.CancelledError:
            pass
        
    async def create_session(self, timeout: int = 300) -> str:
        """Create a new GDB session."""
        session_id = str(uuid.uuid4())
        
        async with self._lock:
            session = GDBSession(session_id, timeout)
            await session.start()
            self.sessions[session_id] = session
            
        logger.info(f"Created GDB session: {session_id}")
        return session_id
        
    async def send_command(self, session_id: str, command: str) -> Dict[str, Any]:
        """Send command to a specific session."""
        async with self._lock:
            session = self.sessions.get(session_id)
            if not session:
                raise ValueError(f"Session not found: {session_id}")
                
        return await session.send_command(command)
        
    async def close_session(self, session_id: str):
        """Close a specific session."""
        async with self._lock:
            session = self.sessions.pop(session_id, None)
            if not session:
                raise ValueError(f"Session not found: {session_id}")
                
        await session.close()
        logger.info(f"Closed GDB session: {session_id}")
        
    async def list_sessions(self) -> list:
        """List all active sessions."""
        async with self._lock:
            return [
                {
                    "id": session.id,
                    "created": session.created.isoformat()
                }
                for session in self.sessions.values()
            ]
            
    async def cleanup(self):
        """Clean up all sessions."""
        # Cancel cleanup task
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
                
        async with self._lock:
            session_ids = list(self.sessions.keys())
            
        for session_id in session_ids:
            try:
                await self.close_session(session_id)
            except Exception as e:
                logger.error(f"Error closing session {session_id}: {e}")