# Stream D: MCP Response Standardization

## Overview
Create consistent error/warning patterns across all MCP tools with standardized response formats, ensuring a uniform user experience regardless of which tool encounters issues.

## Current State
- Inconsistent response formats between different MCP tools
- No standardized error structure across tools
- Missing consistent metadata (timestamps, request IDs, etc.)
- No unified success/partial success indicators

## Dependencies
**Requires Stream B**: Error message formatting infrastructure must be available for consistent error handling.

## Implementation Tasks

### Task D1: Standard Response Schema (0.5 days)

**File**: `src/autodocs_mcp/models/responses.py`

**Implementation**:
```python
"""Standardized response models for all MCP tools."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field

class ResponseStatus(Enum):
    """Standard response status values."""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"

class ResponseSeverity(Enum):
    """Severity levels for errors and warnings."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ResponseError(BaseModel):
    """Standardized error format for all MCP tools."""
    message: str = Field(description="Human-readable error message")
    suggestion: Optional[str] = Field(None, description="Actionable suggestion to resolve the error")
    severity: ResponseSeverity = Field(description="Error severity level")
    code: str = Field(description="Machine-readable error code")
    recoverable: bool = Field(True, description="Whether this error can be recovered from")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context information")

class ResponseMetadata(BaseModel):
    """Standard metadata for all responses."""
    request_id: str = Field(default_factory=lambda: str(uuid4())[:8])
    timestamp: datetime = Field(default_factory=datetime.now)
    tool_name: str = Field(description="Name of the MCP tool that generated this response")
    tool_version: str = Field(default="1.0.0", description="Version of the tool")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")

class StandardMCPResponse(BaseModel):
    """Base response model for all MCP tools."""
    status: ResponseStatus = Field(description="Overall operation status")
    success: bool = Field(description="Whether the primary operation succeeded")

    # Error and warning information
    errors: List[ResponseError] = Field(default_factory=list, description="List of errors encountered")
    warnings: List[str] = Field(default_factory=list, description="List of warning messages")
    suggestions: List[str] = Field(default_factory=list, description="List of actionable suggestions")

    # Metadata
    metadata: ResponseMetadata = Field(description="Response metadata")

    # Tool-specific data (to be extended by specific response types)
    data: Optional[Dict[str, Any]] = Field(None, description="Tool-specific response data")

    @property
    def partial_success(self) -> bool:
        """Check if this is a partial success (succeeded but with errors/warnings)."""
        return self.success and (len(self.errors) > 0 or len(self.warnings) > 0)

    def add_error(self, error: ResponseError):
        """Add an error to the response."""
        self.errors.append(error)
        if error.severity in [ResponseSeverity.ERROR, ResponseSeverity.CRITICAL]:
            self.success = False

    def add_warning(self, message: str):
        """Add a warning message."""
        self.warnings.append(message)

    def add_suggestion(self, suggestion: str):
        """Add an actionable suggestion."""
        if suggestion and suggestion not in self.suggestions:
            self.suggestions.append(suggestion)

    def finalize(self) -> Dict[str, Any]:
        """Finalize the response and determine status."""
        if self.success and not self.partial_success:
            self.status = ResponseStatus.SUCCESS
        elif self.success and self.partial_success:
            self.status = ResponseStatus.PARTIAL_SUCCESS
        else:
            self.status = ResponseStatus.FAILURE

        return self.model_dump(exclude_none=True)

class ScanDependenciesResponse(StandardMCPResponse):
    """Specific response model for scan_dependencies tool."""

    def __init__(self, **data):
        super().__init__(**data)
        self.metadata.tool_name = "scan_dependencies"

    @classmethod
    def from_scan_result(cls, result: 'ScanResult', execution_time: float = None) -> 'ScanDependenciesResponse':
        """Create response from ScanResult with error formatting."""
        response = cls(
            success=len(result.dependencies) > 0,
            metadata=ResponseMetadata(
                tool_name="scan_dependencies",
                execution_time=execution_time
            ),
            data={
                "project_name": result.project_name,
                "project_path": str(result.project_path),
                "dependencies": [dep.model_dump() for dep in result.dependencies],
                "dependency_count": result.successful_deps,
                "scan_timestamp": result.scan_timestamp.isoformat()
            }
        )

        # Add formatted errors
        if result.failed_deps:
            formatted_errors = ErrorFormatter.format_dependency_parsing_errors(result.failed_deps)
            for formatted_error in formatted_errors:
                response.add_error(ResponseError(
                    message=formatted_error.message,
                    suggestion=formatted_error.suggestion,
                    severity=ResponseSeverity(formatted_error.severity.value),
                    code=formatted_error.error_code,
                    recoverable=formatted_error.recoverable,
                    context=formatted_error.context
                ))
                if formatted_error.suggestion:
                    response.add_suggestion(formatted_error.suggestion)

        # Add warnings
        for warning in result.warnings:
            response.add_warning(warning)

        return response

class GetPackageDocsResponse(StandardMCPResponse):
    """Specific response model for get_package_docs tool."""

    def __init__(self, **data):
        super().__init__(**data)
        self.metadata.tool_name = "get_package_docs"

    @classmethod
    def create_success(cls, package_info: 'PackageInfo', documentation: str,
                      dependencies: List[Dict] = None, from_cache: bool = False,
                      execution_time: float = None) -> 'GetPackageDocsResponse':
        """Create successful response."""
        return cls(
            success=True,
            metadata=ResponseMetadata(
                tool_name="get_package_docs",
                execution_time=execution_time
            ),
            data={
                "package_name": package_info.name,
                "version": package_info.version,
                "documentation": documentation,
                "from_cache": from_cache,
                "dependencies": dependencies or [],
                "dependency_count": len(dependencies) if dependencies else 0
            }
        )

    @classmethod
    def create_failure(cls, package_name: str, errors: List[ResponseError],
                      execution_time: float = None) -> 'GetPackageDocsResponse':
        """Create failure response."""
        response = cls(
            success=False,
            metadata=ResponseMetadata(
                tool_name="get_package_docs",
                execution_time=execution_time
            ),
            data={
                "package_name": package_name
            }
        )

        for error in errors:
            response.add_error(error)
            if error.suggestion:
                response.add_suggestion(error.suggestion)

        return response

class CacheStatsResponse(StandardMCPResponse):
    """Response model for cache statistics."""

    def __init__(self, **data):
        super().__init__(**data)
        self.metadata.tool_name = "get_cache_stats"

    @classmethod
    def create(cls, stats: Dict[str, Any], execution_time: float = None) -> 'CacheStatsResponse':
        """Create cache stats response."""
        return cls(
            success=True,
            metadata=ResponseMetadata(
                tool_name="get_cache_stats",
                execution_time=execution_time
            ),
            data=stats
        )

class RefreshCacheResponse(StandardMCPResponse):
    """Response model for cache refresh operations."""

    def __init__(self, **data):
        super().__init__(**data)
        self.metadata.tool_name = "refresh_cache"

    @classmethod
    def create(cls, refresh_stats: Dict[str, Any], execution_time: float = None) -> 'RefreshCacheResponse':
        """Create cache refresh response."""
        return cls(
            success=True,
            metadata=ResponseMetadata(
                tool_name="refresh_cache",
                execution_time=execution_time
            ),
            data=refresh_stats
        )
```

