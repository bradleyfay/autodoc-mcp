# Missing Requirements - Priority 2 (HIGH)

## Overview
Essential production features missing from the current implementation that are required for enterprise deployment and operational monitoring.

## Missing Production Requirements

### REQUIREMENT #1: Health Check and Monitoring Endpoints
**Priority**: HIGH
**Impact**: Cannot deploy without health checks for load balancers and monitoring

#### Task 4.1: Implement Health Check System
**Assignee**: Full-Stack Developer
**Estimated Time**: 3 hours

**Requirements**:
```python
# src/autodocs_mcp/health.py (new file)

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any
import time
import asyncio

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    message: str
    response_time_ms: float
    timestamp: float

class HealthChecker:
    """Comprehensive health checking for all system components."""

    def __init__(self):
        self.checks = {}

    async def check_cache_manager(self) -> HealthCheck:
        """Check cache manager health."""
        start_time = time.time()

        try:
            if cache_manager is None:
                return HealthCheck(
                    name="cache_manager",
                    status=HealthStatus.UNHEALTHY,
                    message="Cache manager not initialized",
                    response_time_ms=0,
                    timestamp=time.time()
                )

            # Test cache read/write
            test_key = "_health_check_test"
            await cache_manager.invalidate(test_key)  # Cleanup if exists

            response_time = (time.time() - start_time) * 1000

            return HealthCheck(
                name="cache_manager",
                status=HealthStatus.HEALTHY,
                message="Cache operations working",
                response_time_ms=response_time,
                timestamp=time.time()
            )

        except Exception as e:
            return HealthCheck(
                name="cache_manager",
                status=HealthStatus.UNHEALTHY,
                message=f"Cache error: {str(e)}",
                response_time_ms=(time.time() - start_time) * 1000,
                timestamp=time.time()
            )

    async def check_pypi_connectivity(self) -> HealthCheck:
        """Check PyPI API connectivity."""
        start_time = time.time()

        try:
            from .core.network_resilience import NetworkResilientClient

            async with NetworkResilientClient() as client:
                # Test lightweight PyPI endpoint
                config = get_config()
                test_url = f"{config.pypi_base_url}/requests/json"
                await client.get_with_retry(test_url)

            response_time = (time.time() - start_time) * 1000

            return HealthCheck(
                name="pypi_connectivity",
                status=HealthStatus.HEALTHY,
                message="PyPI API accessible",
                response_time_ms=response_time,
                timestamp=time.time()
            )

        except Exception as e:
            return HealthCheck(
                name="pypi_connectivity",
                status=HealthStatus.UNHEALTHY if "not found" not in str(e).lower() else HealthStatus.HEALTHY,
                message=f"PyPI connectivity: {str(e)}",
                response_time_ms=(time.time() - start_time) * 1000,
                timestamp=time.time()
            )

    async def check_dependencies(self) -> HealthCheck:
        """Check dependency parser health."""
        start_time = time.time()

        try:
            if parser is None:
                return HealthCheck(
                    name="dependency_parser",
                    status=HealthStatus.UNHEALTHY,
                    message="Dependency parser not initialized",
                    response_time_ms=0,
                    timestamp=time.time()
                )

            # Test parser with minimal valid project
            from pathlib import Path
            import tempfile

            with tempfile.TemporaryDirectory() as temp_dir:
                test_project = Path(temp_dir) / "pyproject.toml"
                test_project.write_text("""
[project]
name = "health-test"
version = "1.0.0"
dependencies = ["requests>=2.0.0"]
                """)

                result = await parser.parse_project(Path(temp_dir))

                if result.successful_deps > 0:
                    status = HealthStatus.HEALTHY
                    message = f"Parser working, found {result.successful_deps} dependencies"
                else:
                    status = HealthStatus.DEGRADED
                    message = "Parser running but found no dependencies"

            response_time = (time.time() - start_time) * 1000

            return HealthCheck(
                name="dependency_parser",
                status=status,
                message=message,
                response_time_ms=response_time,
                timestamp=time.time()
            )

        except Exception as e:
            return HealthCheck(
                name="dependency_parser",
                status=HealthStatus.UNHEALTHY,
                message=f"Parser error: {str(e)}",
                response_time_ms=(time.time() - start_time) * 1000,
                timestamp=time.time()
            )

    async def get_overall_health(self) -> Dict[str, Any]:
        """Get comprehensive health status."""
        checks = await asyncio.gather(
            self.check_cache_manager(),
            self.check_pypi_connectivity(),
            self.check_dependencies(),
            return_exceptions=True
        )

        health_data = {
            "status": "healthy",
            "timestamp": time.time(),
            "checks": {},
            "summary": {
                "healthy": 0,
                "degraded": 0,
                "unhealthy": 0,
                "total": len(checks)
            }
        }

        overall_status = HealthStatus.HEALTHY

        for check in checks:
            if isinstance(check, Exception):
                health_data["checks"]["unknown_error"] = {
                    "status": "unhealthy",
                    "message": f"Health check failed: {str(check)}",
                    "response_time_ms": 0
                }
                overall_status = HealthStatus.UNHEALTHY
                health_data["summary"]["unhealthy"] += 1
                continue

            health_data["checks"][check.name] = {
                "status": check.status.value,
                "message": check.message,
                "response_time_ms": check.response_time_ms,
                "timestamp": check.timestamp
            }

            if check.status == HealthStatus.UNHEALTHY:
                overall_status = HealthStatus.UNHEALTHY
                health_data["summary"]["unhealthy"] += 1
            elif check.status == HealthStatus.DEGRADED:
                if overall_status == HealthStatus.HEALTHY:
                    overall_status = HealthStatus.DEGRADED
                health_data["summary"]["degraded"] += 1
            else:
                health_data["summary"]["healthy"] += 1

        health_data["status"] = overall_status.value
        return health_data

# Add health endpoints to main.py
@mcp.tool
async def health_check() -> dict[str, Any]:
    """
    Get system health status for monitoring and load balancer checks.

    Returns:
        Comprehensive health status of all system components
    """
    health_checker = HealthChecker()
    return await health_checker.get_overall_health()

@mcp.tool
async def ready_check() -> dict[str, Any]:
    """
    Kubernetes-style readiness check for deployment orchestration.

    Returns:
        Simple ready/not-ready status
    """
    try:
        # Quick checks for readiness
        if parser is None or cache_manager is None or version_resolver is None:
            return {
                "ready": False,
                "reason": "Services not initialized"
            }

        return {
            "ready": True,
            "timestamp": time.time()
        }

    except Exception as e:
        return {
            "ready": False,
            "reason": f"Readiness check failed: {str(e)}"
        }
```

