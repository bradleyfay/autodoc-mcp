# Configuration Reference

This reference documents all configuration options, environment variables, and settings for the AutoDocs MCP Server.

## Environment Variables

### Core Configuration

#### `CACHE_DIR`

**Default:** `~/.cache/autodoc-mcp`
**Type:** String (file path)
**Description:** Directory for storing cached documentation files.

```bash
# Use custom cache location
export CACHE_DIR="/tmp/autodoc-cache"

# Platform-specific defaults
# macOS/Linux: ~/.cache/autodoc-mcp
# Windows: %LOCALAPPDATA%/autodoc-mcp/cache
```

**Notes:**
- Directory will be created automatically if it doesn't exist
- Requires read/write permissions
- Consider available disk space for large dependency trees

#### `LOG_LEVEL`

**Default:** `INFO`
**Type:** String
**Allowed Values:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
**Description:** Controls verbosity of server logging.

```bash
# Enable debug logging for troubleshooting
export LOG_LEVEL=DEBUG

# Minimal logging for production
export LOG_LEVEL=WARNING
```

**Log Level Details:**
- **`DEBUG`**: Detailed execution traces, cache operations, network requests
- **`INFO`**: Service startup, tool invocations, performance metrics
- **`WARNING`**: Recoverable errors, degraded performance warnings
- **`ERROR`**: Failed requests, unrecoverable errors
- **`CRITICAL`**: Service failures, initialization errors

### Performance Configuration

#### `MAX_DEPENDENCY_CONTEXT`

**Default:** `8`
**Type:** Integer
**Range:** `1-20`
**Description:** Maximum number of dependencies to include in context responses.

```bash
# Include more dependencies for complex projects
export MAX_DEPENDENCY_CONTEXT=12

# Minimal context for faster responses
export MAX_DEPENDENCY_CONTEXT=3
```

**Impact:**
- Higher values provide richer context but slower responses
- Lower values improve speed but may miss important dependencies
- Smart scoping automatically selects most relevant dependencies

#### `MAX_CONTEXT_TOKENS`

**Default:** `30000`
**Type:** Integer
**Range:** `5000-100000`
**Description:** Token budget for AI context responses.

```bash
# Larger context for advanced AI models
export MAX_CONTEXT_TOKENS=50000

# Reduced context for token-limited models
export MAX_CONTEXT_TOKENS=15000
```

**Guidelines:**
- **15k tokens**: Basic context, essential information only
- **30k tokens**: Default, comprehensive context for most use cases
- **50k tokens**: Extended context for complex frameworks
- **100k tokens**: Maximum context for advanced AI models

#### `MAX_CONCURRENT`

**Default:** `10`
**Type:** Integer
**Range:** `1-20`
**Description:** Maximum concurrent PyPI requests for dependency fetching.

```bash
# Conservative concurrency for limited bandwidth
export MAX_CONCURRENT=5

# Aggressive concurrency for high-performance networks
export MAX_CONCURRENT=15
```

**Network Considerations:**
- Lower values for unstable or rate-limited connections
- Higher values for high-bandwidth, stable networks
- PyPI rate limiting may affect optimal values

### Network Configuration

#### `PYPI_BASE_URL`

**Default:** `https://pypi.org/pypi`
**Type:** String (URL)
**Description:** Base URL for PyPI API requests.

```bash
# Use private PyPI mirror
export PYPI_BASE_URL=https://pypi.company.com/simple

# Use alternative PyPI index
export PYPI_BASE_URL=https://test.pypi.org/pypi
```

#### `REQUEST_TIMEOUT`

**Default:** `15`
**Type:** Integer (seconds)
**Range:** `5-60`
**Description:** Timeout for individual PyPI requests.

```bash
# Shorter timeout for fast networks
export REQUEST_TIMEOUT=10

# Longer timeout for slow/unreliable networks
export REQUEST_TIMEOUT=30
```

#### `RETRY_ATTEMPTS`

**Default:** `3`
**Type:** Integer
**Range:** `1-10`
**Description:** Number of retry attempts for failed network requests.

```bash
# More aggressive retries for unreliable networks
export RETRY_ATTEMPTS=5

# No retries for development/testing
export RETRY_ATTEMPTS=1
```

### Cache Configuration

#### `CACHE_CLEANUP_INTERVAL`

