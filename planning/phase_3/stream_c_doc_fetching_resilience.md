# Stream C: Documentation Fetching Resilience

## Overview
Implement graceful degradation for documentation fetching operations, ensuring users get maximum useful information even when some packages fail to load or network issues occur.

## Current State
- Basic timeout handling in `doc_fetcher.py`
- No retry logic for documentation fetching
- Simple exception raising without partial results
- Missing concurrent error handling for dependency documentation

## Dependencies
**Requires Stream A**: Network resilience infrastructure must be implemented first for retry patterns and circuit breaker functionality.

## Implementation Tasks

### Task C1: Enhanced Documentation Fetcher with Partial Results (1.5 days)

**File**: `src/autodocs_mcp/core/doc_fetcher.py`

**Implementation**:
```python
"""Enhanced documentation fetcher with graceful degradation."""

import asyncio
from typing import Any, Dict, List, Tuple
from dataclasses import dataclass

from .network_resilience import NetworkResilientClient
from .error_formatter import ErrorFormatter, FormattedError
from ..exceptions import NetworkError, PackageNotFoundError

@dataclass
class DocFetchResult:
    """Result of documentation fetching with error tracking."""
    package_info: PackageInfo | None
    success: bool
    errors: List[FormattedError]
    warnings: List[str]
    from_cache: bool = False
    fetch_time: float = 0.0

class PyPIDocumentationFetcher(DocumentationFetcherInterface):
    """Enhanced fetcher with graceful degradation and error collection."""

    def __init__(self, semaphore: asyncio.Semaphore | None = None):
        self.config = get_config()
        self.semaphore = semaphore or asyncio.Semaphore(self.config.max_concurrent)
        self._resilient_client: NetworkResilientClient | None = None
        self._error_formatter = ErrorFormatter()

    async def fetch_package_info_safe(self, package_name: str) -> DocFetchResult:
        """Fetch package info with comprehensive error handling."""
        start_time = time.time()
        errors = []
        warnings = []
        package_info = None

        async with self.semaphore:
            try:
                logger.debug("Fetching package documentation", package=package_name)

                response = await self._resilient_client.get_with_retry(
                    f"https://pypi.org/pypi/{package_name}/json",
                    headers={"Accept": "application/json"}
                )

                data = response.json()
                package_info = self._parse_pypi_response(data, package_name)

                logger.info("Successfully fetched package info",
                           package=package_name,
                           version=package_info.version)

            except PackageNotFoundError as e:
                formatted_error = self._error_formatter.format_exception(
                    e, {"package": package_name}
                )
                errors.append(formatted_error)
                logger.warning("Package not found", package=package_name)

            except NetworkError as e:
                formatted_error = self._error_formatter.format_exception(
                    e, {"package": package_name}
                )
                errors.append(formatted_error)
                logger.error("Network error fetching package",
                           package=package_name, error=str(e))

            except Exception as e:
                formatted_error = self._error_formatter.format_exception(
                    e, {"package": package_name, "operation": "documentation_fetch"}
                )
                errors.append(formatted_error)
                logger.error("Unexpected error fetching package",
                           package=package_name, error=str(e))

        fetch_time = time.time() - start_time

        return DocFetchResult(
            package_info=package_info,
            success=package_info is not None,
            errors=errors,
            warnings=warnings,
            fetch_time=fetch_time
        )

    async def fetch_multiple_packages_safe(self,
                                         package_names: List[str]) -> Dict[str, DocFetchResult]:
        """Fetch multiple packages with individual error handling."""
        logger.info("Fetching multiple packages", count=len(package_names))

        # Create tasks for concurrent fetching
        tasks = [
            self.fetch_package_info_safe(package_name)
            for package_name in package_names
        ]

        # Wait for all tasks, collecting results regardless of individual failures
        results = await asyncio.gather(*tasks, return_exceptions=False)

        # Create result mapping
        fetch_results = {}
        for package_name, result in zip(package_names, results):
            fetch_results[package_name] = result

        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful

        logger.info("Completed batch documentation fetch",
                   total=len(package_names),
                   successful=successful,
                   failed=failed)

        return fetch_results

    def _parse_pypi_response(self, data: Dict[str, Any], package_name: str) -> PackageInfo:
        """Parse PyPI response with validation."""
        try:
            info = data["info"]

            # Validate required fields
            if not info.get("name"):
                raise ValueError("Missing package name in PyPI response")
            if not info.get("version"):
                raise ValueError("Missing version in PyPI response")

            return PackageInfo(
                name=info["name"],
                version=info["version"],
                summary=info.get("summary") or "",
                description=info.get("description") or "",
                author=info.get("author"),
                author_email=info.get("author_email"),
                license_=info.get("license"),
                home_page=info.get("home_page"),
                project_urls=info.get("project_urls") or {},
                classifiers=info.get("classifiers") or [],
                keywords=info.get("keywords"),
                requires_dist=info.get("requires_dist") or [],
            )

        except KeyError as e:
            raise ValueError(f"Malformed PyPI response: missing key {e}") from e
```

