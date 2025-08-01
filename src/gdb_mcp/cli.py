#!/usr/bin/env python3
"""CLI entry point for the GDB MCP server."""

import asyncio
from .server import main as async_main


def main():
    """Synchronous wrapper for the async main function."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()