# Stream E: Performance & Rate Limiting

## Overview
Implement advanced timeout handling, intelligent rate limiting, and performance optimization to ensure the MCP server remains responsive under various load conditions and network scenarios.

## Current State
- Basic 30-second timeout configuration
- Simple semaphore-based concurrency control (max_concurrent=5)
- No adaptive rate limiting based on API response patterns
- Missing performance monitoring and alerting
- No intelligent backoff strategies for different error types

## Dependencies
**Requires Stream A**: Circuit breaker patterns and network resilience infrastructure must be available for advanced rate limiting strategies.

## Implementation Tasks

### Task E1: Adaptive Rate Limiting System (1.5 days)

**File**: `src/autodocs_mcp/core/rate_limiter.py`

**Implementation**:
```python
"""Adaptive rate limiting system for PyPI API interactions."""

import asyncio
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional, Tuple
import httpx
from structlog import get_logger

logger = get_logger(__name__)

class RateLimitStrategy(Enum):
    """Rate limiting strategies based on API behavior."""
    CONSERVATIVE = "conservative"  # Start slow, increase gradually
    AGGRESSIVE = "aggressive"     # Start fast, back off on errors
    ADAPTIVE = "adaptive"         # Learn from API response patterns

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting behavior."""
    strategy: RateLimitStrategy = RateLimitStrategy.ADAPTIVE
    initial_rate: float = 2.0  # requests per second
    max_rate: float = 10.0     # maximum requests per second
    min_rate: float = 0.5      # minimum requests per second
    burst_size: int = 5        # maximum burst size
    backoff_factor: float = 2.0
    recovery_factor: float = 1.2
    window_size: int = 60      # sliding window in seconds

class APIMetrics:
    """Track API performance metrics for rate limiting decisions."""

    def __init__(self, window_size: int = 60):
        self.window_size = window_size
        self.request_times: deque = deque()
        self.response_times: deque = deque()
        self.error_times: deque = deque()
        self.rate_limit_times: deque = deque()

    def record_request(self, response_time: float):
        """Record a successful request."""
        now = time.time()
        self.request_times.append(now)
        self.response_times.append(response_time)
        self._cleanup_old_entries()

    def record_error(self, error_type: str):
        """Record an error."""
        now = time.time()
        self.error_times.append((now, error_type))
        self._cleanup_old_entries()

    def record_rate_limit(self, retry_after: Optional[int] = None):
        """Record a rate limit response."""
        now = time.time()
        self.rate_limit_times.append((now, retry_after))
        self._cleanup_old_entries()

    def _cleanup_old_entries(self):
        """Remove entries older than the window size."""
        cutoff = time.time() - self.window_size

        while self.request_times and self.request_times[0] < cutoff:
            self.request_times.popleft()

        while self.response_times and self.response_times[0] < cutoff:
            self.response_times.popleft()

        while self.error_times and self.error_times[0][0] < cutoff:
            self.error_times.popleft()

        while self.rate_limit_times and self.rate_limit_times[0][0] < cutoff:
            self.rate_limit_times.popleft()

    @property
    def current_rate(self) -> float:
        """Calculate current request rate (requests per second)."""
        if not self.request_times:
            return 0.0
        return len(self.request_times) / self.window_size

    @property
    def average_response_time(self) -> float:
        """Calculate average response time."""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)

    @property
    def error_rate(self) -> float:
        """Calculate error rate (errors per second)."""
        if not self.error_times:
            return 0.0
        return len(self.error_times) / self.window_size

    @property
    def recent_rate_limits(self) -> int:
        """Count recent rate limit responses."""
        return len(self.rate_limit_times)

class AdaptiveRateLimiter:
    """Intelligent rate limiter that adapts to API behavior."""

    def __init__(self, config: RateLimitConfig | None = None):
        self.config = config or RateLimitConfig()
        self.metrics = APIMetrics(self.config.window_size)
        self.current_rate = self.config.initial_rate
        self.tokens = self.config.burst_size
        self.last_refill = time.time()
        self._lock = asyncio.Lock()

        # Adaptive learning state
        self.consecutive_successes = 0
        self.consecutive_errors = 0
        self.last_adjustment = time.time()

    async def acquire(self) -> bool:
        """Acquire permission to make a request."""
        async with self._lock:
            await self._refill_tokens()

            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                # Calculate wait time for next token
                wait_time = 1.0 / self.current_rate
                logger.debug("Rate limit wait", wait_time=wait_time, current_rate=self.current_rate)
                await asyncio.sleep(wait_time)
                self.tokens = max(0, self.tokens - 1)
                return True

    async def _refill_tokens(self):
        """Refill token bucket based on current rate."""
        now = time.time()
        time_elapsed = now - self.last_refill

        # Add tokens based on current rate
        tokens_to_add = time_elapsed * self.current_rate
        self.tokens = min(self.config.burst_size, self.tokens + tokens_to_add)
        self.last_refill = now

    def record_success(self, response_time: float):
        """Record a successful request and adapt rate if needed."""
        self.metrics.record_request(response_time)
        self.consecutive_successes += 1
        self.consecutive_errors = 0

        # Adaptive rate adjustment
        self._adjust_rate_on_success()

    def record_error(self, error_type: str, response: httpx.Response | None = None):
        """Record an error and adapt rate if needed."""
        self.metrics.record_error(error_type)
        self.consecutive_errors += 1
        self.consecutive_successes = 0

        # Handle rate limiting responses
        if response and response.status_code == 429:
            retry_after = self._extract_retry_after(response)
            self.metrics.record_rate_limit(retry_after)
            self._handle_rate_limit_response(retry_after)
        else:
            # Handle other errors
            self._adjust_rate_on_error(error_type)

    def _adjust_rate_on_success(self):
        """Increase rate after consecutive successes."""
        if self.consecutive_successes >= 10:  # After 10 successful requests
            if time.time() - self.last_adjustment > 30:  # Don't adjust too frequently
                old_rate = self.current_rate
                self.current_rate = min(
                    self.config.max_rate,
                    self.current_rate * self.config.recovery_factor
                )

                if self.current_rate != old_rate:
                    logger.info("Increased request rate",
                               old_rate=old_rate,
                               new_rate=self.current_rate,
                               reason="consecutive_successes")
                    self.last_adjustment = time.time()
                    self.consecutive_successes = 0

    def _adjust_rate_on_error(self, error_type: str):
        """Decrease rate after errors."""
        if self.consecutive_errors >= 3:  # After 3 consecutive errors
            old_rate = self.current_rate
            self.current_rate = max(
                self.config.min_rate,
                self.current_rate / self.config.backoff_factor
            )

            if self.current_rate != old_rate:
                logger.warning("Decreased request rate",
                             old_rate=old_rate,
                             new_rate=self.current_rate,
                             reason=f"consecutive_errors_{error_type}")
                self.last_adjustment = time.time()
                self.consecutive_errors = 0

    def _handle_rate_limit_response(self, retry_after: Optional[int]):
        """Handle explicit rate limit response from API."""
        if retry_after:
            # Respect the API's retry-after header
            backoff_rate = 1.0 / (retry_after + 5)  # Add 5s buffer
            self.current_rate = max(self.config.min_rate, backoff_rate)
        else:
            # No retry-after header, use aggressive backoff
            self.current_rate = max(
                self.config.min_rate,
                self.current_rate / (self.config.backoff_factor * 2)
            )

        logger.warning("Rate limited by API",
                      new_rate=self.current_rate,
                      retry_after=retry_after)
        self.last_adjustment = time.time()

    def _extract_retry_after(self, response: httpx.Response) -> Optional[int]:
        """Extract retry-after value from response headers."""
        retry_after = response.headers.get('retry-after')
        if retry_after:
            try:
                return int(retry_after)
            except ValueError:
                pass
        return None

    def get_stats(self) -> Dict[str, float]:
        """Get current rate limiter statistics."""
        return {
            "current_rate": self.current_rate,
            "available_tokens": self.tokens,
            "metrics": {
                "current_rate": self.metrics.current_rate,
                "average_response_time": self.metrics.average_response_time,
                "error_rate": self.metrics.error_rate,
                "recent_rate_limits": self.metrics.recent_rate_limits,
            }
        }

class PerformanceMonitor:
    """Monitor and alert on performance issues."""

    def __init__(self):
        self.request_metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.alert_thresholds = {
            "response_time": 5.0,  # seconds
            "error_rate": 0.1,     # 10% error rate
            "cache_hit_rate": 0.7, # 70% cache hit rate
        }

    def record_request(self, endpoint: str, response_time: float, success: bool, from_cache: bool = False):
        """Record request metrics."""
        self.request_metrics[endpoint].append({
            "timestamp": time.time(),
            "response_time": response_time,
            "success": success,
            "from_cache": from_cache
        })

        # Check for performance issues
        self._check_performance_alerts(endpoint)

    def _check_performance_alerts(self, endpoint: str):
        """Check if performance metrics exceed thresholds."""
        metrics = self.request_metrics[endpoint]

        if len(metrics) < 10:  # Need minimum sample size
            return

        # Check average response time
        recent_requests = list(metrics)[-10:]  # Last 10 requests
        avg_response_time = sum(m["response_time"] for m in recent_requests) / len(recent_requests)

        if avg_response_time > self.alert_thresholds["response_time"]:
            logger.warning("High response time detected",
                          endpoint=endpoint,
                          avg_response_time=avg_response_time,
                          threshold=self.alert_thresholds["response_time"])

        # Check error rate
        error_count = sum(1 for m in recent_requests if not m["success"])
        error_rate = error_count / len(recent_requests)

        if error_rate > self.alert_thresholds["error_rate"]:
            logger.warning("High error rate detected",
                          endpoint=endpoint,
                          error_rate=error_rate,
                          threshold=self.alert_thresholds["error_rate"])

        # Check cache hit rate
        cache_hits = sum(1 for m in recent_requests if m["from_cache"])
        cache_hit_rate = cache_hits / len(recent_requests)

        if cache_hit_rate < self.alert_thresholds["cache_hit_rate"]:
            logger.info("Low cache hit rate",
                       endpoint=endpoint,
                       cache_hit_rate=cache_hit_rate,
                       threshold=self.alert_thresholds["cache_hit_rate"])

    def get_performance_stats(self) -> Dict[str, Dict]:
        """Get performance statistics for all endpoints."""
        stats = {}

        for endpoint, metrics in self.request_metrics.items():
            if not metrics:
                continue

            recent_metrics = list(metrics)[-50:]  # Last 50 requests

            response_times = [m["response_time"] for m in recent_metrics]
            success_count = sum(1 for m in recent_metrics if m["success"])
            cache_hits = sum(1 for m in recent_metrics if m["from_cache"])

            stats[endpoint] = {
                "total_requests": len(recent_metrics),
                "success_rate": success_count / len(recent_metrics),
                "error_rate": (len(recent_metrics) - success_count) / len(recent_metrics),
                "cache_hit_rate": cache_hits / len(recent_metrics),
                "avg_response_time": sum(response_times) / len(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
            }

        return stats
```