### Task C2: Enhanced Cache Manager with Error Recovery (1 day)

**File**: `src/autodocs_mcp/core/cache_manager.py`

**Implementation**:
```python
"""Enhanced cache manager with graceful degradation."""

from typing import Tuple, Optional, Dict, Any
import time
from pathlib import Path

from .doc_fetcher import DocFetchResult, PyPIDocumentationFetcher
from ..exceptions import CacheError
from ..models import PackageInfo, CacheEntry

class FileCacheManager:
    """Enhanced cache manager with error recovery and partial results."""

    async def resolve_and_cache_safe(self,
                                   package_name: str,
                                   version_constraint: str | None = None) -> Tuple[PackageInfo | None, bool, List[FormattedError]]:
        """Resolve and cache with comprehensive error handling."""
        errors = []
        from_cache = False
        package_info = None

        try:
            # Try to resolve version first
            if version_constraint:
                try:
                    resolved_version = await self.version_resolver.resolve_version(
                        package_name, version_constraint
                    )
                except Exception as e:
                    formatted_error = ErrorFormatter.format_exception(
                        e, {"package": package_name, "constraint": version_constraint}
                    )
                    errors.append(formatted_error)
                    # Try without version constraint as fallback
                    resolved_version = None
            else:
                resolved_version = None

            # Try cache first
            if resolved_version:
                cache_key = f"{package_name}-{resolved_version}"
                try:
                    cached_entry = self.get_cached_entry(cache_key)
                    if cached_entry:
                        package_info = cached_entry.package_info
                        from_cache = True
                        logger.debug("Retrieved from cache", package=package_name, version=resolved_version)
                        return package_info, from_cache, errors
                except CacheError as e:
                    logger.warning("Cache retrieval failed", package=package_name, error=str(e))
                    # Continue to fetch from network

            # Fetch from network
            async with PyPIDocumentationFetcher() as fetcher:
                fetch_result = await fetcher.fetch_package_info_safe(package_name)

                if fetch_result.success and fetch_result.package_info:
                    package_info = fetch_result.package_info

                    # Try to cache the result
                    try:
                        cache_key = f"{package_name}-{package_info.version}"
                        cache_entry = CacheEntry(
                            cache_key=cache_key,
                            package_info=package_info,
                            cached_at=datetime.now(),
                            cache_version="1.0"
                        )
                        self.save_cache_entry(cache_entry)
                        logger.debug("Cached package info", package=package_name, version=package_info.version)

                    except CacheError as e:
                        # Caching failed, but we still have the data
                        logger.warning("Failed to cache package info", package=package_name, error=str(e))
                        errors.append(FormattedError(
                            message=f"Could not cache documentation for '{package_name}'",
                            suggestion="Documentation was retrieved successfully but caching failed. This may affect future performance.",
                            severity=ErrorSeverity.WARNING,
                            error_code="cache_save_failed",
                            recoverable=True
                        ))

                # Collect any fetch errors
                errors.extend(fetch_result.errors)

        except Exception as e:
            # Catch-all for unexpected errors
            formatted_error = ErrorFormatter.format_exception(
                e, {"package": package_name, "operation": "resolve_and_cache"}
            )
            errors.append(formatted_error)

        return package_info, from_cache, errors

    def get_cached_entry_safe(self, cache_key: str) -> Tuple[CacheEntry | None, List[FormattedError]]:
        """Get cached entry with error handling."""
        errors = []

        try:
            cache_file = self.cache_dir / f"{cache_key}.json"

            if not cache_file.exists():
                return None, errors

            # Check if cache file is corrupted
            try:
                with cache_file.open('r', encoding='utf-8') as f:
                    content = f.read().strip()

                if not content:
                    # Empty cache file
                    cache_file.unlink()  # Remove corrupted file
                    errors.append(FormattedError(
                        message=f"Corrupted cache file removed: {cache_key}",
                        suggestion="The cache file was empty and has been cleaned up automatically.",
                        severity=ErrorSeverity.INFO,
                        error_code="cache_corruption_fixed"
                    ))
                    return None, errors

                data = json.loads(content)
                return CacheEntry.model_validate(data), errors

            except json.JSONDecodeError:
                # Corrupted JSON file
                cache_file.unlink()
                errors.append(FormattedError(
                    message=f"Corrupted cache file removed: {cache_key}",
                    suggestion="The cache file was corrupted and has been cleaned up automatically.",
                    severity=ErrorSeverity.WARNING,
                    error_code="cache_corruption_fixed"
                ))
                return None, errors

        except Exception as e:
            formatted_error = ErrorFormatter.format_exception(
                e, {"cache_key": cache_key, "operation": "cache_retrieval"}
            )
            errors.append(formatted_error)
            return None, errors
```