**Default:** `3600` (1 hour)
**Type:** Integer (seconds)
**Range:** `300-86400`
**Description:** Interval for automatic cache maintenance.

```bash
# More frequent cleanup for limited storage
export CACHE_CLEANUP_INTERVAL=1800

# Less frequent cleanup for ample storage
export CACHE_CLEANUP_INTERVAL=7200
```

#### `MAX_CACHE_SIZE_MB`

**Default:** `1000` (1GB)
**Type:** Integer (megabytes)
**Range:** `100-10000`
**Description:** Maximum cache size before cleanup triggers.

```bash
# Larger cache for development environments
export MAX_CACHE_SIZE_MB=2000

# Smaller cache for resource-constrained environments
export MAX_CACHE_SIZE_MB=500
```

## MCP Client Configuration

### Standard MCP Configuration Format

```json
{
  "mcpServers": {
    "autodoc-mcp": {
      "command": "autodoc-mcp",
      "env": {
        "CACHE_DIR": "~/.cache/autodoc-mcp",
        "LOG_LEVEL": "INFO",
        "MAX_DEPENDENCY_CONTEXT": "8",
        "MAX_CONTEXT_TOKENS": "30000",
        "MAX_CONCURRENT": "10"
      }
    }
  }
}
```

### Client-Specific Configuration

=== "Claude Desktop"

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

=== "Cursor Desktop"

    ```json
    {
      "mcpServers": {
        "autodoc-mcp": {
          "command": "autodoc-mcp",
          "env": {
            "CACHE_DIR": "~/.cache/autodoc-mcp",
            "LOG_LEVEL": "INFO",
            "MAX_CONTEXT_TOKENS": "25000"
          }
        }
      }
    }
    ```

=== "Continue.dev"

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

=== "Development/Source"

    ```json
    {
      "mcpServers": {
        "autodoc-mcp": {
          "command": "python",
          "args": ["-m", "autodocs_mcp.main"],
          "cwd": "/path/to/autodoc-mcp",
          "env": {
            "CACHE_DIR": "/tmp/autodoc-cache",
            "LOG_LEVEL": "DEBUG",
            "MAX_CONCURRENT": "5"
          }
        }
      }
    }
    ```

## Configuration Profiles

### Production Profile

Optimized for stability and performance:

```bash
export CACHE_DIR="/var/cache/autodoc-mcp"
export LOG_LEVEL="WARNING"
export MAX_DEPENDENCY_CONTEXT="8"
export MAX_CONTEXT_TOKENS="30000"
export MAX_CONCURRENT="10"
export REQUEST_TIMEOUT="15"
export RETRY_ATTEMPTS="3"
```

### Development Profile

Enhanced debugging and flexibility:

```bash
export CACHE_DIR="/tmp/autodoc-cache"
export LOG_LEVEL="DEBUG"
export MAX_DEPENDENCY_CONTEXT="12"
export MAX_CONTEXT_TOKENS="50000"
export MAX_CONCURRENT="5"
export REQUEST_TIMEOUT="30"
export RETRY_ATTEMPTS="1"
```

### Resource-Constrained Profile

Minimal resource usage:

```bash
export CACHE_DIR="~/.cache/autodoc-mcp"
export LOG_LEVEL="ERROR"
export MAX_DEPENDENCY_CONTEXT="3"
export MAX_CONTEXT_TOKENS="15000"
export MAX_CONCURRENT="3"
export MAX_CACHE_SIZE_MB="200"
```

### High-Performance Profile

Maximum speed and throughput:

```bash
export CACHE_DIR="/fast-ssd/autodoc-cache"
export LOG_LEVEL="WARNING"
export MAX_DEPENDENCY_CONTEXT="15"
export MAX_CONTEXT_TOKENS="50000"
export MAX_CONCURRENT="15"
export REQUEST_TIMEOUT="10"
export MAX_CACHE_SIZE_MB="5000"
```

## Configuration Validation

The server validates all configuration values on startup:

### Validation Rules

| Setting | Validation |
|---------|------------|
| `CACHE_DIR` | Must be writable directory |
| `LOG_LEVEL` | Must be valid Python logging level |
| `MAX_DEPENDENCY_CONTEXT` | Integer between 1-20 |
| `MAX_CONTEXT_TOKENS` | Integer between 5000-100000 |
| `MAX_CONCURRENT` | Integer between 1-20 |
| `REQUEST_TIMEOUT` | Integer between 5-60 |
| `RETRY_ATTEMPTS` | Integer between 1-10 |