### Task E2: Enhanced Network Client with Performance Monitoring (1 day)

**File**: `src/autodocs_mcp/core/network_resilience.py` (enhancement)

**Implementation**:
```python
# Add to existing NetworkResilientClient class

class NetworkResilientClient:
    """Enhanced client with rate limiting and performance monitoring."""

    def __init__(self,
                 retry_config: RetryConfig | None = None,
                 rate_limiter: AdaptiveRateLimiter | None = None):
        self.retry_config = retry_config or RetryConfig()
        self.rate_limiter = rate_limiter or AdaptiveRateLimiter()
        self.performance_monitor = PerformanceMonitor()
        self._client: httpx.AsyncClient | None = None
        self._circuit_breaker = CircuitBreaker()

    async def get_with_retry(self, url: str, **kwargs) -> httpx.Response:
        """Make GET request with rate limiting and performance monitoring."""
        # Acquire rate limit permission
        await self.rate_limiter.acquire()

        start_time = time.time()
        success = False
        response = None

        for attempt in range(1, self.retry_config.max_attempts + 1):
            try:
                # Check circuit breaker
                if self._circuit_breaker.is_open():
                    raise NetworkError("Circuit breaker is open")

                logger.debug("Making HTTP request", url=url, attempt=attempt)
                response = await self._client.get(url, **kwargs)

                # Record timing
                request_time = time.time() - start_time

                # Handle different status codes
                if response.status_code == 404:
                    # Not a rate limiting issue, record success
                    self.rate_limiter.record_success(request_time)
                    self.performance_monitor.record_request(url, request_time, False)
                    raise PackageNotFoundError(f"Package not found: {url}")

                if response.status_code == 429:
                    # Rate limited
                    self.rate_limiter.record_error("rate_limit", response)
                    self.performance_monitor.record_request(url, request_time, False)

                    if attempt == self.retry_config.max_attempts:
                        raise NetworkError(f"Rate limited after {attempt} attempts")

                    # Wait for retry with respect to rate limiting
                    await self._wait_for_rate_limit_retry(response)
                    continue

                response.raise_for_status()

                # Success
                success = True
                request_time = time.time() - start_time
                self._circuit_breaker.record_success()
                self.rate_limiter.record_success(request_time)
                self.performance_monitor.record_request(url, request_time, True)

                return response

            except httpx.TimeoutException as e:
                self._circuit_breaker.record_failure()
                self.rate_limiter.record_error("timeout")

                if attempt == self.retry_config.max_attempts:
                    request_time = time.time() - start_time
                    self.performance_monitor.record_request(url, request_time, False)
                    raise NetworkError(f"Request timeout after {attempt} attempts") from e

                await self._wait_for_retry(attempt)

            except httpx.HTTPStatusError as e:
                self._circuit_breaker.record_failure()
                self.rate_limiter.record_error("http_error", e.response)

                # Don't retry 4xx errors except 429 (already handled above)
                if 400 <= e.response.status_code < 500:
                    request_time = time.time() - start_time
                    self.performance_monitor.record_request(url, request_time, False)
                    raise NetworkError(f"HTTP {e.response.status_code}: {e.response.text}")

                if attempt == self.retry_config.max_attempts:
                    request_time = time.time() - start_time
                    self.performance_monitor.record_request(url, request_time, False)
                    raise NetworkError(f"HTTP error after {attempt} attempts") from e

                await self._wait_for_retry(attempt)

            except httpx.RequestError as e:
                self._circuit_breaker.record_failure()
                self.rate_limiter.record_error("network_error")

                if attempt == self.retry_config.max_attempts:
                    request_time = time.time() - start_time
                    self.performance_monitor.record_request(url, request_time, False)
                    raise NetworkError(f"Network error after {attempt} attempts: {e}") from e

                await self._wait_for_retry(attempt)

    async def _wait_for_rate_limit_retry(self, response: httpx.Response):
        """Wait for rate limit retry with respect to retry-after header."""
        retry_after = response.headers.get('retry-after')

        if retry_after:
            try:
                wait_time = int(retry_after) + 2  # Add 2s buffer
                logger.info("Rate limited, waiting", retry_after=retry_after, wait_time=wait_time)
                await asyncio.sleep(wait_time)
                return
            except ValueError:
                pass

        # Fallback to adaptive rate limiter wait time
        wait_time = 1.0 / self.rate_limiter.current_rate + 5  # Add 5s buffer
        logger.info("Rate limited, using adaptive wait", wait_time=wait_time)
        await asyncio.sleep(wait_time)

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics."""
        return {
            "rate_limiter": self.rate_limiter.get_stats(),
            "circuit_breaker": {
                "state": self._circuit_breaker._state,
                "failure_count": self._circuit_breaker._failure_count,
            },
            "performance": self.performance_monitor.get_performance_stats()
        }
```