### Task D2: Response Builder Utility (0.5 days)

**File**: `src/autodocs_mcp/core/response_builder.py`

**Implementation**:
```python
"""Utility for building standardized MCP responses."""

import time
from typing import Any, Dict, List, Optional, Type, TypeVar
from functools import wraps

from ..models.responses import (
    ResponseError, ResponseSeverity, StandardMCPResponse,
    ScanDependenciesResponse, GetPackageDocsResponse,
    CacheStatsResponse, RefreshCacheResponse
)
from .error_formatter import ErrorFormatter, FormattedError

T = TypeVar('T', bound=StandardMCPResponse)

class ResponseBuilder:
    """Builder for creating standardized MCP responses."""

    @staticmethod
    def build_error_response(response_class: Type[T],
                           primary_error: Exception,
                           context: Optional[Dict[str, Any]] = None,
                           execution_time: Optional[float] = None) -> T:
        """Build an error response from an exception."""
        formatted_error = ErrorFormatter.format_exception(primary_error, context)

        response_error = ResponseError(
            message=formatted_error.message,
            suggestion=formatted_error.suggestion,
            severity=ResponseSeverity(formatted_error.severity.value),
            code=formatted_error.error_code,
            recoverable=formatted_error.recoverable,
            context=formatted_error.context
        )

        response = response_class(
            success=False,
            metadata=response_class().metadata  # Get default metadata
        )

        if execution_time is not None:
            response.metadata.execution_time = execution_time

        response.add_error(response_error)
        if response_error.suggestion:
            response.add_suggestion(response_error.suggestion)

        return response

    @staticmethod
    def build_from_formatted_errors(response_class: Type[T],
                                   formatted_errors: List[FormattedError],
                                   success: bool = False,
                                   data: Optional[Dict[str, Any]] = None,
                                   execution_time: Optional[float] = None) -> T:
        """Build response from list of formatted errors."""
        response = response_class(
            success=success,
            data=data or {}
        )

        if execution_time is not None:
            response.metadata.execution_time = execution_time

        for formatted_error in formatted_errors:
            response_error = ResponseError(
                message=formatted_error.message,
                suggestion=formatted_error.suggestion,
                severity=ResponseSeverity(formatted_error.severity.value),
                code=formatted_error.error_code,
                recoverable=formatted_error.recoverable,
                context=formatted_error.context
            )
            response.add_error(response_error)

            if formatted_error.suggestion:
                response.add_suggestion(formatted_error.suggestion)

        return response

def standardized_response(response_class: Type[StandardMCPResponse]):
    """Decorator to standardize MCP tool responses."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()

            try:
                # Execute the original function
                result = await func(*args, **kwargs)

                # If result is already a standardized response, return as-is
                if isinstance(result, StandardMCPResponse):
                    if result.metadata.execution_time is None:
                        result.metadata.execution_time = time.time() - start_time
                    return result.finalize()

                # If result is a dict, wrap it in the response class
                if isinstance(result, dict):
                    response = response_class(
                        success=result.get('success', True),
                        data=result,
                        metadata=response_class().metadata
                    )
                    response.metadata.execution_time = time.time() - start_time
                    return response.finalize()

                # Fallback: create generic success response
                response = response_class(
                    success=True,
                    data={"result": result} if result is not None else {}
                )
                response.metadata.execution_time = time.time() - start_time
                return response.finalize()

            except Exception as e:
                execution_time = time.time() - start_time
                error_response = ResponseBuilder.build_error_response(
                    response_class, e, execution_time=execution_time
                )
                return error_response.finalize()

        return wrapper
    return decorator
```

