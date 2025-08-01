# GDB-MCP Specification

## Overview

GDB-MCP is an MCP (Model Context Protocol) server that provides programmatic access to GDB (GNU Debugger) functionality. It enables AI models and other MCP clients to interact with GDB through a standardized interface.

The server operates GDB in MI (Machine Interface) mode internally and exposes both resources and tools for debugging operations.

## Architecture

### Components

1. **MCP Server**: Handles client connections and request routing
2. **GDB Process Manager**: Manages GDB subprocess lifecycle in MI mode
3. **Resource Provider**: Serves GDB command documentation
4. **Tool Handler**: Processes debugging commands

### Design Principles

- **Local-first**: Designed primarily for local debugging scenarios
- **Stateful Sessions**: Maintains GDB session state across tool calls
- **MI Mode**: Uses GDB's machine interface for reliable parsing
- **Resource-based Documentation**: Provides comprehensive command reference

## Resources

The server exposes the following resources:

| URI | Name | Description |
|-----|------|-------------|
| `gdb://commands/reference` | GDB Commands Reference | Complete reference for all GDB commands |
| `gdb://commands/cli` | GDB CLI Commands | CLI commands with abbreviations and usage |
| `gdb://commands/mi` | GDB MI Commands | Machine Interface commands reference |
| `gdb://commands/mapping` | CLI to MI Mapping | Correspondence between CLI and MI commands |

### Resource Format

All resources are served as Markdown documents with:
- Command syntax and parameters
- Usage examples
- Output format descriptions
- Cross-references between CLI and MI modes

## Tools

The server provides tools for GDB interaction:

### Response Format

All tool responses follow this JSON structure:

```json
{
    "type": "ok",
    "content": any
}
```

or

```json
{
    "type": "error",
    "content": string
}
```

### Available Tools

| Name | Description | Inputs | Outputs |
|------|-------------|--------|---------|
| `open` | Start a GDB session | `{ "timeout": int = 300 }` | `{ "id": UUID }` |
| `call` | Send command to GDB | `{ "id": UUID, "command": string }` | `{ "result": any, "output": string }` |
| `close` | Close GDB session | `{ "id": UUID }` | `{}` |
| `list_sessions` | List active sessions | `{}` | `{ "sessions": [{ "id": UUID, "created": timestamp }] }` |

### Tool Details

#### `open`
- Starts a new GDB debugging session
- Returns a unique session ID for subsequent commands
- Default timeout of 300 seconds

#### `call`
- Executes GDB commands in a specific session
- Supports both CLI and MI command formats
- Returns:
  - `result`: Structured MI response (parsed result record)
  - `output`: Raw console output (all output lines from GDB)
- Commands are executed synchronously

#### `close`
- Terminates a GDB session cleanly
- Releases associated resources
- Invalidates the session ID

#### `list_sessions`
- Returns all active debugging sessions
- Includes session creation timestamps
- Useful for session management

## Session Management

### Session Lifecycle

1. **Creation**: `open` tool creates a new session
2. **Usage**: `call` tool sends commands to session
3. **Termination**: `close` tool or timeout ends session

### Session State

Each session maintains:
- GDB subprocess instance
- Current execution state
- Loaded program information
- Breakpoint and watchpoint data
- Variable and expression watches

### Concurrency

- Multiple sessions can run simultaneously
- Each session is isolated
- Commands within a session are serialized
- No cross-session interference

## Error Handling

### Error Types

1. **Session Errors**
   - Invalid session ID
   - Session timeout
   - Session already closed

2. **GDB Errors**
   - Command syntax errors
   - Runtime errors
   - Target program errors

3. **System Errors**
   - GDB process failure
   - Resource limitations
   - Permission issues

### Error Responses

Errors are returned with descriptive messages:
```json
{
    "type": "error",
    "content": "Session not found: 123e4567-e89b-12d3-a456-426614174000"
}
```

## Security Considerations

### Local Execution

- Designed for local debugging only
- No network debugging support by default
- File system access limited to user permissions

### Process Isolation

- Each GDB instance runs in separate process
- No shared memory between sessions
- Clean process termination on errors

### Resource Limits

- Session timeout prevents resource leaks
- Maximum concurrent sessions configurable
- Memory usage monitoring recommended

## Implementation Notes

### GDB MI Mode

The server uses GDB's MI mode for:
- Structured command output
- Reliable parsing
- Asynchronous notifications
- Better error reporting

### Python Implementation

Key dependencies:
- `mcp`: MCP protocol implementation
- `asyncio`: Asynchronous I/O
- `subprocess`: GDB process management
- `pydantic`: Data validation

### Extensibility

The architecture supports:
- Additional tool implementations
- Custom resource providers
- Plugin-based extensions
- Alternative debugger backends

## Usage Examples

### Basic Debugging Session

```python
# Start session
open_result = await tool_call("open", {})
session_id = open_result["content"]["id"]

# Load executable
await tool_call("call", {
    "id": session_id,
    "command": "file /path/to/executable"
})

# Set breakpoint
await tool_call("call", {
    "id": session_id,
    "command": "break main"
})

# Run program
await tool_call("call", {
    "id": session_id,
    "command": "run"
})

# Examine variables
await tool_call("call", {
    "id": session_id,
    "command": "print variable_name"
})

# Close session
await tool_call("close", {"id": session_id})
```

### Resource Access

```python
# Get CLI commands reference
cli_reference = await read_resource("gdb://commands/cli")

# Get MI commands reference
mi_reference = await read_resource("gdb://commands/mi")
```

## Future Enhancements

### Planned Features

1. **Remote Debugging Support**
   - GDB server mode integration
   - SSH tunnel support
   - Security authentication

2. **Enhanced Tools**
   - Batch command execution
   - Conditional breakpoints UI
   - Memory dump analysis

3. **Additional Resources**
   - Architecture-specific commands
   - Extension command documentation
   - Best practices guide

### Potential Integrations

- IDE protocol adapters
- DAP (Debug Adapter Protocol) bridge
- Custom visualization tools
- Automated debugging assistants

## References

- [GDB Documentation](https://sourceware.org/gdb/current/onlinedocs/gdb.html)
- [GDB/MI Interface](https://sourceware.org/gdb/current/onlinedocs/gdb.html/GDB_002fMI.html)
- [Model Context Protocol](https://github.com/modelcontextprotocol/specification)

## Version History

### 0.1.0 (Current)
- Initial implementation
- Basic session management
- Command execution tools
- Documentation resources

### Roadmap
- 0.2.0: Enhanced error handling and session persistence
- 0.3.0: Remote debugging support
- 0.4.0: Advanced debugging tools
- 1.0.0: Production-ready release