### Task E3: Add Performance Monitoring to MCP Tools (0.5 days)

**File**: `src/autodocs_mcp/main.py` (enhancement)

**Implementation**:
```python
# Add new MCP tool for performance monitoring

@mcp.tool
@standardized_response(StandardMCPResponse)
async def get_performance_stats() -> dict[str, Any]:
    """
    Get performance statistics and metrics.

    Returns:
        Performance metrics including request rates, response times, error rates
    """
    if not cache_manager:
        raise AutoDocsError("Service not initialized")

    stats = {
        "cache_stats": await cache_manager.get_cache_stats(),
        "performance_metrics": {},
        "rate_limiting": {},
        "system_health": "healthy"
    }

    # Get network client performance stats if available
    if hasattr(cache_manager, '_get_network_stats'):
        network_stats = await cache_manager._get_network_stats()
        stats["performance_metrics"] = network_stats.get("performance", {})
        stats["rate_limiting"] = network_stats.get("rate_limiter", {})

    # Determine system health
    performance = stats["performance_metrics"]
    if performance:
        # Check if any endpoint has high error rate
        high_error_endpoints = [
            endpoint for endpoint, metrics in performance.items()
            if metrics.get("error_rate", 0) > 0.2  # 20% error rate threshold
        ]

        if high_error_endpoints:
            stats["system_health"] = "degraded"
            stats["health_issues"] = [
                f"High error rate on {endpoint}" for endpoint in high_error_endpoints
            ]

    return stats

# Enhance existing tools to include performance tracking
@mcp.tool
@standardized_response(GetPackageDocsResponse)
async def get_package_docs(package_name: str,
                          version_constraint: str | None = None,
                          query: str | None = None) -> GetPackageDocsResponse:
    """Enhanced with performance monitoring."""
    start_time = time.time()

    # ... existing implementation ...

    # Add performance metadata to response
    response.metadata.performance_metrics = {
        "cache_hit": from_cache,
        "dependencies_fetched": len(dependency_docs),
        "total_requests": 1 + len(dependency_docs)
    }

    return response
```