### Task C3: Update MCP Tools with Graceful Documentation Fetching (0.5 days)

**File**: `src/autodocs_mcp/main.py`

**Implementation**:
```python
@mcp.tool
async def get_package_docs(package_name: str,
                          version_constraint: str | None = None,
                          query: str | None = None) -> dict[str, Any]:
    """
    Enhanced package documentation retrieval with graceful error handling.
    """
    if not cache_manager:
        return {
            "success": False,
            "error": {
                "message": "Service not initialized",
                "suggestion": "Try again or restart the MCP server",
                "severity": "critical",
                "code": "service_not_initialized"
            }
        }

    # Collect all errors from the operation
    all_errors = []
    warnings = []

    try:
        package_info, from_cache, cache_errors = await cache_manager.resolve_and_cache_safe(
            package_name, version_constraint
        )

        all_errors.extend(cache_errors)

        if package_info:
            # Format documentation
            async with PyPIDocumentationFetcher() as fetcher:
                formatted_docs = fetcher.format_documentation(package_info, query)

            # Try to fetch related packages (with error collection)
            dependency_docs, dep_errors = await _fetch_dependency_docs_safe(
                package_name, package_info.version
            )
            all_errors.extend(dep_errors)

            return {
                "success": True,
                "partial_success": len(all_errors) > 0,

                # Main package documentation
                "package_name": package_info.name,
                "version": package_info.version,
                "documentation": formatted_docs,
                "from_cache": from_cache,

                # Dependency documentation (best effort)
                "dependencies": dependency_docs,
                "dependency_count": len(dependency_docs),

                # Error/warning information
                "errors": [
                    {
                        "message": err.message,
                        "suggestion": err.suggestion,
                        "severity": err.severity.value,
                        "code": err.error_code,
                        "recoverable": err.recoverable
                    }
                    for err in all_errors
                ],
                "warnings": warnings,
                "suggestions": [err.suggestion for err in all_errors if err.suggestion]
            }
        else:
            # No package info available
            return {
                "success": False,
                "partial_success": False,
                "package_name": package_name,
                "errors": [
                    {
                        "message": err.message,
                        "suggestion": err.suggestion,
                        "severity": err.severity.value,
                        "code": err.error_code,
                        "recoverable": err.recoverable
                    }
                    for err in all_errors
                ],
                "suggestions": [err.suggestion for err in all_errors if err.suggestion]
            }

    except Exception as e:
        formatted_error = ErrorFormatter.format_exception(e, {"package": package_name})
        return {
            "success": False,
            "error": {
                "message": formatted_error.message,
                "suggestion": formatted_error.suggestion,
                "severity": formatted_error.severity.value,
                "code": formatted_error.error_code,
                "recoverable": formatted_error.recoverable
            }
        }

async def _fetch_dependency_docs_safe(package_name: str, version: str) -> Tuple[List[Dict], List[FormattedError]]:
    """Fetch dependency documentation with individual error handling."""
    dependency_docs = []
    errors = []

    try:
        # Get package dependencies (limit to prevent explosion)
        deps_to_fetch = await _get_key_dependencies(package_name, version, limit=5)

        if not deps_to_fetch:
            return dependency_docs, errors

        # Fetch dependencies concurrently with individual error handling
        async with PyPIDocumentationFetcher() as fetcher:
            fetch_results = await fetcher.fetch_multiple_packages_safe(deps_to_fetch)

            for dep_name, result in fetch_results.items():
                if result.success and result.package_info:
                    # Successfully fetched dependency
                    formatted = fetcher.format_documentation(
                        result.package_info, truncate=True
                    )
                    dependency_docs.append({
                        "name": result.package_info.name,
                        "version": result.package_info.version,
                        "documentation": formatted,
                        "relationship": "dependency",
                        "from_cache": result.from_cache
                    })
                else:
                    # Failed to fetch dependency - collect errors but continue
                    errors.extend(result.errors)

    except Exception as e:
        formatted_error = ErrorFormatter.format_exception(
            e, {"package": package_name, "operation": "dependency_fetch"}
        )
        errors.append(formatted_error)

    return dependency_docs, errors
```

