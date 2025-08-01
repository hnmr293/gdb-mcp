#!/usr/bin/env python3
"""GDB MCP Server - Provides GDB commands reference as resources."""

import asyncio
import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import (
    Resource,
    TextResourceContents,
    Tool,
)
from pydantic import AnyUrl

from .gdb_manager import GDBManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to the GDB commands reference file
COMMANDS_FILE = Path(__file__).parent.parent.parent / "resources" / "gdb_commands.md"


class GDBMCPServer:
    """MCP Server that provides GDB debugger resources and tools."""
    
    def __init__(self):
        self.server = Server("gdb-mcp")
        self.gdb_manager = GDBManager()
        self._setup_handlers()
        
    def _setup_handlers(self):
        """Set up the MCP server handlers."""
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List available resources."""
            return [
                Resource(
                    uri=AnyUrl("gdb://commands/reference"),
                    name="GDB Commands Reference",
                    description="Comprehensive reference for GDB CLI and MI commands",
                    mimeType="text/markdown",
                ),
                Resource(
                    uri=AnyUrl("gdb://commands/cli"),
                    name="GDB CLI Commands",
                    description="Command Line Interface commands with abbreviations",
                    mimeType="text/markdown",
                ),
                Resource(
                    uri=AnyUrl("gdb://commands/mi"),
                    name="GDB MI Commands",
                    description="Machine Interface commands for programmatic control",
                    mimeType="text/markdown",
                ),
                Resource(
                    uri=AnyUrl("gdb://commands/mapping"),
                    name="CLI to MI Command Mapping",
                    description="Correspondence between CLI and MI commands",
                    mimeType="text/markdown",
                ),
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: AnyUrl) -> str:
            """Read a specific resource."""
            
            # Load the commands file
            if not COMMANDS_FILE.exists():
                raise ValueError(f"Commands file not found: {COMMANDS_FILE}")
                
            content = COMMANDS_FILE.read_text(encoding="utf-8")
            
            # Convert URI to string for comparison
            uri_str = str(uri)
            
            # Parse the content based on the requested URI
            if uri_str == "gdb://commands/reference":
                # Return the full reference
                return content
            
            elif uri_str == "gdb://commands/cli":
                # Extract CLI commands section
                return self._extract_section(content, "## CLI Commands", "## MI Commands")
            
            elif uri_str == "gdb://commands/mi":
                # Extract MI commands section
                return self._extract_section(content, "## MI Commands", "## Command Correspondence")
            
            elif uri_str == "gdb://commands/mapping":
                # Extract command mapping section
                return self._extract_section(content, "## Command Correspondence", "## Notes")
            
            else:
                raise ValueError(f"Unknown resource URI: {uri_str}")
        
        # Tool handlers
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="open",
                    description="Start a new GDB debugging session",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "timeout": {
                                "type": "integer",
                                "description": "Session timeout in seconds",
                                "default": 300
                            }
                        }
                    }
                ),
                Tool(
                    name="call",
                    description="Send a command to a GDB session",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "Session ID"
                            },
                            "command": {
                                "type": "string",
                                "description": "GDB command to execute"
                            }
                        },
                        "required": ["id", "command"]
                    }
                ),
                Tool(
                    name="close",
                    description="Close a GDB session",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "Session ID to close"
                            }
                        },
                        "required": ["id"]
                    }
                ),
                Tool(
                    name="list_sessions",
                    description="List all active GDB sessions",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
            """Handle tool calls."""
            try:
                if name == "open":
                    timeout = arguments.get("timeout", 300)
                    session_id = await self.gdb_manager.create_session(timeout)
                    return [{
                        "type": "text",
                        "text": json.dumps({
                            "type": "ok",
                            "content": {"id": session_id}
                        })
                    }]
                
                elif name == "call":
                    session_id = arguments["id"]
                    command = arguments["command"]
                    result = await self.gdb_manager.send_command(session_id, command)
                    return [{
                        "type": "text",
                        "text": json.dumps({
                            "type": "ok",
                            "content": result
                        })
                    }]
                
                elif name == "close":
                    session_id = arguments["id"]
                    await self.gdb_manager.close_session(session_id)
                    return [{
                        "type": "text",
                        "text": json.dumps({
                            "type": "ok",
                            "content": {}
                        })
                    }]
                
                elif name == "list_sessions":
                    sessions = await self.gdb_manager.list_sessions()
                    return [{
                        "type": "text",
                        "text": json.dumps({
                            "type": "ok",
                            "content": {"sessions": sessions}
                        })
                    }]
                
                else:
                    return [{
                        "type": "text",
                        "text": json.dumps({
                            "type": "error",
                            "content": f"Unknown tool: {name}"
                        })
                    }]
                    
            except Exception as e:
                logger.error(f"Tool error: {e}")
                return [{
                    "type": "text",
                    "text": json.dumps({
                        "type": "error",
                        "content": str(e)
                    })
                }]
    
    def _extract_section(self, content: str, start_marker: str, end_marker: Optional[str] = None) -> str:
        """Extract a section from the markdown content."""
        lines = content.split('\n')
        start_idx = None
        end_idx = None
        
        for i, line in enumerate(lines):
            if line.strip() == start_marker:
                start_idx = i
            elif end_marker and line.strip() == end_marker and start_idx is not None:
                end_idx = i
                break
        
        if start_idx is None:
            return f"Section '{start_marker}' not found"
        
        if end_idx is None:
            # Return from start to end of file
            return '\n'.join(lines[start_idx:])
        else:
            return '\n'.join(lines[start_idx:end_idx])
    
    async def run(self):
        """Run the MCP server."""
        from mcp.server.stdio import stdio_server
        
        async with stdio_server() as (read_stream, write_stream):
            logger.info("GDB MCP Server starting...")
            
            # Run the server with initialization options
            init_options = InitializationOptions(
                server_name="gdb-mcp",
                server_version="0.1.0",
                capabilities=self.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
            
            # Start the GDB manager
            await self.gdb_manager.start()
            
            try:
                await self.server.run(
                    read_stream,
                    write_stream,
                    init_options
                )
            finally:
                # Clean up all GDB sessions on shutdown
                await self.gdb_manager.cleanup()


async def main():
    """Main entry point."""
    server = GDBMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())