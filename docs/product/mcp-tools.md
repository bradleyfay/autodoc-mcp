# MCP Tools Reference

The AutoDocs MCP Server provides **8 production-ready MCP tools** organized into three functional categories. Each tool follows MCP protocol standards and provides structured JSON responses.

## Tool Categories Overview

| Category | Tools | Purpose |
|----------|-------|---------|
| **Core Documentation** | `scan_dependencies`, `get_package_docs`, `get_package_docs_with_context` | Parse projects and fetch documentation |
| **Cache Management** | `refresh_cache`, `get_cache_stats` | Manage documentation cache |
| **System Health** | `health_check`, `ready_check`, `get_metrics` | Monitor system status |

## Core Documentation Tools

### `scan_dependencies`

**Purpose:** Parse Python project dependencies from pyproject.toml files with graceful error handling.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `project_path` | string | No | Current directory | Path to project directory containing pyproject.toml |

#### Response Structure

```json
{
  "success": true,
  "project_name": "my-fastapi-app",
  "total_dependencies": 12,
  "successfully_parsed": 10,
  "failed_to_parse": 2,
  "dependencies": [
    {
      "name": "fastapi",
      "version_constraint": ">=0.100.0",
      "category": "main"
    },
    {
      "name": "pytest",
      "version_constraint": "^7.0.0",
      "category": "dev"
    }
  ],
  "parsing_errors": [
    {
      "raw_spec": "invalid-package==",
      "error": "Invalid version constraint"
    }
  ],
  "metadata": {
    "python_requires": ">=3.8",
    "description": "My FastAPI application"
  }
}
```

#### Use Cases

- **Project Discovery**: Understand what packages a project uses
- **Dependency Analysis**: Get structured dependency information
- **Version Constraint Validation**: Identify malformed dependency specifications
- **Development Setup**: Prepare environment for new projects

#### Example Usage

AI assistants can use this tool when users ask questions like:
- "What packages does this project use?"
- "Show me the project dependencies"
- "What version of FastAPI is required?"

---

### `get_package_docs_with_context` ⭐

**Purpose:** Retrieve comprehensive documentation context including the requested package and its most relevant dependencies with smart scoping. This is the primary Phase 4 tool for rich AI context.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `package_name` | string | Yes | - | Primary package name to document |
| `version_constraint` | string | No | Latest | Version constraint for primary package |
| `include_dependencies` | boolean | No | `true` | Whether to include dependency context |
| `context_scope` | string | No | `"smart"` | Context scope: `"primary_only"`, `"runtime"`, or `"smart"` |
| `max_dependencies` | integer | No | 8 | Maximum number of dependencies to include |
| `max_tokens` | integer | No | 30000 | Maximum token budget for context |

#### Context Scope Options

- **`"primary_only"`**: Only the requested package, no dependencies
- **`"runtime"`**: Include all runtime dependencies (excludes dev/test dependencies)
- **`"smart"`**: Intelligent selection of most relevant dependencies based on framework awareness

#### Response Structure

```json
{
  "success": true,
  "context": {
    "primary_package": {
      "name": "fastapi",
      "version": "0.104.1",
      "summary": "FastAPI framework, high performance, easy to learn, fast to code, ready for production",
      "key_features": [
        "Automatic interactive API documentation",
        "Based on standard Python type hints",
        "High performance, on par with NodeJS and Go"
      ],
      "main_classes": ["FastAPI", "APIRouter", "Depends", "HTTPException"],
      "key_functions": ["Depends", "HTTPException", "status"],
      "usage_examples": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'Hello': 'World'}",
      "documentation_url": "https://fastapi.tiangolo.com/"
    },
    "runtime_dependencies": [
      {
        "name": "pydantic",
        "version": "2.5.1",
        "why_included": "Required by fastapi for data validation",
        "relevance_score": 0.95,
        "summary": "Data validation using Python type hints",
        "key_features": [
          "Data validation and settings management",
          "JSON serialization/deserialization"
        ],
        "main_classes": ["BaseModel", "Field", "validator"]
      },
      {
        "name": "starlette",
        "version": "0.27.0",
        "why_included": "Required by fastapi as ASGI foundation",
        "relevance_score": 0.90,
        "summary": "Lightweight ASGI framework/toolkit",
        "key_features": [
          "ASGI framework foundation",
          "Routing and middleware support"
        ],
        "main_classes": ["Request", "Response", "Middleware"]
      }
    ],
    "context_metadata": {
      "total_packages": 3,
      "context_scope": "smart (2 runtime deps)",
      "token_estimate": 15420,
      "truncated": false,
      "framework_detected": "FastAPI"
    }
  },
  "performance": {
    "total_time_seconds": 0.89,
    "cache_hits": 1,
    "cache_misses": 2,
    "network_requests": 2,
    "concurrent_fetches": 2
  }
}
```

#### Smart Framework Detection

The tool includes special handling for major frameworks:

