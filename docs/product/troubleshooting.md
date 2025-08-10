# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the AutoDocs MCP Server. Each section includes symptoms, diagnosis steps, and solutions.

## Quick Diagnostic Commands

Before diving into specific issues, run these commands to gather diagnostic information:

```bash
# Check if AutoDocs is installed
autodoc-mcp --version

# Test manual startup
autodoc-mcp

# Check environment configuration
env | grep -E "(CACHE_DIR|LOG_LEVEL|MAX_)"

# Test network connectivity to PyPI
curl -s https://pypi.org/pypi/requests/json | head -n 10
```

## Installation Issues

### "Command not found: autodoc-mcp"

**Symptoms:**
- `autodoc-mcp: command not found` error
- MCP client cannot start the server

**Diagnosis:**
```bash
# Check if package is installed
pip show autodoc-mcp
pip list | grep autodoc

# Check PATH
echo $PATH
which python
which pip
```

**Solutions:**

=== "Using uv (Recommended)"

    ```bash
    # Install with uv tool
    uv tool install autodoc-mcp

    # Verify installation
    autodoc-mcp --version
    ```

=== "Using pip"

    ```bash
    # Install globally
    pip install autodoc-mcp

    # Or install for user only
    pip install --user autodoc-mcp

    # Add to PATH if needed
    export PATH="$HOME/.local/bin:$PATH"
    ```

=== "Fix PATH Issues"

    ```bash
    # Add to shell profile (.bashrc, .zshrc, etc.)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

### "Permission denied" during installation

**Symptoms:**
- Permission errors during `pip install`
- Cannot write to system directories

**Solutions:**

```bash
# Use user installation
pip install --user autodoc-mcp

# Or use virtual environment
python -m venv autodoc-env
source autodoc-env/bin/activate  # Windows: autodoc-env\Scripts\activate
pip install autodoc-mcp
```

### "Package not found" from PyPI

**Symptoms:**
- `No matching distribution found` error
- Package cannot be downloaded

**Solutions:**

```bash
# Update pip
pip install --upgrade pip

# Clear pip cache
pip cache purge

# Use specific index URL
pip install -i https://pypi.org/simple/ autodoc-mcp

# For corporate networks, configure proxy
pip install --proxy http://proxy.company.com:8080 autodoc-mcp
```

## MCP Client Connection Issues

### MCP client cannot connect to server

**Symptoms:**
- "Failed to connect to MCP server" in AI client
- Server not responding to MCP protocol

**Diagnosis:**
```bash
# Test server startup manually
autodoc-mcp

# Expected output should show:
# [INFO] Starting AutoDocs MCP Server v0.x.x
# [INFO] FastMCP server initialized with 8 tools
# [INFO] Ready for MCP connections
```

**Solutions:**

=== "Fix Command Path"

    Update MCP client configuration:
    ```json
    {
      "mcpServers": {
        "autodoc-mcp": {
          "command": "autodoc-mcp",  // Use full path if needed: "/usr/local/bin/autodoc-mcp"
          "env": {
            "LOG_LEVEL": "DEBUG"
          }
        }
      }
    }
    ```

=== "Enable Debug Logging"

    ```json
    {
      "mcpServers": {
        "autodoc-mcp": {
          "command": "autodoc-mcp",
          "env": {
            "LOG_LEVEL": "DEBUG"
          }
        }
      }
    }
    ```

=== "Use Python Module"

    ```json
    {
      "mcpServers": {
        "autodoc-mcp": {
          "command": "python",
          "args": ["-m", "autodocs_mcp.main"],
          "env": {
            "LOG_LEVEL": "DEBUG"
          }
        }
      }
    }
    ```

### "Tools not available" in AI client

**Symptoms:**
- AI assistant says tools are not available
- No AutoDocs tools visible in MCP client

**Diagnosis:**
```bash
# Check server logs for initialization errors
export LOG_LEVEL=DEBUG
autodoc-mcp

# Look for errors during tool registration
```

**Solutions:**

1. **Restart MCP client** after configuration changes
2. **Verify JSON syntax** in MCP client configuration
3. **Check server startup** for error messages
4. **Test tool availability** by asking AI assistant: "What MCP tools are available?"

## Network and PyPI Issues

### "Failed to connect to PyPI" errors

**Symptoms:**
- Network timeouts when fetching package documentation
- "Unable to reach PyPI" error messages

**Diagnosis:**
```bash
# Test PyPI connectivity
curl -I https://pypi.org/pypi/requests/json

# Check DNS resolution
nslookup pypi.org

