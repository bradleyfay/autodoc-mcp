# Test Coverage Remediation - Priority 1 (BLOCKING)

## Overview
Current test coverage of 62% is inadequate for production deployment. Critical application components have dangerously low coverage, creating high risk of production failures.

## Current Coverage Analysis

**Critical Gaps Identified**:
- **main.py (26% coverage)**: Core MCP server logic untested
- **doc_fetcher.py (24% coverage)**: Primary documentation functionality missing tests
- **cache_manager.py (45% coverage)**: Data persistence layer undertested
- **error_formatter.py (38% coverage)**: User-facing error messages untested

**Target**: >80% overall coverage with 100% coverage for critical paths

## Test Coverage Tasks

### Task 3.1: Core MCP Server Testing
**Assignee**: QA Engineer + Backend Developer
**Estimated Time**: 6 hours
**Target Coverage**: >80% for `main.py`

**Current Issues**:
- MCP tool endpoints completely untested
- Service initialization logic untested
- Error handling in main server loop untested

**Required Test Cases**:

```python
# tests/unit/test_main_server.py

@pytest.mark.asyncio
class TestMCPTools:
    """Comprehensive MCP tool testing."""

    async def test_scan_dependencies_success(self, mock_parser):
        """Test successful dependency scanning."""
        # Setup mock parser response
        mock_result = ScanResult(...)
        mock_parser.parse_project.return_value = mock_result

        # Test the MCP tool
        result = await scan_dependencies("/test/project")

        assert result["success"] is True
        assert result["dependency_count"] == expected_count

    async def test_scan_dependencies_parser_not_initialized(self):
        """Test scan_dependencies when parser is None."""
        global parser
        original_parser = parser
        parser = None

        try:
            result = await scan_dependencies("/test/project")
            assert result["success"] is False
            assert result["error"]["code"] == "service_not_initialized"
        finally:
            parser = original_parser

    async def test_scan_dependencies_project_parsing_error(self, mock_parser):
        """Test scan_dependencies with ProjectParsingError."""
        mock_parser.parse_project.side_effect = ProjectParsingError(
            "Invalid project", Path("/test")
        )

        result = await scan_dependencies("/test/project")

        assert result["success"] is False
        assert "Invalid project" in result["error"]["message"]

    async def test_get_package_docs_success(self, mock_services):
        """Test successful package documentation retrieval."""
        # Detailed test implementation...

    async def test_get_package_docs_services_not_initialized(self):
        """Test get_package_docs when services are None."""
        # Implementation...

    async def test_get_package_docs_with_context_success(self, mock_context_fetcher):
        """Test successful context documentation retrieval."""
        # Implementation...

    async def test_refresh_cache_success(self, mock_cache_manager):
        """Test successful cache refresh."""
        # Implementation...

    async def test_get_cache_stats_success(self, mock_cache_manager):
        """Test successful cache statistics retrieval."""
        # Implementation...

@pytest.mark.asyncio
class TestServiceInitialization:
    """Test service initialization and error handling."""

    async def test_initialize_services_success(self):
        """Test successful service initialization."""
        # Implementation...

    async def test_initialize_services_cache_failure(self):
        """Test service initialization with cache manager failure."""
        # Implementation...

    async def test_main_function_graceful_shutdown(self):
        """Test main function handles shutdown signals."""
        # Implementation...
```

**Files to Create/Modify**:
- `tests/unit/test_main_server.py` (new)
- `tests/integration/test_mcp_tools_integration.py` (new)

**Acceptance Criteria**:
- ✅ All MCP tools have comprehensive unit tests
- ✅ Service initialization edge cases covered
- ✅ Error handling paths tested
- ✅ >80% coverage for `main.py`

---

### Task 3.2: Documentation Fetcher Testing
**Assignee**: QA Engineer
**Estimated Time**: 5 hours
**Target Coverage**: >80% for `doc_fetcher.py`

**Current Issues**:
- PyPI API integration completely untested
- Documentation formatting logic untested
- Network error handling untested

**Required Test Cases**:

