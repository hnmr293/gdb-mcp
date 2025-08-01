#!/bin/bash
# MCP Inspector launcher for WSL environments

echo "Starting MCP Inspector without browser auto-launch..."
echo "Please open http://localhost:5173 in your browser manually"
echo ""

# Disable browser launch
export BROWSER=echo

# Run MCP Inspector
mcp-inspector "$@"