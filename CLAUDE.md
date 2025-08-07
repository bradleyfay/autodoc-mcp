# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **AutoDocs MCP Server** project - a **fully implemented** Model Context Protocol (MCP) server that automatically provides AI assistants with contextual, version-specific documentation for Python project dependencies. The goal is to eliminate manual package documentation lookup and provide more accurate AI coding assistance.

## Architecture

The project follows a modular SOLID architecture with these implemented core components:

- **dependency_parser.py**: Handles pyproject.toml parsing with graceful degradation for malformed dependencies
- **doc_fetcher.py**: PyPI JSON API integration with concurrent request handling and AI-optimized formatting
- **cache_manager.py**: Version-based JSON file caching system (no time expiration)
- **version_resolver.py**: Converts version constraints to specific versions using PyPI API
- **main.py**: FastMCP server with four MCP tools and structured logging

## MCP Tools Available

The server exposes four MCP tools:

1. **scan_dependencies**: Parse pyproject.toml and extract dependencies with graceful error handling
2. **get_package_docs**: Retrieve version-specific cached or fresh documentation from PyPI API  
3. **refresh_cache**: Clear the entire documentation cache
4. **get_cache_stats**: View cache statistics and cached packages

## Key Technical Decisions

- **Version-Based Caching**: Cache key format `{package_name}-{version}` with no time expiration
- **PyPI Integration**: Uses `https://pypi.org/pypi/{package_name}/json` endpoint for both version resolution and documentation
- **Graceful Degradation**: Continues processing even with malformed dependencies or network failures
- **Transport**: stdio for MCP protocol compliance with stderr-only logging
- **Framework**: FastMCP for MCP server implementation
- **Dependencies**: httpx, pydantic, structlog, packaging, fastmcp

## Implementation Status: COMPLETE ✅

**Priority 1 (Core Validation)**: ✅ Complete
- Dependency parsing with graceful degradation
- MCP protocol integration
- Comprehensive test coverage

**Priority 2 (Documentation Fetching)**: ✅ Complete  
- PyPI API integration with version resolution
- Version-based caching system
- AI-optimized documentation formatting
- Successfully tested with requests, pydantic, fastapi

## Installation & Usage

### Install the MCP Server
```bash
# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

### Development & Testing
```bash
# Test dependency scanning
uv run python scripts/dev.py test-scan

# Test documentation fetching
uv run python scripts/dev.py test-docs requests ">=2.28.0"

# Check cache stats  
uv run python scripts/dev.py cache-stats

# Clear cache
uv run python scripts/dev.py clear-cache
```

### Run as MCP Server
```bash
# Start the MCP server (stdio protocol)
uv run python -m autodocs_mcp.main
```

## MCP Integration

### For Claude Code Sessions
To install this MCP server in Claude Code sessions:

```bash
# 1. Install the server in current session
uv sync

# 2. Start the MCP server (in background)
uv run python -m autodocs_mcp.main &

# 3. The server will be available with these tools:
#    - scan_dependencies: Parse project dependencies 
#    - get_package_docs: Fetch package documentation
#    - refresh_cache: Clear documentation cache
#    - get_cache_stats: View cache statistics
```

### For Other AI Clients (Cursor, etc.)
MCP server configuration:
```json
{
  "mcpServers": {
    "autodocs-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "autodocs_mcp.main"],
      "cwd": "/Users/bradleyfay/autodocs",
      "env": {
        "CACHE_DIR": "~/.cache/autodocs-mcp"
      }
    }
  }
}
```

## Cache Configuration

- **Default Location**: `~/.cache/autodocs-mcp/`
- **Format**: JSON files named `{package}-{version}.json`  
- **Expiration**: No time-based expiration (versions are immutable)
- **Performance**: Instant cache hits for previously fetched versions

## Future Development

Ready for **Priority 3** (Graceful Degradation) and **Priority 4** (Dependency Context) based on `planning/implementation_priorities.md`. Current implementation already includes significant graceful degradation features.