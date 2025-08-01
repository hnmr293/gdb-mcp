#!/usr/bin/env python3
"""Quick test script to run the GDB MCP server."""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gdb_mcp.server import main

if __name__ == "__main__":
    asyncio.run(main())