**Files to Create/Modify**:
- `src/autodocs_mcp/health.py` (new)
- `src/autodocs_mcp/main.py` (add health endpoints)

**Acceptance Criteria**:
- ✅ Health check endpoint returns comprehensive status
- ✅ Individual component health checks working
- ✅ Readiness check suitable for K8s deployments
- ✅ Health checks complete within 2 seconds
- ✅ Proper HTTP status codes for load balancers

---

### REQUIREMENT #2: Structured Logging and Observability
**Priority**: HIGH
**Impact**: Cannot troubleshoot production issues without proper logging

#### Task 4.2: Enhance Logging and Metrics
**Assignee**: Full-Stack Developer
**Estimated Time**: 3 hours

**Requirements**:
```python
# src/autodocs_mcp/observability.py (new file)

import time
import json
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager
import structlog
from dataclasses import dataclass, field

@dataclass
class RequestMetrics:
    """Track request performance metrics."""

    request_id: str
    operation: str
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    success: bool = False
    error_type: Optional[str] = None
    cache_hit: bool = False

    @property
    def duration_ms(self) -> float:
        """Calculate request duration in milliseconds."""
        end = self.end_time or time.time()
        return (end - self.start_time) * 1000

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for logging."""
        return {
            "request_id": self.request_id,
            "operation": self.operation,
            "duration_ms": round(self.duration_ms, 2),
            "success": self.success,
            "error_type": self.error_type,
            "cache_hit": self.cache_hit,
            "timestamp": self.start_time
        }

class MetricsCollector:
    """Collect and aggregate performance metrics."""

    def __init__(self):
        self.active_requests: Dict[str, RequestMetrics] = {}
        self.completed_requests: list[RequestMetrics] = []
        self.max_completed = 1000  # Keep last 1000 requests

    def start_request(self, request_id: str, operation: str) -> RequestMetrics:
        """Start tracking a request."""
        metrics = RequestMetrics(request_id=request_id, operation=operation)
        self.active_requests[request_id] = metrics
        return metrics

    def finish_request(self, request_id: str, success: bool = True,
                      error_type: Optional[str] = None, cache_hit: bool = False):
        """Finish tracking a request."""
        if request_id in self.active_requests:
            metrics = self.active_requests.pop(request_id)
            metrics.end_time = time.time()
            metrics.success = success
            metrics.error_type = error_type
            metrics.cache_hit = cache_hit

            # Log the completed request
            logger = structlog.get_logger(__name__)
            logger.info("Request completed", **metrics.to_dict())

            # Store for aggregation (ring buffer)
            self.completed_requests.append(metrics)
            if len(self.completed_requests) > self.max_completed:
                self.completed_requests.pop(0)

    def get_stats(self) -> Dict[str, Any]:
        """Get aggregated performance statistics."""
        if not self.completed_requests:
            return {"total_requests": 0}

        total = len(self.completed_requests)
        successful = sum(1 for r in self.completed_requests if r.success)
        cache_hits = sum(1 for r in self.completed_requests if r.cache_hit)

        durations = [r.duration_ms for r in self.completed_requests]

        # Calculate percentiles
        sorted_durations = sorted(durations)
        p50_idx = int(0.5 * len(sorted_durations))
        p95_idx = int(0.95 * len(sorted_durations))
        p99_idx = int(0.99 * len(sorted_durations))

        return {
            "total_requests": total,
            "success_rate": round(successful / total * 100, 2),
            "cache_hit_rate": round(cache_hits / total * 100, 2),
            "active_requests": len(self.active_requests),
            "response_times": {
                "avg_ms": round(sum(durations) / len(durations), 2),
                "p50_ms": round(sorted_durations[p50_idx], 2),
                "p95_ms": round(sorted_durations[p95_idx], 2),
                "p99_ms": round(sorted_durations[p99_idx], 2),
                "max_ms": round(max(durations), 2)
            }
        }

# Global metrics collector
metrics_collector = MetricsCollector()

@asynccontextmanager
async def track_request(operation: str):
    """Context manager to track request metrics."""
    import uuid
    request_id = str(uuid.uuid4())[:8]

    metrics = metrics_collector.start_request(request_id, operation)

    try:
        yield metrics
        metrics_collector.finish_request(request_id, success=True)
    except Exception as e:
        metrics_collector.finish_request(
            request_id,
            success=False,
            error_type=type(e).__name__
        )
        raise

# Enhanced logging configuration
def setup_production_logging():
    """Configure structured logging for production."""
    processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.JSONRenderer()  # JSON for production
    ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )

# Add metrics endpoint to main.py
@mcp.tool
async def get_metrics() -> dict[str, Any]:
    """
    Get system performance metrics for monitoring.

    Returns:
        Performance statistics and metrics
    """
    return {
        "performance": metrics_collector.get_stats(),
        "timestamp": time.time()
    }
```

