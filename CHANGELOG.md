# Changelog

All notable changes to the AutoDocs MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-08-07

### Added
- **Core MCP Server Implementation**
  - FastMCP-based server with stdio transport for MCP protocol compliance
  - Four complete MCP tools: `scan_dependencies`, `get_package_docs`, `refresh_cache`, `get_cache_stats`
  - Structured logging with stderr output for proper MCP integration

- **Dependency Management System**
  - Complete pyproject.toml parsing with graceful degradation for malformed dependencies
  - Support for standard dependencies, optional dependencies, and complex version constraints
  - Robust error handling that continues processing even with parsing failures

- **Documentation Fetching & Caching**
  - PyPI JSON API integration for retrieving package documentation and metadata
  - Version resolution system that converts constraints to specific versions
  - Version-based caching system with `{package_name}-{version}` format
  - No time-based cache expiration (versions are immutable)
  - AI-optimized documentation formatting for better context

- **Project Architecture**
  - Modular SOLID design with clear separation of concerns:
    - `dependency_parser.py`: pyproject.toml parsing with error handling
    - `doc_fetcher.py`: PyPI API integration with concurrent requests
    - `cache_manager.py`: JSON-based version caching
    - `version_resolver.py`: Version constraint resolution
    - `main.py`: FastMCP server implementation
  - Comprehensive type hints with Pydantic models
  - Configuration management with environment variables

- **Development Infrastructure**
  - Complete test suite with pytest, asyncio, and mocking
  - Code quality tools: ruff (linting/formatting), mypy (type checking)
  - Pre-commit hooks configuration
  - Development scripts for testing individual components
  - uv-based dependency management and virtual environments

- **Documentation & Configuration**
  - Comprehensive README with installation and usage instructions
  - MCP integration examples for Claude Code and other AI clients
  - Project instructions in CLAUDE.md for AI assistant context
  - Environment variable configuration support
  - `.mcp.json` template for Claude Code integration

### Technical Features
- **Graceful Degradation**: Continues operation despite malformed dependencies or network failures
- **Concurrent Processing**: Optimized PyPI requests with httpx async client
- **Version Immutability**: Cache design assumes package versions never change
- **Transport Compliance**: Full stdio protocol implementation for MCP servers
- **Error Resilience**: Comprehensive exception handling at all levels

### Dependencies
- fastmcp >= 2.0.0 (MCP server framework)
- httpx >= 0.25.0 (async HTTP client)
- pydantic >= 2.0.0 (data validation)
- structlog >= 23.2.0 (structured logging)
- packaging >= 23.0 (version parsing)
- tomlkit >= 0.12.0 (TOML parsing)

### Development Dependencies
- pytest >= 7.4.0 with asyncio, mock, and coverage plugins
- ruff >= 0.1.0 (linting and formatting)
- mypy >= 1.6.0 (type checking)
- pre-commit >= 3.5.0 (git hooks)

### Notes
- This release represents a complete, production-ready MCP server
- Successfully tested with major packages: requests, pydantic, fastapi
- Ready for integration with AI coding assistants
- Cache directory defaults to `~/.cache/autodocs-mcp/`
- Supports Python 3.11+ as specified in pyproject.toml