```python
# tests/unit/test_doc_fetcher.py

@pytest.mark.asyncio
class TestPyPIDocumentationFetcher:
    """Comprehensive documentation fetcher testing."""

    async def test_fetch_package_info_success(self, mock_network_client):
        """Test successful package information fetching."""
        # Mock successful PyPI response
        mock_response = {
            "info": {
                "name": "requests",
                "version": "2.28.2",
                "summary": "HTTP library",
                "description": "...",
                "author": "Kenneth Reitz"
            }
        }
        mock_network_client.get_with_retry.return_value.json.return_value = mock_response

        async with PyPIDocumentationFetcher() as fetcher:
            result = await fetcher.fetch_package_info("requests")

        assert result.name == "requests"
        assert result.version == "2.28.2"
        assert result.summary == "HTTP library"

    async def test_fetch_package_info_package_not_found(self, mock_network_client):
        """Test fetching non-existent package."""
        mock_network_client.get_with_retry.side_effect = PackageNotFoundError("Not found")

        async with PyPIDocumentationFetcher() as fetcher:
            with pytest.raises(PackageNotFoundError):
                await fetcher.fetch_package_info("nonexistent-package")

    async def test_fetch_package_info_network_error(self, mock_network_client):
        """Test network error handling."""
        mock_network_client.get_with_retry.side_effect = NetworkError("Connection failed")

        async with PyPIDocumentationFetcher() as fetcher:
            with pytest.raises(NetworkError):
                await fetcher.fetch_package_info("requests")

    async def test_fetch_package_info_safe_success(self, mock_network_client):
        """Test safe package fetching with error collection."""
        # Implementation for DocFetchResult testing...

    async def test_fetch_multiple_packages_safe(self, mock_network_client):
        """Test batch package fetching with partial failures."""
        # Implementation...

    def test_format_documentation_basic(self):
        """Test basic documentation formatting."""
        package_info = PackageInfo(
            name="test-package",
            version="1.0.0",
            summary="Test package",
            description="A test package for testing"
        )

        fetcher = PyPIDocumentationFetcher()
        result = fetcher.format_documentation(package_info)

        assert "# test-package v1.0.0" in result
        assert "Test package" in result

    def test_format_documentation_with_query(self):
        """Test documentation formatting with query filtering."""
        # Implementation...

    def test_format_documentation_size_limits(self):
        """Test documentation truncation for large content."""
        # Implementation...

    def test_parse_pypi_response_valid(self):
        """Test PyPI response parsing."""
        # Implementation...

    def test_parse_pypi_response_malformed(self):
        """Test PyPI response parsing with malformed data."""
        # Implementation...
```

**Files to Create/Modify**:
- `tests/unit/test_doc_fetcher.py` (enhance existing)
- `tests/integration/test_pypi_api.py` (new)

**Acceptance Criteria**:
- ✅ PyPI API integration thoroughly tested
- ✅ Documentation formatting edge cases covered
- ✅ Network error scenarios tested
- ✅ Safe fetching methods tested
- ✅ >80% coverage for `doc_fetcher.py`

---

### Task 3.3: Cache Manager Testing
**Assignee**: Backend Developer
**Estimated Time**: 4 hours
**Target Coverage**: >85% for `cache_manager.py`

**Current Issues**:
- Cache corruption handling untested
- File I/O error scenarios untested
- Cache statistics and cleanup untested

**Required Test Cases**:

```python
# tests/unit/test_cache_manager.py

@pytest.mark.asyncio
class TestFileCacheManager:
    """Comprehensive cache manager testing."""

    async def test_get_cache_hit(self, temp_cache_dir):
        """Test successful cache retrieval."""
        # Setup cache file with valid data
        cache_manager = FileCacheManager(temp_cache_dir)

        # Create test cache entry
        test_package = PackageInfo(name="test", version="1.0.0")
        await cache_manager.set("test-1.0.0", test_package)

        # Retrieve and verify
        result = await cache_manager.get("test-1.0.0")
        assert result is not None
        assert result.data.name == "test"

    async def test_get_cache_miss(self, temp_cache_dir):
        """Test cache miss behavior."""
        cache_manager = FileCacheManager(temp_cache_dir)
        result = await cache_manager.get("nonexistent-key")
        assert result is None

    async def test_get_corrupted_cache_file(self, temp_cache_dir):
        """Test handling of corrupted cache files."""
        cache_manager = FileCacheManager(temp_cache_dir)

        # Create corrupted cache file
        cache_file = temp_cache_dir / "corrupted-key.json"
        cache_file.write_text("invalid json content")

        result = await cache_manager.get("corrupted-key")
        assert result is None
        assert not cache_file.exists()  # Should be cleaned up

    async def test_set_cache_success(self, temp_cache_dir):
        """Test successful cache storage."""
        # Implementation...

    async def test_set_cache_io_error(self, temp_cache_dir, mock_io_error):
        """Test cache storage with I/O errors."""
        # Implementation...

    async def test_invalidate_specific_key(self, temp_cache_dir):
        """Test invalidation of specific cache key."""
        # Implementation...

    async def test_invalidate_entire_cache(self, temp_cache_dir):
        """Test invalidation of entire cache."""
        # Implementation...

    async def test_get_cache_stats(self, temp_cache_dir):
        """Test cache statistics generation."""
        # Implementation...

    async def test_list_cached_packages(self, temp_cache_dir):
        """Test listing cached package keys."""
        # Implementation...

    def test_get_cached_entry_safe_success(self, temp_cache_dir):
        """Test safe cache retrieval with error handling."""
        # Implementation...

    def test_get_cached_entry_safe_corruption(self, temp_cache_dir):
        """Test safe cache retrieval with corruption handling."""
        # Implementation...

    async def test_resolve_and_cache_hit(self, temp_cache_dir, mock_version_resolver):
        """Test resolve_and_cache with cache hit."""
        # Implementation...

    async def test_resolve_and_cache_miss(self, temp_cache_dir, mock_version_resolver):
        """Test resolve_and_cache with cache miss and fresh fetch."""
        # Implementation...
```