| Framework | Enhanced Dependencies | Priority Boost |
|-----------|----------------------|----------------|
| **FastAPI** | pydantic, starlette, uvicorn | +0.3 relevance |
| **Django** | django-rest-framework, psycopg2 | +0.2 relevance |
| **Flask** | werkzeug, jinja2, flask-sqlalchemy | +0.2 relevance |
| **SQLAlchemy** | alembic, psycopg2, pymysql | +0.2 relevance |

#### Use Cases

- **AI Code Generation**: Provide comprehensive context for accurate code suggestions
- **Framework Learning**: Understand how packages work together in ecosystems
- **API Integration**: Get complete context for API libraries and their dependencies
- **Troubleshooting**: Understand package relationships when debugging issues

#### Example Usage

AI assistants use this tool when users ask questions like:
- "Help me build a FastAPI application with user authentication"
- "Show me how to use SQLAlchemy with async support"
- "What are the key features of the requests library?"

---

### `get_package_docs` (Legacy)

**Purpose:** Retrieve basic documentation for a single package without dependency context. This is the legacy tool - prefer `get_package_docs_with_context` for rich AI contexts.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `package_name` | string | Yes | - | Package name to document |
| `version_constraint` | string | No | Latest | Version constraint for the package |
| `query` | string | No | None | Filter documentation sections by keyword |

#### Response Structure

```json
{
  "success": true,
  "package": {
    "name": "requests",
    "version": "2.31.0",
    "summary": "Python HTTP for Humans",
    "key_features": [
      "Simple HTTP library for Python",
      "Built-in JSON decoder",
      "Automatic decompression"
    ],
    "main_classes": ["Session", "Request", "Response"],
    "usage_examples": "import requests\n\nr = requests.get('https://api.github.com')\nprint(r.json())"
  },
  "performance": {
    "fetch_time_seconds": 0.12,
    "cache_hit": true
  }
}
```

#### Use Cases

- **Simple Package Lookup**: Quick documentation for single packages
- **Legacy Integration**: Existing code that depends on the simpler interface
- **Minimal Context**: When you specifically don't want dependency information

## Cache Management Tools

### `refresh_cache`

**Purpose:** Clear the local documentation cache to force fresh fetches from PyPI.

#### Parameters

None - this tool takes no parameters.

#### Response Structure

```json
{
  "success": true,
  "cache_cleared": true,
  "statistics": {
    "files_removed": 45,
    "space_freed_mb": 12.3,
    "cache_directory": "/Users/user/.cache/autodoc-mcp"
  },
  "message": "Cache successfully cleared"
}
```

#### Use Cases

- **Force Refresh**: Clear stale cache entries
- **Debugging**: Eliminate cache-related issues
- **Development**: Test with fresh documentation fetches
- **Maintenance**: Regular cache cleanup

#### Example Usage

AI assistants use this when users ask:
- "Clear the AutoDocs cache"
- "Refresh the documentation cache"
- "Remove cached documentation"

---

### `get_cache_stats`

**Purpose:** View statistics about the documentation cache including cached packages and performance metrics.

#### Parameters

None - this tool takes no parameters.

#### Response Structure

```json
{
  "success": true,
  "cache_info": {
    "total_entries": 127,
    "total_size_mb": 45.2,
    "cache_directory": "/Users/user/.cache/autodoc-mcp",
    "oldest_entry": "2024-01-15T10:30:00Z",
    "newest_entry": "2024-08-10T14:25:00Z"
  },
  "performance_stats": {
    "total_requests": 1543,
    "cache_hits": 1205,
    "cache_misses": 338,
    "hit_rate_percent": 78.1,
    "average_response_time_ms": 45
  },
  "cached_packages": [
    {
      "name": "fastapi",
      "version": "0.104.1",
      "cached_at": "2024-08-10T14:25:00Z",
      "size_kb": 234
    },
    {
      "name": "pydantic",
      "version": "2.5.1",
      "cached_at": "2024-08-10T14:24:00Z",
      "size_kb": 189
    }
  ]
}
```

#### Use Cases

- **Cache Monitoring**: Understand cache performance and usage
- **Storage Management**: Monitor disk space usage
- **Performance Analysis**: Analyze hit rates and response times
- **Debugging**: Verify which packages are cached

#### Example Usage

AI assistants use this when users ask:
- "What's the status of the AutoDocs cache?"
- "How much space is the documentation cache using?"
- "Show me cache performance statistics"

## System Health & Monitoring Tools

### `health_check`

**Purpose:** Comprehensive health status check for monitoring systems and load balancers.

#### Parameters

None - this tool takes no parameters.

#### Response Structure

```json
{
  "success": true,
  "overall_status": "healthy",
  "timestamp": "2024-08-10T14:30:00Z",
  "components": {
    "cache_system": {
      "status": "healthy",
      "details": {
        "cache_directory_accessible": true,
        "cache_write_test": "passed",
        "cache_read_test": "passed"
      }
    },
    "network_connectivity": {
      "status": "healthy",
      "details": {
        "pypi_reachable": true,
        "dns_resolution": "working",
        "last_successful_request": "2024-08-10T14:29:45Z"
      }
    },
    "core_services": {
      "status": "healthy",
      "details": {
        "dependency_parser": "initialized",
        "context_fetcher": "initialized",
        "doc_fetcher": "initialized"
      }
    }
  },
  "system_info": {
    "version": "0.4.2",
    "uptime_seconds": 3600,
    "python_version": "3.11.5",
    "memory_usage_mb": 128.5
  }
}
```

