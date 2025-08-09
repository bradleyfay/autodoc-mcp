# Phase 3: Integration Testing Plan

## Overview
Comprehensive testing strategy for graceful degradation features across all work streams, ensuring robust integration and real-world reliability.

## Testing Philosophy
- **Test failure scenarios as thoroughly as success scenarios**
- **Validate partial success behavior extensively**
- **Ensure graceful degradation doesn't impact performance**
- **Test integration points between work streams**

## Integration Test Phases

### Phase 3A: Cross-Stream Integration (Mid-development)
**Timing**: After Stream A and Stream B are complete
**Duration**: 0.5 days
**Purpose**: Validate early integration between network resilience and error messaging

### Phase 3B: Full Integration Testing (End of development)
**Timing**: After all streams are complete
**Duration**: 1 day
**Purpose**: Comprehensive testing of all graceful degradation features

## Test Categories

### Category 1: Network Resilience Integration Tests

**File**: `tests/integration/test_network_resilience.py`

**Test Scenarios**:
```python
"""Network resilience integration tests."""

import pytest
import asyncio
from unittest.mock import patch, AsyncMock
import httpx

from autodocs_mcp.core.network_resilience import NetworkResilientClient
from autodocs_mcp.core.rate_limiter import AdaptiveRateLimiter
from autodocs_mcp.exceptions import NetworkError, PackageNotFoundError

class TestNetworkResilienceIntegration:
    """Test network resilience with rate limiting and error formatting."""

    @pytest.mark.asyncio
    async def test_retry_with_rate_limiting(self):
        """Test that retries respect rate limiting."""
        rate_limiter = AdaptiveRateLimiter()

        async with NetworkResilientClient(rate_limiter=rate_limiter) as client:
            # Mock consecutive failures followed by success
            with patch.object(client._client, 'get') as mock_get:
                # First two calls fail with timeout
                mock_get.side_effect = [
                    httpx.TimeoutException("Timeout"),
                    httpx.TimeoutException("Timeout"),
                    httpx.Response(200, json={"info": {"name": "test", "version": "1.0.0"}})
                ]

                # Should succeed on third attempt with proper rate limiting
                response = await client.get_with_retry("https://pypi.org/pypi/test/json")
                assert response.status_code == 200

                # Rate should be decreased due to errors
                assert rate_limiter.current_rate < rate_limiter.config.initial_rate

    @pytest.mark.asyncio
    async def test_circuit_breaker_with_rate_limiting(self):
        """Test circuit breaker integration with rate limiting."""
        rate_limiter = AdaptiveRateLimiter()

        async with NetworkResilientClient(rate_limiter=rate_limiter) as client:
            # Trigger circuit breaker with multiple failures
            with patch.object(client._client, 'get') as mock_get:
                mock_get.side_effect = httpx.RequestError("Connection failed")

                # Should fail multiple requests and open circuit breaker
                for _ in range(6):  # Exceed failure threshold
                    with pytest.raises(NetworkError):
                        await client.get_with_retry("https://pypi.org/pypi/test/json")

                # Circuit breaker should be open
                assert client._circuit_breaker._state == "open"

                # Rate should be at minimum
                assert rate_limiter.current_rate == rate_limiter.config.min_rate

    @pytest.mark.asyncio
    async def test_rate_limit_response_handling(self):
        """Test handling of 429 responses with retry-after."""
        async with NetworkResilientClient() as client:
            with patch.object(client._client, 'get') as mock_get:
                # Mock 429 response with retry-after header
                rate_limit_response = httpx.Response(
                    429,
                    headers={"retry-after": "5"},
                    text="Rate limited"
                )
                success_response = httpx.Response(
                    200,
                    json={"info": {"name": "test", "version": "1.0.0"}}
                )

                mock_get.side_effect = [rate_limit_response, success_response]

                # Should handle rate limit and succeed on retry
                start_time = time.time()
                response = await client.get_with_retry("https://pypi.org/pypi/test/json")
                elapsed = time.time() - start_time

                assert response.status_code == 200
                assert elapsed >= 5.0  # Should wait for retry-after duration
```

### Category 2: Error Message Integration Tests

**File**: `tests/integration/test_error_messaging.py`