**Files to Create/Modify**:
- `tests/unit/test_cache_manager.py` (enhance existing)
- `tests/integration/test_cache_persistence.py` (new)

**Acceptance Criteria**:
- ✅ All cache operations thoroughly tested
- ✅ Error conditions and corruption handling covered
- ✅ File I/O edge cases tested
- ✅ Cache statistics functionality tested
- ✅ >85% coverage for `cache_manager.py`

---

### Task 3.4: Error Formatter Testing
**Assignee**: QA Engineer
**Estimated Time**: 3 hours
**Target Coverage**: >85% for `error_formatter.py`

**Current Issues**:
- User-facing error message generation untested
- Dependency parsing error formatting untested
- Error suggestion logic untested

**Required Test Cases**:

```python
# tests/unit/test_error_formatter.py

class TestErrorFormatter:
    """Comprehensive error formatter testing."""

    def test_format_dependency_parsing_errors(self):
        """Test dependency parsing error formatting."""
        failed_deps = [
            {
                "dependency_string": "invalid[package]name>=1.0",
                "error": "Invalid package name format: 'invalid[package]name'",
                "source": "dependencies"
            }
        ]

        result = ErrorFormatter.format_dependency_parsing_errors(failed_deps)

        assert len(result) == 1
        assert result[0].error_code == "invalid_package_name"
        assert "invalid[package]name" in result[0].message
        assert result[0].suggestion is not None

    def test_format_single_dependency_error_invalid_package_name(self):
        """Test specific error type formatting."""
        # Implementation...

    def test_format_single_dependency_error_malformed_extras(self):
        """Test malformed extras error formatting."""
        # Implementation...

    def test_format_single_dependency_error_invalid_version(self):
        """Test invalid version error formatting."""
        # Implementation...

    def test_suggest_package_name_fix(self):
        """Test package name suggestion logic."""
        assert ErrorFormatter._suggest_package_name_fix("my@package") == "my-package"
        assert ErrorFormatter._suggest_package_name_fix("UPPER") == "UPPER"

    def test_suggest_extras_fix(self):
        """Test extras syntax suggestion logic."""
        result = ErrorFormatter._suggest_extras_fix("package[extra")
        assert "package[extra1,extra2]>=1.0.0" in result

    def test_format_network_errors(self):
        """Test network error formatting."""
        errors = [
            {
                "type": "PackageNotFoundError",
                "package": "nonexistent",
                "message": "Package not found",
                "suggestions": ["similar-package"]
            }
        ]

        result = ErrorFormatter.format_network_errors(errors)

        assert len(result) == 1
        assert result[0].error_code == "package_not_found"
        assert "nonexistent" in result[0].message
        assert "similar-package" in result[0].suggestion

    def test_format_exception_project_parsing_error(self):
        """Test ProjectParsingError formatting."""
        exc = ProjectParsingError("Invalid TOML", Path("/test/pyproject.toml"))
        result = ErrorFormatter.format_exception(exc)

        assert result.severity == ErrorSeverity.CRITICAL
        assert result.error_code == "project_parse_error"
        assert not result.recoverable

    def test_format_exception_package_not_found(self):
        """Test PackageNotFoundError formatting."""
        # Implementation...

    def test_format_exception_network_error(self):
        """Test NetworkError formatting."""
        # Implementation...

    def test_format_exception_generic(self):
        """Test generic exception formatting."""
        # Implementation...

class TestResponseFormatter:
    """Test response formatting functionality."""

    def test_format_scan_response_success(self):
        """Test successful scan response formatting."""
        # Implementation...

    def test_format_scan_response_with_errors(self):
        """Test scan response formatting with dependency errors."""
        # Implementation...

    def test_format_scan_response_suggestions_generation(self):
        """Test suggestions summary generation."""
        # Implementation...
```

