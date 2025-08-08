# Production Bug Fixes - Priority 1 (BLOCKING)

## Overview
Critical bugs that will cause production failures, resource leaks, or service degradation. These must be resolved before deployment.

## Critical Production Bugs

### BUG #1: Configuration Parameter Mismatch
**Severity**: CRITICAL
**Location**: `src/autodocs_mcp/config.py:37-56`
**Impact**: Runtime errors due to missing configuration parameters

#### Task 2.1: Fix Configuration Loading
**Assignee**: Backend Developer
**Estimated Time**: 2 hours

**Problem**: The `from_env()` method doesn't load rate limiting and circuit breaker settings that are used throughout the network resilience code.

**Requirements**:
```python
@classmethod
def from_env(cls) -> "AutoDocsConfig":
    """Load configuration from environment variables."""
    cache_dir_str = os.getenv(
        "AUTODOCS_CACHE_DIR", str(Path.home() / ".autodocs" / "cache")
    )

    return cls(
        cache_dir=Path(cache_dir_str),
        max_concurrent=int(os.getenv("AUTODOCS_MAX_CONCURRENT", "10")),
        request_timeout=int(os.getenv("AUTODOCS_REQUEST_TIMEOUT", "30")),
        log_level=os.getenv("AUTODOCS_LOG_LEVEL", "INFO"),
        pypi_base_url=os.getenv("AUTODOCS_PYPI_URL", "https://pypi.org/pypi"),
        max_cached_versions_per_package=int(
            os.getenv("AUTODOCS_MAX_VERSIONS", "3")
        ),
        cache_cleanup_days=int(os.getenv("AUTODOCS_CLEANUP_DAYS", "90")),
        max_dependency_context=int(os.getenv("AUTODOCS_MAX_DEPS", "8")),
        max_context_tokens=int(os.getenv("AUTODOCS_MAX_TOKENS", "30000")),
        # ADD MISSING PARAMETERS:
        max_retry_attempts=int(os.getenv("AUTODOCS_MAX_RETRY_ATTEMPTS", "3")),
        base_retry_delay=float(os.getenv("AUTODOCS_BASE_RETRY_DELAY", "1.0")),
        max_retry_delay=float(os.getenv("AUTODOCS_MAX_RETRY_DELAY", "30.0")),
        circuit_breaker_threshold=int(os.getenv("AUTODOCS_CIRCUIT_BREAKER_THRESHOLD", "5")),
        circuit_breaker_timeout=float(os.getenv("AUTODOCS_CIRCUIT_BREAKER_TIMEOUT", "60.0")),
        rate_limit_requests_per_minute=int(os.getenv("AUTODOCS_RATE_LIMIT_RPM", "60")),
        max_documentation_size=int(os.getenv("AUTODOCS_MAX_DOC_SIZE", "50000")),
    )
```

**Files to Modify**:
- `src/autodocs_mcp/config.py`

**Acceptance Criteria**:
- ✅ All configuration parameters loaded from environment
- ✅ Default values match field definitions
- ✅ Configuration validation works correctly
- ✅ NetworkResilientClient initialization succeeds
- ✅ No missing parameter runtime errors

---

### BUG #2: HTTP Client Resource Leak
**Severity**: CRITICAL
**Location**: Multiple files using `NetworkResilientClient`
**Impact**: File descriptor exhaustion in long-running processes

#### Task 2.2: Fix HTTP Client Resource Management
**Assignee**: Backend Developer
**Estimated Time**: 4 hours

**Problem**: Inconsistent httpx client cleanup patterns will exhaust file descriptors under load.

**Requirements**:

1. **Implement Connection Pool Manager**:
```python
class ConnectionPoolManager:
    """Singleton connection pool manager for HTTP clients."""

    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self._clients: dict[str, httpx.AsyncClient] = {}
            self.initialized = True

    async def get_client(self, config_key: str) -> httpx.AsyncClient:
        """Get or create HTTP client with connection pooling."""
        async with self._lock:
            if config_key not in self._clients:
                self._clients[config_key] = httpx.AsyncClient(
                    timeout=httpx.Timeout(30.0),
                    follow_redirects=True,
                    headers={"User-Agent": "AutoDocs-MCP/1.0"},
                    limits=httpx.Limits(
                        max_connections=100,
                        max_keepalive_connections=20,
                        keepalive_expiry=30.0,
                    ),
                )
            return self._clients[config_key]

    async def close_all(self):
        """Close all HTTP clients."""
        async with self._lock:
            for client in self._clients.values():
                await client.aclose()
            self._clients.clear()
```

