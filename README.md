# GDB-MCP

https://github.com/user-attachments/assets/84e717ba-6983-442d-bf11-7ba2b17108af

GDB-MCP is a Model Context Protocol (MCP) server that provides programmatic access to the GNU Debugger (GDB). It enables AI models and other MCP clients to interact with GDB through a standardized interface, making debugging capabilities accessible through natural language interactions.

Since it uses the gdb/mi interface, you can access the full functionality of gdb. We also provide a command reference for gdb in resources.

## Features

- **Session Management**: Create and manage multiple isolated GDB debugging sessions
- **Command Execution**: Execute both CLI and MI (Machine Interface) GDB commands
- **Comprehensive Documentation**: Access complete GDB command reference through MCP resources
- **Asynchronous Operation**: Built on asyncio for efficient concurrent session handling
- **Timeout Protection**: Automatic cleanup of idle sessions to prevent resource leaks

## Installation

### Prerequisites

- Python 3.12 or higher
- GDB installed on your system
- MCP-compatible client (e.g., Claude Desktop)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/gdb-mcp.git
cd gdb-mcp

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start

### Running the Server

```bash
# Start the MCP server
gdb-mcp

# Or run directly with Python
python -m gdb_mcp
```

### Claude Desktop Configuration

Add the following to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "gdb-mcp": {
      "command": "gdb-mcp"
    }
  }
}
```

See `examples/claude_code_config_example.json` for a complete configuration example.

## Usage

### Available Resources

The server provides comprehensive GDB documentation through MCP resources:

- `gdb://commands/reference` - Complete GDB command reference
- `gdb://commands/cli` - CLI commands with abbreviations
- `gdb://commands/mi` - Machine Interface commands
- `gdb://commands/mapping` - CLI to MI command correspondence

### Available Tools

#### `open` - Start a debugging session
```json
{
  "name": "open",
  "arguments": {
    "timeout": 300  // Optional, defaults to 300 seconds
  }
}
```

#### `call` - Execute a GDB command
```json
{
  "name": "call",
  "arguments": {
    "id": "session-uuid",
    "command": "break main"
  }
}
```

#### `close` - Close a debugging session
```json
{
  "name": "close",
  "arguments": {
    "id": "session-uuid"
  }
}
```

#### `list_sessions` - List all active sessions
```json
{
  "name": "list_sessions",
  "arguments": {}
}
```

## Example Usage

### Basic Debugging Session

```python
# Start a new debugging session
session = await client.call_tool("open", {})
session_id = session["content"]["id"]

# Load an executable
await client.call_tool("call", {
    "id": session_id,
    "command": "file /path/to/program"
})

# Set a breakpoint
await client.call_tool("call", {
    "id": session_id,
    "command": "break main"
})

# Run the program
result = await client.call_tool("call", {
    "id": session_id,
    "command": "run"
})

# Examine variables
result = await client.call_tool("call", {
    "id": session_id,
    "command": "print variable_name"
})

# Close the session
await client.call_tool("close", {"id": session_id})
```

### Accessing Documentation

```python
# Get CLI commands reference
cli_docs = await client.read_resource("gdb://commands/cli")

# Get MI commands reference
mi_docs = await client.read_resource("gdb://commands/mi")
```

## Architecture

GDB-MCP consists of several key components:

1. **MCP Server** (`server.py`) - Handles client connections and request routing
2. **GDB Manager** (`gdb_manager.py`) - Manages GDB subprocess lifecycle
3. **Session Management** - Maintains isolated debugging sessions with automatic timeout
4. **Resource Provider** - Serves comprehensive GDB documentation

The server operates GDB in MI (Machine Interface) mode internally for reliable command parsing and structured output.

## Development

### Project Structure

```
gdb-mcp/
    src/gdb_mcp/
        __init__.py
        __main__.py
        cli.py              # CLI entry point
        server.py           # MCP server implementation
        gdb_manager.py      # GDB process management
    resources/
        gdb_commands.md     # GDB command reference
    docs/                   # Additional documentation
    examples/               # Usage examples
    tests/                  # Test suite
    scripts/                # Utility scripts
```

## Security Considerations

- Designed for local debugging only
- Each GDB session runs in an isolated process
- Automatic session timeout prevents resource leaks
- File system access limited to user permissions

## Acknowledgments

- Built on the [Model Context Protocol](https://modelcontextprotocol.io/)
- Powered by [GNU Debugger (GDB)](https://www.gnu.org/software/gdb/)