**Integration with MCP Tools**:
```python
# Update main.py MCP tools with metrics tracking

@mcp.tool
async def scan_dependencies(project_path: str | None = None) -> dict[str, Any]:
    """Scan project dependencies with metrics tracking."""
    async with track_request("scan_dependencies") as metrics:
        # ... existing implementation ...
        pass

@mcp.tool
async def get_package_docs(
    package_name: str, version_constraint: str | None = None, query: str | None = None
) -> dict[str, Any]:
    """Get package docs with metrics tracking."""
    async with track_request("get_package_docs") as metrics:
        # ... existing implementation ...
        # Set cache_hit flag based on cache result
        metrics_collector.finish_request(
            metrics.request_id,
            cache_hit=from_cache  # Set this based on cache result
        )
```

**Files to Create/Modify**:
- `src/autodocs_mcp/observability.py` (new)
- `src/autodocs_mcp/main.py` (add metrics tracking to all tools)
- `src/autodocs_mcp/config.py` (add logging configuration options)

**Acceptance Criteria**:
- ✅ All MCP operations tracked with performance metrics
- ✅ Structured JSON logging for production
- ✅ Request correlation IDs for tracing
- ✅ Metrics endpoint for monitoring integration
- ✅ Cache hit rates and response time percentiles tracked