2. **Update NetworkResilientClient**:
```python
class NetworkResilientClient:
    """HTTP client with built-in retry logic, circuit breaker, and rate limiting."""

    def __init__(self, retry_config: RetryConfig | None = None):
        config = get_config()
        self.retry_config = retry_config or RetryConfig(
            max_attempts=config.max_retry_attempts,
            base_delay=config.base_retry_delay,
            max_delay=config.max_retry_delay,
        )
        self._pool_manager = ConnectionPoolManager()
        self._circuit_breaker = CircuitBreaker(
            failure_threshold=config.circuit_breaker_threshold,
            reset_timeout=config.circuit_breaker_timeout,
        )
        self._rate_limiter = RateLimiter(config.rate_limit_requests_per_minute)

    async def __aenter__(self) -> "NetworkResilientClient":
        """Enter async context manager."""
        # Get shared client from pool instead of creating new one
        self._client = await self._pool_manager.get_client("default")
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit async context manager."""
        # Don't close the client - it's managed by the pool
        self._client = None
```

**Files to Modify**:
- `src/autodocs_mcp/core/network_resilience.py`
- `src/autodocs_mcp/core/network_client.py`
- `src/autodocs_mcp/main.py` (add cleanup in shutdown)

**Acceptance Criteria**:
- ✅ HTTP clients use connection pooling
- ✅ No file descriptor leaks under continuous load
- ✅ Proper cleanup on application shutdown
- ✅ Connection limits prevent resource exhaustion
- ✅ Performance maintained or improved

---

### BUG #3: Memory Leak in Rate Limiter
**Severity**: CRITICAL
**Location**: `src/autodocs_mcp/core/network_resilience.py:70`
**Impact**: Unbounded memory growth under heavy load

#### Task 2.3: Fix Rate Limiter Memory Management
**Assignee**: Backend Developer
**Estimated Time**: 2 hours

**Problem**: The rate limiter deque can grow without bounds if cleanup fails or is interrupted.

**Requirements**:
```python
class RateLimiter:
    """Simple rate limiter with sliding window and memory bounds."""

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: deque[float] = deque()
        self._max_entries = max(requests_per_minute * 2, 1000)  # Safety limit
        self._last_cleanup = time.time()

    async def acquire(self) -> None:
        """Wait if necessary to respect rate limits."""
        now = time.time()

        # Force cleanup every 60 seconds to prevent memory leaks
        if now - self._last_cleanup > 60:
            await self._force_cleanup(now)
            self._last_cleanup = now

        # Remove requests older than 1 minute
        await self._cleanup_old_requests(now)

        # Emergency cleanup if deque grows too large
        if len(self.requests) > self._max_entries:
            logger.warning(
                "Rate limiter deque exceeded max size, forcing cleanup",
                current_size=len(self.requests),
                max_size=self._max_entries
            )
            await self._force_cleanup(now)

        # If we're at the limit, wait until we can make another request
        if len(self.requests) >= self.requests_per_minute:
            if self.requests:  # Safety check
                sleep_time = 60 - (now - self.requests[0]) + 0.1  # Small buffer
                if sleep_time > 0:
                    logger.debug("Rate limiting: sleeping", sleep_time=sleep_time)
                    await asyncio.sleep(sleep_time)

        # Record this request
        self.requests.append(now)

    async def _cleanup_old_requests(self, now: float) -> None:
        """Remove requests older than 1 minute."""
        cutoff = now - 60
        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()

    async def _force_cleanup(self, now: float) -> None:
        """Force cleanup of old entries to prevent memory leaks."""
        cutoff = now - 60
        # Keep only recent requests
        self.requests = deque(t for t in self.requests if t >= cutoff)

        # If still too large, keep only the most recent entries
        if len(self.requests) > self.requests_per_minute:
            self.requests = deque(
                sorted(self.requests)[-self.requests_per_minute:]
            )
```

**Files to Modify**:
- `src/autodocs_mcp/core/network_resilience.py`

**Acceptance Criteria**:
- ✅ Rate limiter memory usage bounded
- ✅ Periodic cleanup prevents memory leaks
- ✅ Emergency cleanup when limits exceeded
- ✅ Rate limiting functionality preserved
- ✅ Performance monitoring and logging added