## Testing Requirements

### Unit Tests
- Test adaptive rate limiting with various API response patterns
- Test performance monitoring and alerting thresholds
- Test circuit breaker integration with rate limiting
- Test rate adjustment algorithms

### Load Tests
- Test behavior under high concurrent request load
- Test rate limiting effectiveness with PyPI API
- Test performance monitoring accuracy under stress

## Example Performance Metrics Output

```json
{
  "status": "success",
  "success": true,
  "data": {
    "cache_stats": {
      "total_entries": 42,
      "cache_size": "15.6 MB",
      "hit_rate": 0.78
    },
    "rate_limiting": {
      "current_rate": 3.5,
      "available_tokens": 4.2,
      "metrics": {
        "current_rate": 3.2,
        "average_response_time": 0.45,
        "error_rate": 0.02,
        "recent_rate_limits": 0
      }
    },
    "performance_metrics": {
      "https://pypi.org/pypi/requests/json": {
        "total_requests": 25,
        "success_rate": 0.96,
        "error_rate": 0.04,
        "cache_hit_rate": 0.80,
        "avg_response_time": 0.42,
        "min_response_time": 0.15,
        "max_response_time": 1.23
      }
    },
    "system_health": "healthy"
  }
}
```

## Acceptance Criteria

- [ ] Rate limiting adapts to API response patterns automatically
- [ ] Performance monitoring tracks key metrics and alerts on issues
- [ ] System maintains responsiveness under various load conditions
- [ ] Rate limiting respects API retry-after headers
- [ ] Performance statistics available through MCP tool
- [ ] Circuit breaker prevents cascade failures during performance issues
- [ ] Intelligent backoff strategies reduce API pressure during errors

## Dependencies
- **Stream A (Network Resilience)**: Required for circuit breaker patterns and retry infrastructure

## Estimated Effort: 2 days
- Task E1: 1.5 days (adaptive rate limiting system)
- Task E2: 1 day (enhanced network client)
- Task E3: 0.5 days (MCP tool integration)
