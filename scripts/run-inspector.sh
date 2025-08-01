#!/bin/bash
# MCP Inspector runner for WSL without Windows integration

# Disable Windows detection
export WSL_DISTRO_NAME=""
export WSL_INTEROP=""

# Set browser to no-op
export BROWSER="echo Browser disabled:"

echo "Starting MCP Inspector..."
echo "Please manually open the URL shown below in your browser"
echo ""

# Run mcp-inspector
exec mcp-inspector "$@"