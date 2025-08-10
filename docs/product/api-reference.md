# API Reference

Technical reference for AutoDocs MCP Server tools and advanced integration patterns.

## 📋 Quick Reference

| Tool | Purpose | Type | Required Parameters |
|------|---------|------|-------------------|
| `scan_dependencies` | Parse project dependencies | Core | None |
| `get_package_docs_with_context` | Get package + dependencies | Core | `package_name` |
| `get_package_docs` | Get single package docs | Core | `package_name` |
| `refresh_cache` | Clear documentation cache | Cache | None |
| `get_cache_stats` | View cache statistics | Cache | None |
| `health_check` | Comprehensive health status | Health | None |
| `ready_check` | Readiness probe | Health | None |
| `get_metrics` | Performance metrics | Health | None |

## 🛠️ Core Tools

### scan_dependencies

Parses project dependencies from pyproject.toml with graceful error handling.

**Parameters:**
- `project_path` (optional): Path to project directory (default: current directory)

**Response Structure:**
```json
{
  "success": true,
  "project_name": "my-project",
  "total_dependencies": 12,
  "successful_parsing": 10,
  "failed_parsing": 2,
  "dependencies": [
    {
      "name": "fastapi",
      "version_constraint": ">=0.100.0",
      "dependency_type": "runtime"
    }
  ],
  "errors": [
    {
      "dependency": "malformed-dep",
      "error": "Invalid version constraint",
      "suggestion": "Check pyproject.toml syntax"
    }
  ]
}
```

### get_package_docs_with_context

⭐ **Primary Phase 4 Tool** - Retrieves comprehensive documentation context including dependencies.

**Parameters:**
- `package_name` (required): Primary package to document
- `version_constraint` (optional): Version constraint for primary package
- `include_dependencies` (optional): Include dependency context (default: true)
- `context_scope` (optional): "primary_only", "runtime", or "smart" (default: "smart")
- `max_dependencies` (optional): Maximum dependencies to include (default: 8)
- `max_tokens` (optional): Token budget for context (default: 30000)

**Response Structure:**
```json
{
  "success": true,
  "context": {
    "primary_package": {
      "name": "fastapi",
      "version": "0.104.1",
      "summary": "FastAPI framework, high performance...",
      "key_features": ["Automatic API docs", "Type hints"],
      "main_classes": ["FastAPI", "APIRouter", "Depends"],
      "usage_examples": "from fastapi import FastAPI\napp = FastAPI()..."
    },
    "runtime_dependencies": [
      {
        "name": "pydantic",
        "version": "2.5.1",
        "why_included": "Required by fastapi",
        "relevance_score": 0.95,
        "summary": "Data validation using Python type hints"
      }
    ],
    "context_scope": "smart (2 deps)",
    "total_packages": 3,
    "token_estimate": 15420
  },
  "performance": {
    "total_time": 0.89,
    "cache_hits": 1,
    "cache_misses": 2,
    "concurrent_requests": 2
  }
}
```

**Context Scoping Options:**

| Scope | Description | Use Case |
|-------|-------------|----------|
| `"primary_only"` | Only the requested package | Focused analysis |
| `"runtime"` | Primary + runtime dependencies | Production context |
| `"smart"` | Relevance-scored selection | AI assistance (recommended) |

### get_package_docs (Legacy)

Retrieves basic documentation for a single package.

**Parameters:**
- `package_name` (required): Package to document
- `version_constraint` (optional): Version constraint
- `query` (optional): Filter documentation sections

**Note:** For rich context with dependencies, use `get_package_docs_with_context` instead.

## 🗄️ Cache Management Tools

### refresh_cache

Clears the local documentation cache.

**Response Structure:**
```json
{
  "success": true,
  "cleared_entries": 47,
  "freed_space_mb": 15.3,
  "cache_location": "/Users/user/.cache/autodoc-mcp"
}
```

### get_cache_stats

Gets statistics about the documentation cache.

**Response Structure:**
```json
{
  "success": true,
  "total_entries": 47,
  "total_size_mb": 15.3,
  "cache_hit_rate": 0.73,
  "most_accessed": ["requests", "fastapi", "pydantic"],
  "cached_packages": [
    {
      "package": "fastapi",
      "version": "0.104.1",
      "size_mb": 2.1,
      "last_accessed": "2025-01-15T10:30:00Z"
    }
  ]
}
```

## 🏥 Health & Monitoring Tools

### health_check

Comprehensive health status for monitoring and load balancers.

**Response Structure:**
```json
{
  "status": "healthy",
  "components": {
    "cache_manager": {"status": "healthy", "details": "47 entries"},
    "network_client": {"status": "healthy", "details": "Circuit breaker: closed"},
    "pypi_connectivity": {"status": "healthy", "response_time": 0.15}
  },
  "system_info": {
    "version": "0.4.2",
    "uptime_seconds": 3600,
    "memory_usage_mb": 45.2
  }
}
```

### ready_check