# Test with verbose output
export LOG_LEVEL=DEBUG
# Then use AutoDocs and check logs
```

**Solutions:**

=== "Corporate Firewall/Proxy"

    ```bash
    # Set proxy environment variables
    export HTTP_PROXY=http://proxy.company.com:8080
    export HTTPS_PROXY=http://proxy.company.com:8080
    export NO_PROXY=localhost,127.0.0.1,.local

    # Configure in MCP client
    {
      "env": {
        "HTTP_PROXY": "http://proxy.company.com:8080",
        "HTTPS_PROXY": "http://proxy.company.com:8080"
      }
    }
    ```

=== "Network Timeouts"

    ```bash
    # Increase timeout and reduce concurrency
    export REQUEST_TIMEOUT=30
    export MAX_CONCURRENT=3
    export RETRY_ATTEMPTS=5
    ```

=== "Alternative PyPI Index"

    ```bash
    # Use mirror or alternative index
    export PYPI_BASE_URL=https://pypi.python.org/pypi
    ```

### Slow response times

**Symptoms:**
- Long delays before getting documentation
- "Request timed out" errors

**Diagnosis:**
```bash
# Check cache status
# Ask AI assistant: "What's the status of the AutoDocs cache?"

# Monitor network performance
ping pypi.org
curl -w "@curl-format.txt" -s https://pypi.org/pypi/requests/json
```

**Solutions:**

1. **First-time cache miss**: Initial requests are slower as documentation is fetched and cached
2. **Reduce concurrency**: Lower `MAX_CONCURRENT` for unstable networks
3. **Increase timeout**: Set `REQUEST_TIMEOUT=30` for slow networks
4. **Pre-populate cache**: Use development scripts to cache common packages

## Cache Issues

### "Context fetcher not initialized" error

**Symptoms:**
- Error when using `get_package_docs_with_context`
- Service fails to start properly

**Diagnosis:**
```bash
# Check cache directory permissions
ls -la ~/.cache/autodoc-mcp/