**Test Scenarios**:
```python
"""Error messaging integration tests."""

import pytest
from pathlib import Path

from autodocs_mcp.core.dependency_parser import PyProjectParser
from autodocs_mcp.core.error_formatter import ErrorFormatter, ResponseFormatter
from autodocs_mcp.models.responses import ScanDependenciesResponse

class TestErrorMessagingIntegration:
    """Test error message formatting across different failure scenarios."""

    @pytest.mark.asyncio
    async def test_malformed_pyproject_error_formatting(self, tmp_path):
        """Test error formatting for various pyproject.toml issues."""
        # Create malformed pyproject.toml
        malformed_content = """
[project]
name = "test-project"
dependencies = [
    "requests>=2.0.0",
    "invalid-package-name==",  # Invalid version
    "numpy[extra1,extra2",     # Unclosed bracket
    "",                        # Empty dependency
    "scipy@#$%",              # Invalid package name
]
"""
        pyproject_path = tmp_path / "pyproject.toml"
        pyproject_path.write_text(malformed_content)

        parser = PyProjectParser()
        result = await parser.parse_project(tmp_path)

        # Format response using ResponseFormatter
        response = ScanDependenciesResponse.from_scan_result(result)
        formatted = response.finalize()

        # Verify error messages are user-friendly
        assert formatted["success"]  # Should succeed with valid deps
        assert formatted["status"] == "partial_success"
        assert len(formatted["errors"]) == 4  # Four malformed dependencies

        # Check specific error messages
        error_messages = [err["message"] for err in formatted["errors"]]
        suggestions = formatted["suggestions"]

        assert any("invalid version specifier" in msg for msg in error_messages)
        assert any("Unclosed bracket" in msg for msg in error_messages)
        assert any("Empty dependency" in msg for msg in error_messages)
        assert any("Invalid package name" in msg for msg in error_messages)

        # Verify suggestions are actionable
        assert len(suggestions) == 4
        assert all(len(suggestion) > 10 for suggestion in suggestions)  # Non-trivial suggestions

    @pytest.mark.asyncio
    async def test_network_error_message_formatting(self):
        """Test network error formatting with context."""
        from autodocs_mcp.exceptions import NetworkError, PackageNotFoundError

        # Test PackageNotFoundError formatting
        error = PackageNotFoundError("Package 'nonexistent-pkg' not found")
        formatted = ErrorFormatter.format_exception(
            error,
            {"package": "nonexistent-pkg", "suggestions": ["nonexistent", "pkg-nonexistent"]}
        )

        assert "not found" in formatted.message.lower()
        assert formatted.suggestion is not None
        assert "nonexistent" in formatted.suggestion
        assert formatted.recoverable is True

        # Test NetworkError formatting
        network_error = NetworkError("Connection timeout after 3 attempts")
        formatted_net = ErrorFormatter.format_exception(
            network_error,
            {"package": "requests", "operation": "documentation_fetch"}
        )

        assert "network error" in formatted_net.message.lower()
        assert "connection" in formatted_net.suggestion.lower()
        assert formatted_net.recoverable is True
```

### Category 3: Documentation Fetching Integration Tests

**File**: `tests/integration/test_doc_fetching.py`

**Test Scenarios**:
```python
"""Documentation fetching integration tests."""

import pytest
from unittest.mock import patch, AsyncMock
import httpx

from autodocs_mcp.core.doc_fetcher import PyPIDocumentationFetcher
from autodocs_mcp.core.cache_manager import FileCacheManager
from autodocs_mcp.exceptions import NetworkError

class TestDocFetchingIntegration:
    """Test documentation fetching with graceful degradation."""

    @pytest.mark.asyncio
    async def test_partial_dependency_fetch_success(self):
        """Test fetching dependencies when some fail."""
        fetcher = PyPIDocumentationFetcher()

        # Mock responses for different packages
        package_responses = {
            "requests": {"info": {"name": "requests", "version": "2.28.0", "summary": "HTTP library"}},
            "urllib3": {"info": {"name": "urllib3", "version": "1.26.0", "summary": "HTTP client"}},
            "certifi": None,  # This will fail
        }

        async with fetcher:
            with patch.object(fetcher._resilient_client, 'get_with_retry') as mock_get:
                def mock_response(url):
                    package_name = url.split('/')[-2]  # Extract package name from URL
                    if package_responses[package_name] is None:
                        raise NetworkError(f"Failed to fetch {package_name}")
                    return httpx.Response(200, json=package_responses[package_name])

                mock_get.side_effect = mock_response

                # Fetch multiple packages
                results = await fetcher.fetch_multiple_packages_safe(
                    ["requests", "urllib3", "certifi"]
                )

                # Should have partial success
                assert len(results) == 3
                assert results["requests"].success
                assert results["urllib3"].success
                assert not results["certifi"].success

                # Failed package should have error information
                assert len(results["certifi"].errors) > 0
                assert "Failed to fetch certifi" in results["certifi"].errors[0].message

    @pytest.mark.asyncio
    async def test_cache_corruption_recovery(self, tmp_path):
        """Test cache corruption detection and recovery."""
        cache_manager = FileCacheManager(cache_dir=tmp_path)

        # Create a corrupted cache file
        corrupted_file = tmp_path / "requests-2.28.0.json"
        corrupted_file.write_text("{ invalid json")

        # Attempt to retrieve from cache
        entry, errors = cache_manager.get_cached_entry_safe("requests-2.28.0")

        # Should handle corruption gracefully
        assert entry is None
        assert len(errors) == 1
        assert "corrupted" in errors[0].message.lower()
        assert errors[0].severity.value == "warning"
        assert not corrupted_file.exists()  # File should be removed

    @pytest.mark.asyncio
    async def test_mcp_tool_partial_success_response(self):
        """Test MCP tool returns proper partial success response."""
        from autodocs_mcp.main import get_package_docs

        # Mock cache manager to return partial results
        with patch('autodocs_mcp.main.cache_manager') as mock_cache:
            # Main package succeeds, dependency fails
            mock_cache.resolve_and_cache_safe.return_value = (
                MockPackageInfo("fastapi", "0.104.1"),  # package_info
                False,  # from_cache
                [MockFormattedError("Network timeout fetching dependency 'starlette'")]  # errors
            )

            result = await get_package_docs("fastapi")

            assert result["status"] == "partial_success"
            assert result["success"] is True
            assert len(result["errors"]) == 1
            assert "starlette" in result["errors"][0]["message"]
            assert len(result["suggestions"]) > 0
```