---

### REQUIREMENT #3: Configuration Validation and Environment Management
**Priority**: HIGH
**Impact**: Configuration errors cause runtime failures

#### Task 4.3: Configuration Validation System
**Assignee**: Full-Stack Developer
**Estimated Time**: 2 hours

**Requirements**:
```python
# Enhance src/autodocs_mcp/config.py

from pydantic import BaseModel, Field, validator
import os
from pathlib import Path
from urllib.parse import urlparse

class AutoDocsConfig(BaseModel):
    """Application configuration with validation."""

    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".autodocs" / "cache")
    max_concurrent: int = Field(default=10, ge=1, le=100)
    request_timeout: int = Field(default=30, ge=5, le=300)
    log_level: str = Field(default="INFO")
    pypi_base_url: str = Field(default="https://pypi.org/pypi")

    # Version-based caching settings
    max_cached_versions_per_package: int = Field(default=3, ge=1, le=10)
    cache_cleanup_days: int = Field(default=90, ge=1)

    # Context settings
    max_dependency_context: int = Field(default=8, ge=1, le=20)
    max_context_tokens: int = Field(default=30000, ge=1000, le=100000)

    # Performance and rate limiting settings
    max_retry_attempts: int = Field(default=3, ge=1, le=10)
    base_retry_delay: float = Field(default=1.0, ge=0.1, le=10.0)
    max_retry_delay: float = Field(default=30.0, ge=1.0, le=300.0)
    circuit_breaker_threshold: int = Field(default=5, ge=1, le=50)
    circuit_breaker_timeout: float = Field(default=60.0, ge=10.0, le=3600.0)
    rate_limit_requests_per_minute: int = Field(default=60, ge=1, le=1000)
    max_documentation_size: int = Field(default=50000, ge=1000, le=1000000)

    # Deployment settings
    environment: str = Field(default="development")
    debug_mode: bool = Field(default=False)

    @validator('log_level')
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v.upper()

    @validator('pypi_base_url')
    def validate_pypi_url(cls, v):
        """Validate PyPI base URL."""
        try:
            parsed = urlparse(v)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("URL must have scheme and netloc")

            # Security check for trusted domains
            trusted_domains = {"pypi.org", "test.pypi.org", "localhost"}
            if parsed.netloc not in trusted_domains and not v.startswith("http://localhost"):
                raise ValueError(f"Untrusted PyPI domain: {parsed.netloc}")

            return v
        except Exception as e:
            raise ValueError(f"Invalid PyPI URL '{v}': {e}")

    @validator('environment')
    def validate_environment(cls, v):
        """Validate deployment environment."""
        valid_envs = {"development", "staging", "production"}
        if v not in valid_envs:
            raise ValueError(f"Invalid environment: {v}. Must be one of {valid_envs}")
        return v

    @validator('max_retry_delay')
    def validate_retry_delays(cls, v, values):
        """Ensure max_retry_delay > base_retry_delay."""
        base_delay = values.get('base_retry_delay', 1.0)
        if v <= base_delay:
            raise ValueError("max_retry_delay must be greater than base_retry_delay")
        return v

    def model_post_init(self, __context: Any) -> None:
        """Post-initialization validation and setup."""
        # Ensure cache directory exists and is writable
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            # Test write permissions
            test_file = self.cache_dir / ".write_test"
            test_file.write_text("test")
            test_file.unlink()
        except Exception as e:
            raise ValueError(f"Cache directory not writable: {self.cache_dir}. Error: {e}")

    @classmethod
    def from_env(cls) -> "AutoDocsConfig":
        """Load configuration from environment with validation."""
        try:
            config_data = {}

            # Map environment variables to config fields
            env_mappings = {
                "AUTODOCS_CACHE_DIR": "cache_dir",
                "AUTODOCS_MAX_CONCURRENT": ("max_concurrent", int),
                "AUTODOCS_REQUEST_TIMEOUT": ("request_timeout", int),
                "AUTODOCS_LOG_LEVEL": "log_level",
                "AUTODOCS_PYPI_URL": "pypi_base_url",
                "AUTODOCS_MAX_VERSIONS": ("max_cached_versions_per_package", int),
                "AUTODOCS_CLEANUP_DAYS": ("cache_cleanup_days", int),
                "AUTODOCS_MAX_DEPS": ("max_dependency_context", int),
                "AUTODOCS_MAX_TOKENS": ("max_context_tokens", int),
                "AUTODOCS_MAX_RETRY_ATTEMPTS": ("max_retry_attempts", int),
                "AUTODOCS_BASE_RETRY_DELAY": ("base_retry_delay", float),
                "AUTODOCS_MAX_RETRY_DELAY": ("max_retry_delay", float),
                "AUTODOCS_CIRCUIT_BREAKER_THRESHOLD": ("circuit_breaker_threshold", int),
                "AUTODOCS_CIRCUIT_BREAKER_TIMEOUT": ("circuit_breaker_timeout", float),
                "AUTODOCS_RATE_LIMIT_RPM": ("rate_limit_requests_per_minute", int),
                "AUTODOCS_MAX_DOC_SIZE": ("max_documentation_size", int),
                "AUTODOCS_ENVIRONMENT": "environment",
                "AUTODOCS_DEBUG": ("debug_mode", lambda x: x.lower() == "true"),
            }

            for env_var, config_key in env_mappings.items():
                value = os.getenv(env_var)
                if value is not None:
                    if isinstance(config_key, tuple):
                        key, converter = config_key
                        config_data[key] = converter(value)
                    else:
                        config_data[config_key] = value

            # Handle Path conversion for cache_dir
            if "cache_dir" in config_data:
                config_data["cache_dir"] = Path(config_data["cache_dir"])

            return cls(**config_data)

        except Exception as e:
            raise ValueError(f"Configuration validation failed: {e}")

    def validate_production_readiness(self) -> list[str]:
        """Validate configuration for production deployment."""
        issues = []

        if self.environment == "production":
            if self.debug_mode:
                issues.append("Debug mode should not be enabled in production")

            if not self.pypi_base_url.startswith("https://"):
                issues.append("HTTPS required for production PyPI URL")

            if self.log_level == "DEBUG":
                issues.append("Debug logging not recommended for production")

            if self.max_concurrent > 50:
                issues.append("High concurrency may overwhelm PyPI API")

        return issues
```