### Validation Errors

Invalid configuration will cause startup errors:

```
[ERROR] Invalid configuration: MAX_DEPENDENCY_CONTEXT must be between 1 and 20, got 25
[ERROR] Invalid configuration: CACHE_DIR '/invalid/path' is not writable
[CRITICAL] Server startup failed due to configuration errors
```

## Runtime Configuration

Some settings can be modified at runtime through MCP tool parameters:

### `get_package_docs_with_context` Parameters

Override default settings per request:

```python
# Override max dependencies for this request
{
  "package_name": "django",
  "max_dependencies": 12,  # Overrides MAX_DEPENDENCY_CONTEXT
  "max_tokens": 40000      # Overrides MAX_CONTEXT_TOKENS
}
```

### Dynamic Scoping

Context scope can be adjusted per request:

```python
{
  "package_name": "fastapi",
  "context_scope": "runtime",      # Override smart scoping
  "include_dependencies": false    # Disable dependency context
}
```

## Platform-Specific Configuration

### macOS Configuration

```bash
# Standard locations
export CACHE_DIR="~/Library/Caches/autodoc-mcp"
export LOG_LEVEL="INFO"

# Claude Desktop config location
# ~/Library/Application Support/Claude/claude_desktop_config.json
```

### Windows Configuration

```bash
# Use Windows path format
export CACHE_DIR="%LOCALAPPDATA%\\autodoc-mcp\\cache"
export LOG_LEVEL="INFO"

# Claude Desktop config location
# %APPDATA%\Claude\claude_desktop_config.json
```

### Linux Configuration

```bash
# Follow XDG Base Directory specification
export CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/autodoc-mcp"
export LOG_LEVEL="INFO"

# Claude Desktop config location
# ~/.config/Claude/claude_desktop_config.json
```

### Docker Configuration

```dockerfile
FROM python:3.11-slim

# Install AutoDocs
RUN pip install autodoc-mcp

# Configure environment
ENV CACHE_DIR=/app/cache
ENV LOG_LEVEL=INFO
ENV MAX_CONCURRENT=5

# Create cache directory
RUN mkdir -p /app/cache

# Run server
CMD ["autodoc-mcp"]
```

## Troubleshooting Configuration

### Check Current Configuration

```bash
# View environment variables
env | grep -E "(CACHE_DIR|LOG_LEVEL|MAX_)"

# Test configuration
autodoc-mcp --validate-config
```

### Common Configuration Issues

#### Cache Directory Issues

```bash
# Check permissions
ls -la ~/.cache/
mkdir -p ~/.cache/autodoc-mcp
chmod 755 ~/.cache/autodoc-mcp
```

#### Environment Variable Issues

```bash
# Verify environment variables are set
echo $CACHE_DIR
echo $MAX_DEPENDENCY_CONTEXT

# Check shell profile
grep -E "(CACHE_DIR|MAX_)" ~/.bashrc ~/.zshrc ~/.profile
```

#### MCP Client Configuration Issues

1. **JSON Syntax**: Validate JSON configuration files
2. **Path Issues**: Use absolute paths for commands
3. **Environment Variables**: Ensure proper escaping in JSON

## Best Practices

### Security Considerations

- **Cache Location**: Use user-specific cache directories
- **File Permissions**: Ensure cache directory has appropriate permissions
- **Network Security**: Use HTTPS for PyPI connections
- **Proxy Configuration**: Configure corporate proxy settings

### Performance Optimization

- **SSD Storage**: Use fast storage for cache directory
- **Network Tuning**: Adjust concurrency based on network capacity
- **Context Sizing**: Balance context richness with response speed
- **Cache Management**: Monitor cache size and cleanup regularly

### Monitoring and Observability

- **Logging**: Enable appropriate log levels for environment
- **Metrics**: Use health check tools to monitor performance
- **Alerting**: Set up monitoring for service health
- **Cache Analytics**: Track cache hit rates and storage usage

---

## Related Documentation

- [Installation Guide](installation.md) - Initial setup and installation
- [MCP Tools Reference](mcp-tools.md) - Complete tool documentation
- [Troubleshooting Guide](troubleshooting.md) - Common issues and solutions
- [Getting Started Guide](getting-started.md) - Basic usage examples
