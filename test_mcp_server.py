#!/usr/bin/env python3
"""Test script to start the MCP server manually for testing."""

from autodoc_mcp.main import main

if __name__ == "__main__":
    print("🚀 Starting AutoDocs MCP Server...")
    print("Press Ctrl+C to stop")
    print("This server can be connected to from Cursor or other MCP clients")
    print()

    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