**Files to Create/Modify**:
- `src/autodocs_mcp/config.py` (enhance existing)
- `src/autodocs_mcp/main.py` (add config validation on startup)

**Acceptance Criteria**:
- ✅ All configuration parameters validated on startup
- ✅ Clear error messages for invalid configuration
- ✅ Production readiness checks implemented
- ✅ Environment-specific validation rules
- ✅ Configuration validation prevents startup with invalid config

## Additional Production Features

### Task 4.4: Request Rate Limiting and Security Headers
**Assignee**: Full-Stack Developer
**Estimated Time**: 2 hours

**Requirements**:
1. **Per-client rate limiting** (if client identification available)
2. **Request size limits** to prevent abuse
3. **Security headers** for HTTP responses
4. **Request correlation IDs** for tracing

**Files to Create/Modify**:
- `src/autodocs_mcp/middleware.py` (new)
- `src/autodocs_mcp/main.py` (integrate middleware)

## Testing Requirements

### Integration Testing
- [ ] Health check endpoints return correct status codes
- [ ] Metrics collection working under load
- [ ] Configuration validation prevents invalid startups
- [ ] Logging format compatible with log aggregation systems

### Performance Testing
- [ ] Health checks complete within SLA (<2 seconds)
- [ ] Metrics collection doesn't impact performance
- [ ] Configuration validation completes quickly
- [ ] Observability overhead <5% of total response time

## Completion Criteria

**Production Requirements Gate**:
1. ✅ Health check endpoints implemented and tested
2. ✅ Comprehensive metrics collection and reporting
3. ✅ Production-ready structured logging
4. ✅ Configuration validation with clear error messages
5. ✅ Request tracking and correlation IDs
6. ✅ Performance overhead acceptable (<5%)
7. ✅ Integration with monitoring systems validated

**Operational Readiness Standards**:
- Health checks suitable for load balancer integration
- Metrics compatible with Prometheus/Grafana
- Logs structured for ELK/Splunk ingestion
- Configuration errors prevent service startup
- Request tracing enables debugging production issues

**Time Allocation**:
- Implementation: 8 hours
- Testing: 2 hours
- Integration: 2 hours
- **Total: 1 day**