## Testing Requirements

### Unit Tests
- Test partial success scenarios with mixed success/failure
- Test error collection and formatting
- Test cache corruption recovery
- Test concurrent fetch error handling

### Integration Tests
- Test with packages that have missing dependencies
- Test network failure during dependency fetching
- Test cache corruption scenarios
- Test large dependency lists with timeouts

## Example Output

**Partial Success Scenario**:
```json
{
  "success": true,
  "partial_success": true,
  "package_name": "fastapi",
  "version": "0.104.1",
  "documentation": "# FastAPI Documentation...",
  "dependencies": [
    {
      "name": "pydantic",
      "version": "2.5.1",
      "documentation": "# Pydantic...",
      "relationship": "dependency"
    }
  ],
  "errors": [
    {
      "message": "Network error while fetching 'starlette': Request timeout after 3 attempts",
      "suggestion": "Check your internet connection. The operation will be retried automatically.",
      "severity": "error",
      "code": "network_error",
      "recoverable": true
    }
  ],
  "suggestions": [
    "Check your internet connection. The operation will be retried automatically."
  ]
}
```

## Acceptance Criteria

- [ ] Documentation fetching continues even when some dependencies fail
- [ ] Cache corruption is detected and recovered automatically
- [ ] Network failures provide partial results where possible
- [ ] All errors include user-friendly messages and suggestions
- [ ] Concurrent fetching handles individual failures gracefully
- [ ] Performance remains good despite error handling overhead

## Dependencies
- **Stream A (Network Resilience)**: Required for retry patterns and circuit breaker

## Estimated Effort: 2-3 days
- Task C1: 1.5 days (enhanced fetcher implementation)
- Task C2: 1 day (cache manager error recovery)
- Task C3: 0.5 days (MCP tool integration)