**Files to Create/Modify**:
- `tests/unit/test_error_formatter.py` (new)

**Acceptance Criteria**:
- ✅ All error formatting patterns tested
- ✅ Suggestion generation logic verified
- ✅ Edge cases and malformed inputs covered
- ✅ Response formatting thoroughly tested
- ✅ >85% coverage for `error_formatter.py`

---

### Task 3.5: Integration Testing Suite
**Assignee**: QA Engineer + Backend Developer
**Estimated Time**: 4 hours

**Required Integration Tests**:

```python
# tests/integration/test_end_to_end.py

@pytest.mark.integration
@pytest.mark.asyncio
class TestEndToEndWorkflow:
    """End-to-end workflow testing."""

    async def test_complete_documentation_workflow(self):
        """Test complete flow from dependency scan to documentation."""
        # 1. Scan project dependencies
        scan_result = await scan_dependencies("tests/fixtures/sample_project")
        assert scan_result["success"] is True

        # 2. Get documentation for first dependency
        first_dep = scan_result["dependencies"][0]["name"]
        docs_result = await get_package_docs(first_dep)
        assert docs_result["success"] is True

        # 3. Get documentation with context
        context_result = await get_package_docs_with_context(first_dep)
        assert context_result["success"] is True

    async def test_error_recovery_workflow(self):
        """Test system behavior under error conditions."""
        # Test with invalid project path
        result = await scan_dependencies("/nonexistent/path")
        assert result["success"] is False
        assert result["error"]["recoverable"] is False

    @pytest.mark.slow
    async def test_performance_requirements(self):
        """Test performance requirements are met."""
        import time

        start_time = time.time()
        result = await get_package_docs_with_context("requests")
        elapsed = time.time() - start_time

        assert result["success"] is True
        assert elapsed < 5.0  # Must complete within 5 seconds

@pytest.mark.integration
class TestRealPyPIIntegration:
    """Test integration with real PyPI API."""

    @pytest.mark.slow
    async def test_real_pypi_requests(self):
        """Test against real PyPI API with common packages."""
        test_packages = ["requests", "pydantic", "fastapi"]

        for package in test_packages:
            result = await get_package_docs(package)
            assert result["success"] is True
            assert result["package_name"] == package

    @pytest.mark.slow
    async def test_network_resilience_with_real_api(self):
        """Test network resilience patterns with real API."""
        # This test should pass even with occasional network issues
        # Implementation...
```

**Files to Create**:
- `tests/integration/test_end_to_end.py` (new)
- `tests/integration/test_real_pypi.py` (new)
- `tests/fixtures/sample_project/pyproject.toml` (test fixture)

**Acceptance Criteria**:
- ✅ Complete end-to-end workflows tested
- ✅ Real PyPI API integration verified
- ✅ Performance requirements validated
- ✅ Error recovery scenarios tested
- ✅ Network resilience patterns verified

## Test Infrastructure Improvements

### Task 3.6: Test Infrastructure and Fixtures
**Assignee**: QA Engineer
**Estimated Time**: 2 hours

**Requirements**:
1. **Enhanced Test Fixtures**:
   - Sample pyproject.toml files for testing
   - Mock PyPI API responses
   - Temporary cache directories
   - Network error simulation

2. **Test Configuration**:
   - Separate test configuration profiles
   - Mock service dependencies
   - Performance test markers

3. **CI/CD Integration**:
   - Coverage reporting integration
   - Slow test categorization
   - Integration test environment setup

**Files to Create/Modify**:
- `tests/conftest.py` (enhance)
- `tests/fixtures/` directory structure
- `pytest.ini` configuration
- `.github/workflows/test.yml` (enhance)

## Completion Criteria

**Test Coverage Gate Requirements**:
1. ✅ Overall coverage >80%
2. ✅ Critical files (main.py, doc_fetcher.py, cache_manager.py) >80%
3. ✅ All MCP tools have comprehensive tests
4. ✅ Integration tests pass with real APIs
5. ✅ Performance tests meet SLA requirements
6. ✅ Error condition testing complete
7. ✅ CI/CD pipeline updated with coverage reporting

**Quality Assurance Standards**:
- All new tests must pass consistently
- Test execution time <5 minutes for unit tests
- Integration tests categorized and run separately
- Coverage reports integrated into PR process
- Performance benchmarks established and monitored

**Time Allocation**:
- Unit test implementation: 16 hours
- Integration test implementation: 4 hours
- Test infrastructure: 2 hours
- **Total: 1.5 days** (with parallel development)
