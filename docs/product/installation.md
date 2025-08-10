# Installation Guide

This guide walks you through installing and setting up the AutoDocs MCP Server for different AI clients and development environments.

## Quick Start

=== "PyPI Installation (Recommended)"

    The fastest way to get started is installing from PyPI:

    ```bash
    # Using uv (recommended)
    uv tool install autodoc-mcp

    # Using pip
    pip install autodoc-mcp
    ```

=== "Development Installation"

    For development work or to access the latest features:

    ```bash
    # Clone the repository
    git clone https://github.com/bradleyfay/autodoc-mcp.git
    cd autodoc-mcp

    # Install with all development dependencies
    uv sync --all-extras

    # Verify installation
    uv run pytest
    ```

## MCP Client Configuration

Configure AutoDocs with your preferred AI client:

### Claude Code Sessions

For temporary sessions in Claude Code:

```bash
# 1. Install the server globally
uv tool install autodoc-mcp

# 2. Start the server (available globally)
autodoc-mcp

# 3. Server provides 8 MCP tools automatically
```

!!! tip "Session Persistence"
    In Claude Code sessions, you'll need to install and start the server each time. The global `autodoc-mcp` command is available after installation.

### Claude Desktop

Configure Claude Desktop by editing your `claude_desktop_config.json`:

=== "macOS"

    Location: `~/Library/Application Support/Claude/claude_desktop_config.json`

    ```json
    {
      "mcpServers": {
        "autodoc-mcp": {
          "command": "autodoc-mcp",
          "env": {
            "CACHE_DIR": "~/.cache/autodoc-mcp",
            "LOG_LEVEL": "INFO"
          }
        }
      }
    }
    ```

=== "Windows"

    Location: `%APPDATA%/Claude/claude_desktop_config.json`

    ```json
    {
      "mcpServers": {
        "autodoc-mcp": {
          "command": "autodoc-mcp",
          "env": {
            "CACHE_DIR": "%USERPROFILE%/.cache/autodoc-mcp",
            "LOG_LEVEL": "INFO"
          }
        }
      }
    }
    ```

=== "Linux"

    Location: `~/.config/Claude/claude_desktop_config.json`

    ```json
    {
      "mcpServers": {
        "autodoc-mcp": {
          "command": "autodoc-mcp",
          "env": {
            "CACHE_DIR": "~/.cache/autodoc-mcp",
            "LOG_LEVEL": "INFO"
          }
        }
      }
    }
    ```

### Cursor Desktop

Add AutoDocs to Cursor via Settings → Rules for AI → MCP Servers:

```json
{
  "mcpServers": {
    "autodoc-mcp": {
      "command": "autodoc-mcp",
      "env": {
        "CACHE_DIR": "~/.cache/autodoc-mcp",
        "LOG_LEVEL": "INFO",
        "MAX_DEPENDENCY_CONTEXT": "8"
      }
    }
  }
}
```

### Continue.dev

For Continue.dev integration, add to your `config.json`:

```json
{
  "mcpServers": [
    {
      "name": "autodoc-mcp",
      "command": "autodoc-mcp",
      "env": {
        "CACHE_DIR": "~/.cache/autodoc-mcp",
        "LOG_LEVEL": "INFO"
      }
    }
  ]
}
```

### Generic MCP Client Configuration

For other MCP clients that support the standard configuration format:

```json
{
  "mcpServers": {
    "autodoc-mcp": {
      "command": "python",
      "args": ["-m", "autodocs_mcp.main"],
      "cwd": "/path/to/autodoc-mcp",
      "env": {
        "CACHE_DIR": "~/.cache/autodoc-mcp",
        "LOG_LEVEL": "INFO",
        "MAX_CONCURRENT": "10",
        "MAX_DEPENDENCY_CONTEXT": "8"
      }
    }
  }
}
```

!!! note "Custom Installation Path"
    If you installed AutoDocs in a custom location or are running from source, adjust the `command` and `args` accordingly.

## Installation Verification

### Test Manual Startup

Verify the installation by starting the server manually:

```bash
# Should display the FastMCP startup screen
autodoc-mcp
```

Expected output:
```
[INFO] Starting AutoDocs MCP Server v0.4.2
[INFO] FastMCP server initialized with 8 tools
[INFO] Ready for MCP connections
```

### Test MCP Tools

Once configured with your AI client, test these commands:

1. **Test dependency scanning:**
   ```
   Ask your AI: "What packages are available in this project?"
   ```
   This should use the `scan_dependencies` tool.

2. **Test documentation context:**
   ```
   Ask your AI: "Tell me about the FastAPI package with its dependencies"
   ```
   This should use the `get_package_docs_with_context` tool.

3. **Test cache status:**
   ```
   Ask your AI: "What's the status of the AutoDocs cache?"
   ```
   This should use the `get_cache_stats` tool.

## Development Setup

### Prerequisites

- **Python 3.8+** (Python 3.11+ recommended)
- **uv** package manager (recommended) or pip
- **Git** for cloning the repository

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/bradleyfay/autodoc-mcp.git
cd autodoc-mcp

# Install development dependencies
uv sync --all-extras

# Install pre-commit hooks
uv run pre-commit install
```

### Run Tests

Verify everything works correctly:

```bash
# Run all 277 tests
uv run pytest

# Run with coverage report
uv run pytest --cov=src --cov-report=html

# Run linting
uv run ruff check

# Type checking
uv run mypy src
```

### Development Tools

The project includes helpful development scripts:

```bash
# Test dependency scanning
uv run python scripts/dev.py test-scan

# Test package documentation fetching
uv run python scripts/dev.py test-docs fastapi ">=0.100.0"

# View cache statistics
uv run python scripts/dev.py cache-stats

# Clear the cache
uv run python scripts/dev.py clear-cache

# Get help
uv run python scripts/dev.py --help
```

## Common Installation Issues

### Permission Errors

If you encounter permission errors during installation:

```bash
# Use user installation
pip install --user autodoc-mcp

# Or create a virtual environment
python -m venv autodoc-env
source autodoc-env/bin/activate  # On Windows: autodoc-env\Scripts\activate
pip install autodoc-mcp
```

### Command Not Found

If `autodoc-mcp` command is not found after installation:

1. **Check installation:**
   ```bash
   pip show autodoc-mcp
   ```

2. **Check PATH:**
   ```bash
   # Add to your shell profile (.bashrc, .zshrc, etc.)
   export PATH="$HOME/.local/bin:$PATH"
   ```

3. **Use full path:**
   ```bash
   python -m autodocs_mcp.main
   ```

### Network Configuration

For corporate networks or proxies:

```bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# Install with proxy
pip install --proxy http://proxy.company.com:8080 autodoc-mcp
```

### Cache Directory Issues

If you have issues with the default cache directory:

```bash
# Use custom cache location
export CACHE_DIR="/tmp/autodoc-cache"

# Or specify in MCP configuration
{
  "env": {
    "CACHE_DIR": "/path/to/custom/cache"
  }
}
```

## Next Steps

After installation, you can:

1. **Configure the server** - See [Configuration Guide](configuration.md)
2. **Learn about available tools** - See [MCP Tools Reference](mcp-tools.md)
3. **Troubleshoot issues** - See [Troubleshooting Guide](troubleshooting.md)
4. **Start using AutoDocs** - See [Getting Started Guide](getting-started.md)

!!! success "Installation Complete"
    You now have AutoDocs MCP Server installed and configured. The server will automatically provide intelligent documentation context to your AI assistant.