### Task D3: Update All MCP Tools (1 day)

**File**: `src/autodocs_mcp/main.py`

**Implementation**:
```python
"""Updated MCP tools with standardized responses."""

from .core.response_builder import standardized_response
from .models.responses import (
    ScanDependenciesResponse, GetPackageDocsResponse,
    CacheStatsResponse, RefreshCacheResponse
)

@mcp.tool
@standardized_response(ScanDependenciesResponse)
async def scan_dependencies(project_path: str | None = None) -> ScanDependenciesResponse:
    """
    Scan project dependencies with standardized response format.
    """
    start_time = time.time()

    if not parser:
        raise AutoDocsError("Parser service not initialized")

    resolved_path = Path(project_path) if project_path else Path.cwd()
    logger.info("Scanning dependencies", project_path=str(resolved_path))

    result = await parser.parse_project(resolved_path)
    execution_time = time.time() - start_time

    return ScanDependenciesResponse.from_scan_result(result, execution_time)

@mcp.tool
@standardized_response(GetPackageDocsResponse)
async def get_package_docs(package_name: str,
                          version_constraint: str | None = None,
                          query: str | None = None) -> GetPackageDocsResponse:
    """
    Get package documentation with standardized error handling.
    """
    start_time = time.time()

    if not cache_manager:
        raise AutoDocsError("Cache manager service not initialized")

    logger.info("Fetching package documentation",
               package=package_name, constraint=version_constraint)

    # Use the enhanced cache manager method
    package_info, from_cache, errors = await cache_manager.resolve_and_cache_safe(
        package_name, version_constraint
    )

    execution_time = time.time() - start_time

    if package_info:
        # Format documentation
        async with PyPIDocumentationFetcher() as fetcher:
            formatted_docs = fetcher.format_documentation(package_info, query)

        # Fetch dependency docs with error collection
        dependency_docs, dep_errors = await _fetch_dependency_docs_safe(
            package_name, package_info.version
        )
        errors.extend(dep_errors)

        response = GetPackageDocsResponse.create_success(
            package_info=package_info,
            documentation=formatted_docs,
            dependencies=dependency_docs,
            from_cache=from_cache,
            execution_time=execution_time
        )

        # Add any errors encountered during the process
        for error in errors:
            response_error = ResponseError(
                message=error.message,
                suggestion=error.suggestion,
                severity=ResponseSeverity(error.severity.value),
                code=error.error_code,
                recoverable=error.recoverable,
                context=error.context
            )
            response.add_error(response_error)
            if error.suggestion:
                response.add_suggestion(error.suggestion)

        return response
    else:
        # Convert formatted errors to response errors
        response_errors = [
            ResponseError(
                message=error.message,
                suggestion=error.suggestion,
                severity=ResponseSeverity(error.severity.value),
                code=error.error_code,
                recoverable=error.recoverable,
                context=error.context
            )
            for error in errors
        ]

        return GetPackageDocsResponse.create_failure(
            package_name=package_name,
            errors=response_errors,
            execution_time=execution_time
        )

@mcp.tool
@standardized_response(RefreshCacheResponse)
async def refresh_cache() -> RefreshCacheResponse:
    """
    Refresh cache with standardized response format.
    """
    start_time = time.time()

    if not cache_manager:
        raise AutoDocsError("Cache manager service not initialized")

    logger.info("Refreshing documentation cache")

    refresh_stats = await cache_manager.clear_cache()
    execution_time = time.time() - start_time

    return RefreshCacheResponse.create(
        refresh_stats=refresh_stats,
        execution_time=execution_time
    )

@mcp.tool
@standardized_response(CacheStatsResponse)
async def get_cache_stats() -> CacheStatsResponse:
    """
    Get cache statistics with standardized response format.
    """
    start_time = time.time()

    if not cache_manager:
        raise AutoDocsError("Cache manager service not initialized")

    logger.debug("Retrieving cache statistics")

    stats = await cache_manager.get_cache_stats()
    execution_time = time.time() - start_time

    return CacheStatsResponse.create(
        stats=stats,
        execution_time=execution_time
    )
```