### Category 4: End-to-End Integration Tests

**File**: `tests/integration/test_e2e_graceful_degradation.py`

**Test Scenarios**:
```python
"""End-to-end graceful degradation tests."""

import pytest
from unittest.mock import patch, AsyncMock
import asyncio

from autodocs_mcp.main import scan_dependencies, get_package_docs
from autodocs_mcp.models.responses import ResponseStatus

class TestE2EGracefulDegradation:
    """Test complete graceful degradation workflows."""

    @pytest.mark.asyncio
    async def test_complete_workflow_with_mixed_failures(self, tmp_path):
        """Test complete workflow from scanning to documentation with failures."""
        # Create a project with some valid and some invalid dependencies
        pyproject_content = """
[project]
name = "test-project"
dependencies = [
    "requests>=2.0.0",        # Valid, should work
    "nonexistent-package",    # Invalid, should fail gracefully
    "numpy",                  # Valid, but will simulate network failure
    "invalid==syntax",        # Invalid syntax
]
"""
        (tmp_path / "pyproject.toml").write_text(pyproject_content)

        # Mock network responses
        with patch('autodocs_mcp.main.parser') as mock_parser, \
             patch('autodocs_mcp.main.cache_manager') as mock_cache:

            # Set up parser mock
            mock_parser.parse_project.return_value = MockScanResult(
                dependencies=[
                    MockDependencySpec("requests", ">=2.0.0"),
                    MockDependencySpec("numpy", None)
                ],
                failed_deps=[
                    {"dependency_string": "nonexistent-package", "error": "Invalid package", "source": "project"},
                    {"dependency_string": "invalid==syntax", "error": "Invalid syntax", "source": "project"}
                ]
            )

            # Test dependency scanning
            scan_result = await scan_dependencies(str(tmp_path))

            assert scan_result["status"] == "partial_success"
            assert scan_result["success"] is True
            assert len(scan_result["data"]["dependencies"]) == 2  # Two valid deps
            assert len(scan_result["errors"]) == 2  # Two invalid deps

            # Set up cache manager for doc fetching
            mock_cache.resolve_and_cache_safe.side_effect = [
                # requests: success
                (MockPackageInfo("requests", "2.28.0"), False, []),
                # numpy: network failure
                (None, False, [MockFormattedError("Network timeout")])
            ]

            # Test documentation fetching for valid package
            requests_docs = await get_package_docs("requests")
            assert requests_docs["status"] == "success"
            assert requests_docs["success"] is True

            # Test documentation fetching for failed package
            numpy_docs = await get_package_docs("numpy")
            assert numpy_docs["status"] == "failure"
            assert numpy_docs["success"] is False
            assert len(numpy_docs["errors"]) > 0

    @pytest.mark.asyncio
    async def test_concurrent_requests_with_rate_limiting(self):
        """Test concurrent documentation requests with rate limiting."""
        packages = ["requests", "numpy", "pandas", "scipy", "matplotlib"]

        with patch('autodocs_mcp.main.cache_manager') as mock_cache:
            # Simulate various response patterns
            mock_cache.resolve_and_cache_safe.side_effect = [
                (MockPackageInfo("requests", "2.28.0"), True, []),  # Cache hit
                (MockPackageInfo("numpy", "1.24.0"), False, []),   # Network success
                (None, False, [MockFormattedError("Rate limited")]),  # Rate limit
                (MockPackageInfo("scipy", "1.9.0"), False, []),    # Success after rate limit
                (None, False, [MockFormattedError("Timeout")]),    # Timeout
            ]

            # Make concurrent requests
            tasks = [get_package_docs(pkg) for pkg in packages]
            results = await asyncio.gather(*tasks)

            # Analyze results
            successes = sum(1 for r in results if r["success"])
            failures = sum(1 for r in results if not r["success"])

            assert successes >= 2  # At least requests and numpy should succeed
            assert failures >= 2   # At least pandas and matplotlib should fail

            # All responses should have proper error formatting
            for result in results:
                assert "status" in result
                assert result["status"] in [s.value for s in ResponseStatus]
                if not result["success"]:
                    assert len(result["errors"]) > 0
                    assert all("suggestion" in error for error in result["errors"])

    @pytest.mark.asyncio
    async def test_performance_monitoring_integration(self):
        """Test performance monitoring during failures."""
        from autodocs_mcp.main import get_performance_stats

        with patch('autodocs_mcp.main.cache_manager') as mock_cache:
            # Simulate performance data
            mock_cache.get_cache_stats.return_value = {"hit_rate": 0.75}
            mock_cache._get_network_stats.return_value = {
                "performance": {
                    "https://pypi.org/pypi/requests/json": {
                        "success_rate": 0.90,
                        "error_rate": 0.10,
                        "avg_response_time": 0.45
                    }
                },
                "rate_limiter": {
                    "current_rate": 2.5,
                    "available_tokens": 3.0
                }
            }

            stats = await get_performance_stats()

            assert stats["success"] is True
            assert "cache_stats" in stats["data"]
            assert "performance_metrics" in stats["data"]
            assert "rate_limiting" in stats["data"]
            assert "system_health" in stats["data"]

# Mock classes for testing
class MockPackageInfo:
    def __init__(self, name, version):
        self.name = name
        self.version = version

class MockFormattedError:
    def __init__(self, message):
        self.message = message
        self.suggestion = "Try again later"
        self.severity = MockSeverity("error")
        self.error_code = "test_error"
        self.recoverable = True
        self.context = {}

class MockSeverity:
    def __init__(self, value):
        self.value = value

class MockScanResult:
    def __init__(self, dependencies, failed_deps):
        self.dependencies = dependencies
        self.failed_deps = failed_deps
        self.warnings = []
        self.errors = []
        self.partial_success = len(failed_deps) > 0

class MockDependencySpec:
    def __init__(self, name, version_constraint):
        self.name = name
        self.version_constraint = version_constraint
```