---

### HIGH PRIORITY: Graceful Shutdown Implementation
**Severity**: HIGH
**Location**: `src/autodocs_mcp/main.py`
**Impact**: Ungraceful shutdowns may corrupt cache or lose data

#### Task 2.4: Implement Graceful Shutdown
**Assignee**: DevOps Engineer + Backend Developer
**Estimated Time**: 3 hours

**Requirements**:
```python
import signal
import asyncio
from contextlib import asynccontextmanager

class GracefulShutdown:
    """Handle graceful shutdown of the MCP server."""

    def __init__(self):
        self.shutdown_event = asyncio.Event()
        self.active_requests = 0
        self.max_shutdown_wait = 30.0  # seconds

    def register_signals(self):
        """Register signal handlers for graceful shutdown."""
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, initiating graceful shutdown")
        self.shutdown_event.set()

    @asynccontextmanager
    async def request_context(self):
        """Context manager to track active requests."""
        self.active_requests += 1
        try:
            yield
        finally:
            self.active_requests -= 1

    async def wait_for_shutdown(self):
        """Wait for shutdown signal and cleanup."""
        await self.shutdown_event.wait()

        logger.info("Shutting down gracefully...")

        # Wait for active requests to complete
        start_time = asyncio.get_event_loop().time()
        while self.active_requests > 0:
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed > self.max_shutdown_wait:
                logger.warning(
                    f"Forcing shutdown after {elapsed}s with {self.active_requests} active requests"
                )
                break

            logger.info(f"Waiting for {self.active_requests} active requests to complete")
            await asyncio.sleep(0.5)

        # Cleanup resources
        await self._cleanup_resources()

    async def _cleanup_resources(self):
        """Cleanup application resources."""
        # Close HTTP client connections
        pool_manager = ConnectionPoolManager()
        await pool_manager.close_all()

        # Flush any pending cache writes
        if cache_manager:
            # Add any pending cache operations cleanup
            pass

        logger.info("Graceful shutdown completed")

# Update main function
async def async_main():
    """Async main function with graceful shutdown."""
    shutdown_handler = GracefulShutdown()
    shutdown_handler.register_signals()

    try:
        await initialize_services()
        logger.info("Starting AutoDocs MCP Server")

        # Start server and wait for shutdown
        server_task = asyncio.create_task(run_mcp_server())
        shutdown_task = asyncio.create_task(shutdown_handler.wait_for_shutdown())

        await asyncio.wait(
            [server_task, shutdown_task],
            return_when=asyncio.FIRST_COMPLETED
        )

    except Exception as e:
        logger.error("Server startup failed", error=str(e))
        raise
    finally:
        await shutdown_handler._cleanup_resources()

def main() -> None:
    """Entry point for the MCP server."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error("Server failed", error=str(e))
        raise
```

**Files to Modify**:
- `src/autodocs_mcp/main.py`
- Add decorators to MCP tools for request tracking

**Acceptance Criteria**:
- ✅ Signal handlers registered for SIGTERM/SIGINT
- ✅ Active requests tracked and allowed to complete
- ✅ Resources properly cleaned up on shutdown
- ✅ Maximum shutdown time enforced
- ✅ Graceful shutdown tested in staging

## Testing Requirements

### Load Testing
- [ ] Memory usage under sustained load
- [ ] File descriptor usage monitoring
- [ ] HTTP connection pool behavior
- [ ] Rate limiter performance with high throughput

### Integration Testing
- [ ] Configuration loading from all environment variables
- [ ] HTTP client cleanup after extended use
- [ ] Graceful shutdown with active requests
- [ ] Resource cleanup verification

### Stress Testing
- [ ] Rate limiter under burst traffic
- [ ] Circuit breaker state transitions
- [ ] Connection pool limits
- [ ] Memory usage over 24+ hours

## Completion Criteria

**Production Reliability Gate**:
1. ✅ All configuration parameters properly loaded
2. ✅ HTTP clients use connection pooling
3. ✅ Rate limiter memory usage bounded
4. ✅ Graceful shutdown implemented and tested
5. ✅ No resource leaks after 24-hour test run
6. ✅ Load testing passes without degradation

**Time Allocation**:
- Implementation: 8 hours
- Testing: 4 hours
- Integration: 2 hours
- **Total: 1.5 days**