## Testing Requirements

### Unit Tests
- Test standardized response format consistency
- Test error response creation from various exception types
- Test response builder utility functions
- Test decorator behavior with different return types

### Integration Tests
- Test all MCP tools return consistent response format
- Test error scenarios produce standardized error responses
- Test partial success scenarios are handled consistently

## Example Standardized Response

**Before** (inconsistent format):
```json
{
  "success": true,
  "dependencies": [...],
  "warnings": ["Some warning"],
  "failed_deps": [...]
}
```

**After** (standardized format):
```json
{
  "status": "partial_success",
  "success": true,
  "errors": [
    {
      "message": "Invalid version specifier in 'package==' from project section",
      "suggestion": "Use valid version operators: package>=1.0.0",
      "severity": "warning",
      "code": "invalid_version",
      "recoverable": true
    }
  ],
  "warnings": [],
  "suggestions": ["Use valid version operators: package>=1.0.0"],
  "metadata": {
    "request_id": "abc12345",
    "timestamp": "2025-08-07T10:30:00Z",
    "tool_name": "scan_dependencies",
    "tool_version": "1.0.0",
    "execution_time": 0.245
  },
  "data": {
    "project_name": "my-project",
    "project_path": "/path/to/project",
    "dependencies": [...],
    "dependency_count": 15,
    "scan_timestamp": "2025-08-07T10:30:00Z"
  }
}
```

## Acceptance Criteria

- [ ] All MCP tools return responses in consistent format
- [ ] Response includes standard metadata (request ID, timestamp, execution time)
- [ ] Error messages follow standardized format with severity levels
- [ ] Partial success scenarios clearly indicated in response status
- [ ] Backwards compatibility maintained for existing tool consumers
- [ ] Request tracking enabled through request IDs
- [ ] Tool performance metrics available through execution time

## Dependencies
- **Stream B (Error Messaging)**: Required for error formatting infrastructure

## Estimated Effort: 1-2 days
- Task D1: 0.5 days (response schema design)
- Task D2: 0.5 days (response builder utility)
- Task D3: 1 day (updating all MCP tools)