## Test Execution Strategy

### Continuous Integration Setup
```yaml
# .github/workflows/phase3-integration-tests.yml
name: Phase 3 Integration Tests

on:
  push:
    paths:
      - 'src/autodocs_mcp/core/network_resilience.py'
      - 'src/autodocs_mcp/core/error_formatter.py'
      - 'src/autodocs_mcp/core/doc_fetcher.py'
      - 'src/autodocs_mcp/models/responses.py'
      - 'src/autodocs_mcp/core/rate_limiter.py'
  pull_request:
    paths:
      - 'src/autodocs_mcp/**'

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-asyncio pytest-mock

      - name: Run Phase 3A Integration Tests (Mid-development)
        run: |
          pytest tests/integration/test_network_resilience.py -v
          pytest tests/integration/test_error_messaging.py -v

      - name: Run Phase 3B Integration Tests (Full integration)
        run: |
          pytest tests/integration/test_doc_fetching.py -v
          pytest tests/integration/test_e2e_graceful_degradation.py -v
```

### Manual Test Scenarios

**Scenario 1: Real PyPI API Testing**
```bash
# Test with real PyPI API (limited calls)
export AUTODOCS_TEST_MODE=real_api
pytest tests/integration/test_real_api_graceful_degradation.py -v
```

**Scenario 2: Network Failure Simulation**
```bash
# Test with simulated network failures
export AUTODOCS_TEST_MODE=network_failure
pytest tests/integration/test_network_failure_scenarios.py -v
```

## Success Criteria

### Phase 3A (Mid-development)
- [ ] Network resilience integrates with error messaging
- [ ] Rate limiting works with retry logic
- [ ] Error messages are consistent across network failures
- [ ] Basic graceful degradation patterns work

### Phase 3B (Full integration)
- [ ] All MCP tools handle failures gracefully
- [ ] Partial success scenarios work end-to-end
- [ ] Performance monitoring captures graceful degradation metrics
- [ ] Complex failure scenarios (multiple simultaneous failures) handled correctly
- [ ] User experience remains good during various failure modes
- [ ] No crashes or undefined behavior under any test scenario

## Risk Mitigation

**Risk**: Integration testing reveals architectural issues
**Mitigation**: Phase 3A testing catches major issues early when they're easier to fix

**Risk**: Performance impact from extensive error handling
**Mitigation**: Performance benchmarks included in integration tests

**Risk**: Complex failure scenarios not covered
**Mitigation**: E2E tests simulate realistic complex scenarios

**Risk**: Real-world edge cases missed
**Mitigation**: Manual testing scenarios with real PyPI API and network conditions