# Test cache write access
touch ~/.cache/autodoc-mcp/test-file
rm ~/.cache/autodoc-mcp/test-file
```

**Solutions:**

=== "Fix Cache Directory"

    ```bash
    # Create cache directory
    mkdir -p ~/.cache/autodoc-mcp
    chmod 755 ~/.cache/autodoc-mcp

    # Or use alternative location
    export CACHE_DIR="/tmp/autodoc-cache"
    ```

=== "Clear Corrupted Cache"

    ```bash
    # Clear cache completely
    rm -rf ~/.cache/autodoc-mcp/*

    # Or use MCP tool
    # Ask AI assistant: "Clear the AutoDocs cache"
    ```

### "Cache write error" messages

**Symptoms:**
- Cannot save documentation to cache
- Repeated network requests for same packages

**Diagnosis:**
```bash
# Check disk space
df -h ~/.cache/
du -sh ~/.cache/autodoc-mcp/

# Check permissions
ls -la ~/.cache/autodoc-mcp/
```

**Solutions:**

1. **Free disk space**: Remove old files or increase available storage
2. **Fix permissions**: `chmod -R 755 ~/.cache/autodoc-mcp/`
3. **Change cache location**: Set `CACHE_DIR` to writable location
4. **Clear cache**: Remove corrupted cache files

### Cache corruption issues

**Symptoms:**
- Inconsistent or incomplete documentation responses
- JSON parsing errors in cached files

**Diagnosis:**
```bash
# Check for corrupted cache files
find ~/.cache/autodoc-mcp/ -name "*.json" -exec python -m json.tool {} \; > /dev/null

# View cache statistics
# Ask AI assistant: "Show me cache performance statistics"
```

**Solutions:**

```bash
# Clear specific package cache
rm ~/.cache/autodoc-mcp/fastapi-*.json

# Clear entire cache
# Ask AI assistant: "Clear the AutoDocs cache"

# Prevent corruption with proper shutdown
# Always stop server gracefully (Ctrl+C, not kill -9)
```

## Package-Specific Issues

### "No dependencies found" for known packages

**Symptoms:**
- Packages with dependencies show empty dependency lists
- Missing expected framework dependencies

**Diagnosis:**
```bash
# Check package metadata manually
curl -s https://pypi.org/pypi/fastapi/json | jq '.info.requires_dist'

# Test with different context scopes
# Ask AI: "Get FastAPI docs with context_scope='runtime'"
```

**Solutions:**

1. **Try different context scope**: Use `"runtime"` or `"smart"` scope
2. **Some packages have optional-only dependencies**: This is normal behavior
3. **Check package version**: Some versions have different dependencies
4. **Verify package exists**: Ensure package name is spelled correctly

### "Package not found" for valid packages

**Symptoms:**
- PyPI returns 404 for valid package names
- Inconsistent package availability

**Diagnosis:**
```bash
# Verify package exists on PyPI
curl -I https://pypi.org/pypi/PACKAGE_NAME/json

# Check for case sensitivity
curl -I https://pypi.org/pypi/package_name/json
```

**Solutions:**

1. **Check spelling**: Package names are case-sensitive
2. **Use canonical name**: Some packages have different canonical names
3. **Try alternative names**: Some packages have aliases or have been renamed
4. **Check package status**: Package may be yanked or delisted

## Performance Issues

### High memory usage

**Symptoms:**
- AutoDocs consuming excessive memory
- System running out of memory

**Diagnosis:**
```bash
# Monitor memory usage
ps aux | grep autodoc
top -p $(pgrep -f autodoc)

# Check cache size
du -sh ~/.cache/autodoc-mcp/
```

**Solutions:**

=== "Reduce Memory Usage"

    ```bash
    # Limit context size
    export MAX_DEPENDENCY_CONTEXT=3
    export MAX_CONTEXT_TOKENS=15000

    # Reduce cache size
    export MAX_CACHE_SIZE_MB=200
    ```

=== "Clean Up Cache"

    ```bash
    # Clear cache periodically
    # Ask AI assistant: "Clear the AutoDocs cache"

    # Implement automatic cleanup
    export CACHE_CLEANUP_INTERVAL=1800
    ```

### Excessive network requests

**Symptoms:**
- High network usage
- Rate limiting errors from PyPI

**Diagnosis:**
```bash
# Monitor network requests
export LOG_LEVEL=DEBUG
# Check logs for request patterns

# Check cache hit rate
# Ask AI assistant: "Show me cache performance statistics"
```

**Solutions:**

```bash
# Reduce concurrent requests
export MAX_CONCURRENT=3

# Increase cache retention
export MAX_CACHE_SIZE_MB=1000

# Use longer timeouts with fewer retries
export REQUEST_TIMEOUT=20
export RETRY_ATTEMPTS=2
```

## Development and Testing Issues

### Tests failing in development

**Symptoms:**
- pytest failures during development
- Import errors in tests

**Diagnosis:**
```bash
# Run tests with verbose output
uv run pytest -v

# Check test environment
uv run python -c "import autodocs_mcp; print(autodocs_mcp.__version__)"

# Run specific test
uv run pytest tests/test_specific.py::test_function -v
```

**Solutions:**

```bash
# Install development dependencies
uv sync --all-extras

# Run pre-commit hooks
uv run pre-commit run --all-files

# Clear Python cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Reinstall in development mode
uv sync --reinstall
```

### Pre-commit hooks failing

**Symptoms:**
- Git commits being rejected
- Linting or formatting errors

**Solutions:**

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run all hooks manually
uv run pre-commit run --all-files

# Fix specific issues
uv run ruff check --fix
uv run ruff format
uv run mypy src
```

## Advanced Troubleshooting

### Enable comprehensive debugging

```bash
# Maximum debug information
export LOG_LEVEL=DEBUG
export REQUEST_TIMEOUT=60
export RETRY_ATTEMPTS=1

# Start server manually
autodoc-mcp

# Monitor all activity
tail -f ~/.cache/autodoc-mcp/debug.log  # if logging to file
```

### Collect diagnostic information

```bash
# System information
uname -a
python --version
pip --version

# Package information
pip show autodoc-mcp
pip list | grep -E "(fastmcp|pydantic|httpx)"

# Environment
env | grep -E "(CACHE|LOG|MAX|PYPI)"

# Network test
curl -w "@curl-format.txt" -s https://pypi.org/pypi/requests/json > /dev/null
```

### Performance profiling

```python
# Use development scripts for profiling
uv run python scripts/dev.py test-docs fastapi --profile

# Monitor resource usage
htop
iotop
netstat -an | grep :80
```

## Getting Help

### Log Analysis

When reporting issues, include relevant log entries:

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Reproduce the issue
# Then share the relevant log output
```

### Health Check Information

```bash
# Get comprehensive health status
# Ask AI assistant: "Check the health status of AutoDocs"

# Get performance metrics
# Ask AI assistant: "Show me AutoDocs performance metrics"

# Get cache statistics
# Ask AI assistant: "What's the status of the AutoDocs cache?"
```

### Issue Report Template

When reporting issues, include:

1. **AutoDocs version**: `autodoc-mcp --version`
2. **Python version**: `python --version`
3. **Operating system**: `uname -a` (Unix) or system info (Windows)
4. **MCP client**: Claude Desktop, Cursor, etc.
5. **Configuration**: Relevant environment variables
6. **Error messages**: Complete error messages and stack traces
7. **Reproduction steps**: Minimal steps to reproduce the issue
8. **Logs**: Relevant log entries with `LOG_LEVEL=DEBUG`

## Prevention Best Practices

### Regular Maintenance

```bash
# Monthly cache cleanup
# Ask AI assistant: "Clear the AutoDocs cache"

# Check system health
# Ask AI assistant: "Check the health status of AutoDocs"

# Update to latest version
pip install --upgrade autodoc-mcp
```

### Monitoring

```bash
# Set up basic monitoring
# Check cache size: du -sh ~/.cache/autodoc-mcp/
# Check memory usage: ps aux | grep autodoc
# Test connectivity: curl -I https://pypi.org/
```

### Backup and Recovery

```bash
# Backup cache (optional - will regenerate automatically)
tar -czf autodoc-cache-backup.tar.gz ~/.cache/autodoc-mcp/

# Quick recovery
rm -rf ~/.cache/autodoc-mcp/
# Cache will regenerate on next use
```

---

If issues persist after trying these solutions, consider:

1. **Updating** to the latest version: `pip install --upgrade autodoc-mcp`
2. **Checking** the [GitHub Issues](https://github.com/bradleyfay/autodoc-mcp/issues) page
3. **Filing** a new issue with diagnostic information
4. **Consulting** the [Configuration Reference](configuration.md) for advanced settings