#### Health Status Values

- **`"healthy"`**: All systems operational
- **`"degraded"`**: Some non-critical issues present
- **`"unhealthy"`**: Critical systems failing

#### Use Cases

- **Load Balancer Checks**: Determine if instance can handle traffic
- **Monitoring Systems**: Automated health monitoring
- **Debugging**: Diagnose system-level issues
- **Operations**: Pre-deployment health verification

---

### `ready_check`

**Purpose:** Kubernetes-style readiness check for deployment orchestration.

#### Parameters

None - this tool takes no parameters.

#### Response Structure

```json
{
  "success": true,
  "ready": true,
  "timestamp": "2024-08-10T14:30:00Z",
  "checks": {
    "services_initialized": true,
    "cache_accessible": true,
    "network_available": true
  },
  "message": "Service ready to handle requests"
}
```

#### Ready States

- **`ready: true`**: Service can handle MCP requests
- **`ready: false`**: Service is initializing or has critical issues

#### Use Cases

- **Container Orchestration**: Kubernetes readiness probes
- **Deployment Automation**: Wait for service readiness
- **Load Balancing**: Route traffic only to ready instances
- **CI/CD Pipelines**: Verify deployment success

---

### `get_metrics`

**Purpose:** Detailed system performance metrics for monitoring and analysis.

#### Parameters

None - this tool takes no parameters.

#### Response Structure

```json
{
  "success": true,
  "timestamp": "2024-08-10T14:30:00Z",
  "performance_metrics": {
    "request_stats": {
      "total_requests": 1543,
      "successful_requests": 1498,
      "failed_requests": 45,
      "success_rate_percent": 97.1,
      "average_response_time_ms": 245,
      "p95_response_time_ms": 850,
      "p99_response_time_ms": 1200
    },
    "cache_metrics": {
      "cache_hits": 1205,
      "cache_misses": 338,
      "hit_rate_percent": 78.1,
      "total_cached_packages": 127,
      "cache_size_mb": 45.2
    },
    "network_metrics": {
      "pypi_requests": 892,
      "successful_fetches": 847,
      "failed_fetches": 45,
      "average_fetch_time_ms": 180,
      "concurrent_request_count": 3
    },
    "system_metrics": {
      "memory_usage_mb": 128.5,
      "cpu_usage_percent": 12.3,
      "uptime_seconds": 3600,
      "active_connections": 5
    }
  },
  "error_summary": {
    "network_errors": 23,
    "parsing_errors": 12,
    "cache_errors": 8,
    "other_errors": 2
  }
}
```

#### Metric Categories

- **Request Stats**: MCP tool invocation performance
- **Cache Metrics**: Documentation cache performance
- **Network Metrics**: PyPI API interaction performance
- **System Metrics**: Resource usage and system health
- **Error Summary**: Error counts by category

#### Use Cases

- **Performance Monitoring**: Track system performance over time
- **Capacity Planning**: Understand resource usage patterns
- **SLA Monitoring**: Verify response time commitments
- **Optimization**: Identify performance bottlenecks

## Tool Selection Guide

### For AI Assistants

**Primary Tool**: Use `get_package_docs_with_context` for most documentation requests.

**When to use each tool:**

| User Request | Recommended Tool | Reason |
|--------------|------------------|---------|
| "Help me with FastAPI" | `get_package_docs_with_context` | Provides FastAPI + pydantic + starlette context |
| "What packages does this project use?" | `scan_dependencies` | Analyzes local project structure |
| "Clear the documentation cache" | `refresh_cache` | Direct cache management |
| "Is AutoDocs working properly?" | `health_check` | Comprehensive status check |

### For Monitoring Systems

| Use Case | Tool | Integration Pattern |
|----------|------|-------------------|
| **Load Balancer Health** | `health_check` | HTTP 200 if healthy |
| **Kubernetes Readiness** | `ready_check` | Pod readiness probe |
| **Performance Monitoring** | `get_metrics` | Periodic metric collection |
| **Cache Monitoring** | `get_cache_stats` | Storage and performance tracking |

### Error Handling

All tools return consistent error structures:

```json
{
  "success": false,
  "error": {
    "type": "NetworkError",
    "message": "Failed to connect to PyPI",
    "details": {
      "url": "https://pypi.org/pypi/fastapi/json",
      "timeout_seconds": 15
    },
    "suggestion": "Check network connectivity and try again"
  }
}
```

Common error types:
- **`NetworkError`**: PyPI connectivity issues
- **`ValidationError`**: Invalid parameters
- **`CacheError`**: Cache system issues
- **`ParsingError`**: Package metadata parsing failures
- **`RateLimitError`**: PyPI rate limiting

Each error includes actionable suggestions for resolution.
