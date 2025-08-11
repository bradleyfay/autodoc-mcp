# AutoDocs MCP Server

[![PyPI](https://img.shields.io/pypi/v/autodoc-mcp)](https://pypi.org/project/autodoc-mcp/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Intelligent documentation context provider for AI assistants**

AutoDocs MCP Server automatically provides AI assistants with contextual, version-specific documentation for Python project dependencies. It uses intelligent dependency resolution to include both the requested package and its most relevant dependencies, giving AI assistants comprehensive context for accurate code assistance.

<a href="https://glama.ai/mcp/servers/@bradleyfay/autodoc-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@bradleyfay/autodoc-mcp/badge" alt="AutoDocs Server MCP server" />
</a>

## Key Features

- **Smart dependency context** - Automatically includes 3-8 most relevant dependencies
- **AI-optimized documentation** - Token-aware formatting with performance metrics
- **Production-ready** - 8 MCP tools with health monitoring and caching
- **Framework-aware** - Special handling for FastAPI, Django, Flask ecosystems
- **High performance** - Concurrent fetching with circuit breakers and connection pooling

## Quick Start

### Installation
```bash
# Using uv (recommended)
uv tool install autodoc-mcp

# Using pip
pip install autodoc-mcp
```

### Basic Usage
```bash
# Start the MCP server
autodoc-mcp

# Test with your AI assistant
# Ask: "What packages are available in this project?"
# Ask: "Tell me about FastAPI with its dependencies"
```

### MCP Client Configuration
Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "autodoc-mcp": {
      "command": "autodoc-mcp",
      "env": {
        "CACHE_DIR": "~/.cache/autodoc-mcp"
      }
    }
  }
}
```

## Documentation

**📚 Complete Documentation**: https://bradleyfay.github.io/autodoc-mcp/

Our documentation is organized into three focused paths:

- **[Product Documentation](https://bradleyfay.github.io/autodoc-mcp/product/)** - Installation, configuration, API reference, and troubleshooting
- **[Development Process](https://bradleyfay.github.io/autodoc-mcp/development/)** - Architecture, contributing guidelines, and development standards
- **[Development Journey](https://bradleyfay.github.io/autodoc-mcp/journey/)** - Project evolution and AI-assisted development insights

### Quick Links
- **[Installation Guide](https://bradleyfay.github.io/autodoc-mcp/product/installation/)** - Setup for different platforms and MCP clients
- **[MCP Tools Reference](https://bradleyfay.github.io/autodoc-mcp/product/mcp-tools/)** - Complete API documentation for all 8 tools
- **[Configuration Options](https://bradleyfay.github.io/autodoc-mcp/product/configuration/)** - Environment variables and advanced settings
- **[Troubleshooting Guide](https://bradleyfay.github.io/autodoc-mcp/product/troubleshooting/)** - Common issues and solutions
- **[Contributing Guide](https://bradleyfay.github.io/autodoc-mcp/development/contributing/)** - How to contribute to the project

## MCP Tools Overview

AutoDocs provides **8 production-ready MCP tools**:

### Core Tools
- **`get_package_docs_with_context`** - Primary tool for comprehensive documentation with dependencies
- **`scan_dependencies`** - Parse project dependencies from pyproject.toml
- **`get_package_docs`** - Legacy single-package documentation tool

### Cache Management
- **`refresh_cache`** - Clear documentation cache
- **`get_cache_stats`** - View cache statistics

### System Health
- **`health_check`** - Comprehensive system health status
- **`ready_check`** - Kubernetes-style readiness check
- **`get_metrics`** - Performance metrics and monitoring data

## Development & Contributing

This project welcomes contributions! Please see our [Contributing Guide](https://bradleyfay.github.io/autodoc-mcp/development/contributing/) for detailed information.

### Quick Development Setup
```bash
git clone https://github.com/bradleyfay/autodoc-mcp.git
cd autodoc-mcp
uv sync --all-extras
uv run pytest  # Run 400+ tests
```

### Development Standards
- **Conventional Commits** - All commits must follow conventional commit format
- **Pre-commit Hooks** - Automated linting, formatting, and type checking
- **Comprehensive Testing** - pytest ecosystem with 400+ tests
- **GitFlow Workflow** - Feature branches, release branches, and semantic versioning

## Project Information

- **Version**: 0.5.1 (Production Ready)
- **Python**: 3.11+ required
- **License**: MIT
- **Architecture**: Layered design with 10 specialized core service modules
- **Dependencies**: Minimal production footprint with FastMCP, httpx, Pydantic

## Transparency & Learning

This project demonstrates transparent AI-assisted development. Explore these directories to see the complete development process:

- **`.claude/agents/`** - Claude Code agent configurations
- **`.specstory/history/`** - Complete session history
- **`planning/`** - Planning documents and technical decisions

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built with [FastMCP](https://github.com/jlowin/fastmcp) | [Documentation Site](https://bradleyfay.github.io/autodoc-mcp/) | [GitHub](https://github.com/bradleyfay/autodoc-mcp)**