Kubernetes-style readiness check.

**Response Structure:**
```json
{
  "ready": true,
  "message": "Server ready to handle requests"
}
```

### get_metrics

System performance metrics.

**Response Structure:**
```json
{
  "performance": {
    "total_requests": 156,
    "average_response_time": 0.84,
    "cache_hit_rate": 0.73,
    "error_rate": 0.02
  },
  "health": {
    "circuit_breaker_state": "closed",
    "active_connections": 2,
    "memory_usage_mb": 45.2
  }
}
```

## 🔧 Advanced Configuration

### Environment Variables

Complete reference for all configuration options:

```bash
# Cache Configuration
export CACHE_DIR="~/.cache/autodoc-mcp"           # Cache location
export MAX_CACHE_SIZE_MB=500                      # Max cache size

# Context Configuration
export MAX_DEPENDENCY_CONTEXT=8                   # Max dependencies in context
export MAX_CONTEXT_TOKENS=30000                   # Token budget
export DEFAULT_CONTEXT_SCOPE="smart"              # Default scoping

# Performance Configuration
export MAX_CONCURRENT=10                          # Concurrent PyPI requests
export REQUEST_TIMEOUT=15                         # Request timeout (seconds)
export CIRCUIT_BREAKER_THRESHOLD=5                # Failure threshold

# Network Configuration
export RETRY_ATTEMPTS=3                           # Retry attempts
export BACKOFF_MULTIPLIER=2                       # Exponential backoff
export CONNECTION_POOL_SIZE=20                    # HTTP connection pool

# Logging Configuration
export LOG_LEVEL="INFO"                           # Logging level
export STRUCTURED_LOGGING=true                    # JSON logging format
```

### Framework Detection

AutoDocs provides enhanced context for major frameworks:

| Framework | Enhanced Features |
|-----------|------------------|
| **FastAPI** | Includes Pydantic, Starlette, Uvicorn automatically |
| **Django** | Includes database connectors, common packages |
| **Flask** | Includes Werkzeug, Jinja2, common extensions |
| **Requests** | Includes urllib3, security packages |
| **Data Science** | Special handling for pandas, numpy, scipy stack |

### Performance Tuning

**For High-Volume Usage:**
```bash
export MAX_CONCURRENT=15
export CONNECTION_POOL_SIZE=30
export MAX_CACHE_SIZE_MB=1000
```

**For Development:**
```bash
export LOG_LEVEL="DEBUG"
export MAX_DEPENDENCY_CONTEXT=12
export MAX_CONTEXT_TOKENS=50000
```

**For Production:**
```bash
export LOG_LEVEL="WARNING"
export STRUCTURED_LOGGING=true
export CIRCUIT_BREAKER_THRESHOLD=3
```

## 🔌 Integration Patterns

### Custom MCP Client Integration

```python
import json
import subprocess

def call_autodocs_tool(tool_name, **params):
    """Call AutoDocs MCP tool programmatically."""
    cmd = ["autodoc-mcp"]

    # Format MCP request
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": params
        },
        "id": 1
    }

    # Execute and parse response
    result = subprocess.run(
        cmd,
        input=json.dumps(request),
        capture_output=True,
        text=True
    )

    return json.loads(result.stdout)

# Example usage
context = call_autodocs_tool(
    "get_package_docs_with_context",
    package_name="fastapi",
    context_scope="smart"
)
```

### Health Check Integration

```bash
#!/bin/bash
# Health check script for deployment

HEALTH_RESPONSE=$(echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"health_check"},"id":1}' | autodoc-mcp)

if echo "$HEALTH_RESPONSE" | jq -r '.result.status' | grep -q "healthy"; then
    exit 0
else
    exit 1
fi
```

## 🚨 Error Handling

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `PACKAGE_NOT_FOUND` | Package doesn't exist on PyPI | Verify package name spelling |
| `NETWORK_ERROR` | PyPI connectivity issues | Check network connection |
| `CACHE_ERROR` | Cache read/write failure | Check cache directory permissions |
| `VALIDATION_ERROR` | Invalid parameter values | Review parameter specifications |
| `TIMEOUT_ERROR` | Request exceeded timeout | Increase timeout or check network |

### Error Response Structure

```json
{
  "success": false,
  "error": {
    "code": "PACKAGE_NOT_FOUND",
    "message": "Package 'nonexistent-pkg' not found on PyPI",
    "details": {
      "package_name": "nonexistent-pkg",
      "suggestions": ["Check spelling", "Verify package exists"]
    },
    "recovery_suggestions": [
      "Verify the package name is correct",
      "Check if the package is published to PyPI"
    ]
  }
}
```

---

## 📚 Related Documentation

- [Getting Started](getting-started.md) - Basic usage and setup
- [MCP Tools](mcp-tools.md) - Detailed tool usage examples
- [Configuration](configuration.md) - Environment and configuration
- [Troubleshooting](troubleshooting.md) - Problem resolution
