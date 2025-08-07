# Stream A: Network Resilience Implementation

## Overview
Implement robust network error handling with retry patterns, circuit breakers, and exponential backoff for all external API calls.

## Current State
- Basic timeout configuration (30s) in `config.py`
- Simple exception raising in `version_resolver.py:34-48`
- No retry logic or circuit breaker patterns
- Network errors bubble up without handling

## Implementation Tasks

### Task A1: Retry Logic with Exponential Backoff (1 day)

**File**: `src/autodocs_mcp/core/network_resilience.py`

**Implementation**:
```python
import asyncio
import random
from typing import Any, Awaitable, Callable, TypeVar
from dataclasses import dataclass
import httpx
from structlog import get_logger

logger = get_logger(__name__)
T = TypeVar('T')

@dataclass
class RetryConfig:
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True

class NetworkResilientClient:
    """HTTP client with built-in retry logic and circuit breaker."""

    def __init__(self, retry_config: RetryConfig | None = None):
        self.retry_config = retry_config or RetryConfig()
        self._client: httpx.AsyncClient | None = None
        self._circuit_breaker = CircuitBreaker()

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            follow_redirects=True
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    async def get_with_retry(self, url: str, **kwargs) -> httpx.Response:
        """Make GET request with retry logic."""

        for attempt in range(1, self.retry_config.max_attempts + 1):
            try:
                # Check circuit breaker
                if self._circuit_breaker.is_open():
                    raise NetworkError("Circuit breaker is open")

                logger.debug("Making HTTP request", url=url, attempt=attempt)
                response = await self._client.get(url, **kwargs)

                # Success - reset circuit breaker
                self._circuit_breaker.record_success()

                if response.status_code == 404:
                    raise PackageNotFoundError(f"Package not found: {url}")

                response.raise_for_status()
                return response

            except httpx.TimeoutException as e:
                self._circuit_breaker.record_failure()
                logger.warning("Request timeout", url=url, attempt=attempt)

                if attempt == self.retry_config.max_attempts:
                    raise NetworkError(f"Request timeout after {attempt} attempts") from e

                await self._wait_for_retry(attempt)

            except httpx.HTTPStatusError as e:
                self._circuit_breaker.record_failure()

                # Don't retry 4xx errors except 429 (rate limit)
                if 400 <= e.response.status_code < 500 and e.response.status_code != 429:
                    raise NetworkError(f"HTTP {e.response.status_code}: {e.response.text}")

                logger.warning("HTTP error", url=url, status=e.response.status_code, attempt=attempt)

                if attempt == self.retry_config.max_attempts:
                    raise NetworkError(f"HTTP error after {attempt} attempts") from e

                await self._wait_for_retry(attempt)

            except httpx.RequestError as e:
                self._circuit_breaker.record_failure()
                logger.warning("Network error", url=url, error=str(e), attempt=attempt)

                if attempt == self.retry_config.max_attempts:
                    raise NetworkError(f"Network error after {attempt} attempts: {e}") from e

                await self._wait_for_retry(attempt)

    async def _wait_for_retry(self, attempt: int):
        """Calculate and wait for retry delay with exponential backoff."""
        delay = min(
            self.retry_config.base_delay * (self.retry_config.exponential_base ** (attempt - 1)),
            self.retry_config.max_delay
        )

        if self.retry_config.jitter:
            delay *= (0.5 + random.random() * 0.5)  # Add ±50% jitter

        logger.debug("Waiting before retry", delay=delay, attempt=attempt)
        await asyncio.sleep(delay)

class CircuitBreaker:
    """Simple circuit breaker to prevent cascade failures."""

    def __init__(self, failure_threshold: int = 5, reset_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self._failure_count = 0
        self._last_failure_time = 0.0
        self._state = "closed"  # closed, open, half_open

    def is_open(self) -> bool:
        if self._state == "open":
            if time.time() - self._last_failure_time > self.reset_timeout:
                self._state = "half_open"
                return False
            return True
        return False

    def record_success(self):
        self._failure_count = 0
        self._state = "closed"

    def record_failure(self):
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._failure_count >= self.failure_threshold:
            self._state = "open"
            logger.warning("Circuit breaker opened", failure_count=self._failure_count)
```

### Task A2: Update Version Resolver (0.5 days)

**File**: `src/autodocs_mcp/core/version_resolver.py`

**Changes**:
```python
# Replace lines 30-48 with resilient client usage
async def resolve_version(self, package_name: str, constraint: str | None = None) -> str:
    """Resolve version with network resilience."""

    async with NetworkResilientClient() as client:
        try:
            response = await client.get_with_retry(
                f"https://pypi.org/pypi/{package_name}/json",
                headers={"Accept": "application/json"}
            )

            data = response.json()
            latest_version = data["info"]["version"]

            logger.info("Resolved version",
                       package=package_name,
                       constraint=constraint,
                       resolved=latest_version)

            return latest_version

        except PackageNotFoundError:
            logger.error("Package not found", package=package_name)
            raise
        except NetworkError as e:
            logger.error("Failed to resolve version",
                        package=package_name,
                        error=str(e))
            raise
```

### Task A3: Update Documentation Fetcher (0.5 days)

**File**: `src/autodocs_mcp/core/doc_fetcher.py`

**Changes**:
```python
# Replace PyPIDocumentationFetcher to use NetworkResilientClient
class PyPIDocumentationFetcher(DocumentationFetcherInterface):
    def __init__(self, semaphore: asyncio.Semaphore | None = None):
        self.config = get_config()
        self.semaphore = semaphore or asyncio.Semaphore(self.config.max_concurrent)
        self._resilient_client: NetworkResilientClient | None = None

    async def __aenter__(self) -> "PyPIDocumentationFetcher":
        self._resilient_client = NetworkResilientClient()
        await self._resilient_client.__aenter__()
        return self

    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        """Fetch with network resilience."""
        async with self.semaphore:
            try:
                response = await self._resilient_client.get_with_retry(
                    f"https://pypi.org/pypi/{package_name}/json"
                )

                data = response.json()
                # ... rest of parsing logic unchanged

            except PackageNotFoundError:
                logger.error("Package not found on PyPI", package=package_name)
                raise
            except NetworkError as e:
                logger.error("Network error fetching package",
                           package=package_name, error=str(e))
                raise
```

## Testing Requirements

### Unit Tests
- Test retry logic with different failure scenarios
- Test exponential backoff timing calculations
- Test circuit breaker state transitions
- Mock network failures and verify behavior

### Integration Tests
- Test with real PyPI API (limited calls)
- Test timeout scenarios
- Test rate limiting responses (429 status)

## Acceptance Criteria

- [ ] All network calls use retry logic with exponential backoff
- [ ] Circuit breaker prevents cascade failures
- [ ] Proper logging of retry attempts and failures
- [ ] Network errors provide context and suggestions
- [ ] No hanging requests (proper timeout handling)
- [ ] Graceful degradation when network is completely unavailable

## Dependencies
- None - this stream can start immediately
- Creates foundation for Stream C (Documentation Fetching Resilience)

## Estimated Effort: 2 days
- Task A1: 1 day (core implementation)
- Task A2: 0.5 days (version resolver update)
- Task A3: 0.5 days (doc fetcher update)
