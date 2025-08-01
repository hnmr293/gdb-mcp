#!/bin/bash
# Test script for MCP Inspector with custom port

PORT=${1:-6278}
echo "Starting MCP Inspector on port $PORT..."
mcp-inspector --port $PORT uv run examples/run_server.py