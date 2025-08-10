# Testing Guide

This guide provides step-by-step instructions for testing AutoDocs MCP Server, including how to write tests, run the test suite, and maintain high-quality test coverage.

## Getting Started with Testing

### Prerequisites

Ensure you have the development environment set up:

```bash
# Install all dependencies including testing tools
uv sync

# Verify pytest installation
uv run python -m pytest --version
```

### Running Tests

#### Run All Tests
```bash
# Run complete test suite
uv run python -m pytest

# Run with coverage report
uv run python -m pytest --cov=src --cov-report=html

# Run tests in parallel (faster)
uv run python -m pytest -n auto
```

#### Run Specific Test Categories
```bash
# Unit tests only
uv run python -m pytest tests/unit/

# Integration tests only
uv run python -m pytest tests/integration/

# Specific test file
uv run python -m pytest tests/unit/test_cache_manager.py

# Specific test function
uv run python -m pytest tests/unit/test_cache_manager.py::TestCacheManager::test_store_and_retrieve
```

#### Debug Test Failures
```bash
# Verbose output with print statements
uv run python -m pytest -v -s

# Stop on first failure
uv run python -m pytest -x

# Drop into debugger on failures
uv run python -m pytest --pdb
```

## Writing Tests

### Test Organization

The test suite is organized into clear categories:

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests for individual modules
│   ├── test_cache_manager.py
│   ├── test_doc_fetcher.py
│   └── test_dependency_parser.py
└── integration/             # Integration and end-to-end tests
    ├── test_mcp_server.py
    └── test_end_to_end.py
```

### Required Testing Patterns

#### 1. Use pytest-mock Exclusively

**✅ CORRECT - Use pytest-mock**:
```python
def test_cache_operations(self, mocker):
    # Mock using pytest-mock
    mock_path = mocker.patch("pathlib.Path.exists", return_value=True)
    mock_open = mocker.mock_open(read_data='{"test": "data"}')
    mocker.patch("pathlib.Path.open", mock_open)

    # Test implementation
    cache_manager = CacheManager()
    result = cache_manager.get("test-key")

    # Verify mock calls
    mock_path.assert_called_once()
    assert result == {"test": "data"}
```

**❌ FORBIDDEN - Do not use unittest.mock**:
```python
# This pattern is FORBIDDEN
from unittest.mock import patch, MagicMock

def test_something():
    with patch("module.function") as mock:
        # Don't do this
        pass
```

#### 2. Use Provided Fixtures

**Use mock_services for MCP tool tests**:
```python
def test_mcp_tool(self, mock_services, mocker):
    """Test MCP tools using the shared mock_services fixture."""
    # The fixture provides pre-configured service mocks
    mock_services.dependency_parser.parse_dependencies.return_value = {
        "dependencies": {"requests": ">=2.28.0"}
    }

    # Test your MCP tool
    result = await scan_dependencies(project_path="/test/path")

    # Verify the result
    assert result["dependencies"]["requests"] == ">=2.28.0"
```

#### 3. Test Async Functions Properly

**✅ CORRECT - Async test pattern**:
```python
import pytest

@pytest.mark.asyncio
async def test_async_function(self, mocker):
    """Test async functions with proper async/await."""
    mock_client = mocker.AsyncMock()
    mock_client.get.return_value.json.return_value = {"test": "data"}

    # Test async function
    result = await fetch_package_info("requests")

    # Verify async mock calls
    mock_client.get.assert_awaited_once()
    assert result["test"] == "data"
```

#### 4. Test Both Success and Failure Paths

**Complete test coverage example**:
```python
class TestCacheManager:
    def test_successful_cache_retrieval(self, mocker):
        """Test successful cache operations."""
        # Setup mocks for success path
        mock_exists = mocker.patch("pathlib.Path.exists", return_value=True)
        mock_open = mocker.mock_open(read_data='{"cached": "data"}')
        mocker.patch("pathlib.Path.open", mock_open)

        cache_manager = CacheManager()
        result = cache_manager.get("test-key")

        assert result == {"cached": "data"}
        mock_exists.assert_called_once()

    def test_cache_miss_handling(self, mocker):
        """Test behavior when cache key doesn't exist."""
        mock_exists = mocker.patch("pathlib.Path.exists", return_value=False)

        cache_manager = CacheManager()
        result = cache_manager.get("nonexistent-key")

        assert result is None
        mock_exists.assert_called_once()

    def test_cache_corruption_recovery(self, mocker):
        """Test recovery from corrupted cache files."""
        mock_exists = mocker.patch("pathlib.Path.exists", return_value=True)
        # Simulate corrupted JSON
        mock_open = mocker.mock_open(read_data='invalid json{')
        mocker.patch("pathlib.Path.open", mock_open)

        cache_manager = CacheManager()
        result = cache_manager.get("corrupted-key")

        # Should gracefully handle corruption
        assert result is None
```

### Integration Testing

#### Testing MCP Tools

Use the shared `mock_services` fixture for testing MCP tools:

```python
@pytest.mark.asyncio
async def test_get_package_docs_tool(self, mock_services, mocker):
    """Test the get_package_docs MCP tool end-to-end."""
    # Configure mock responses
    mock_services.doc_fetcher.fetch_docs.return_value = {
        "name": "requests",
        "version": "2.28.0",
        "documentation": "HTTP library for Python"
    }

    # Test the MCP tool
    result = await get_package_docs(
        package_name="requests",
        version_constraint=">=2.28.0"
    )

    # Verify result structure
    assert result["package_name"] == "requests"
    assert "documentation" in result
    assert result["success"] is True

    # Verify service interactions
    mock_services.doc_fetcher.fetch_docs.assert_called_once()
```

#### End-to-End Testing

Test complete workflows from input to output:

```python
@pytest.mark.asyncio
async def test_dependency_scanning_workflow(self, mock_services, tmp_path):
    """Test complete dependency scanning workflow."""
    # Create test pyproject.toml
    pyproject_content = """
    [project]
    dependencies = [
        "requests>=2.28.0",
        "pydantic>=2.0.0"
    ]
    """
    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_file.write_text(pyproject_content)

    # Test the complete workflow
    result = await scan_dependencies(project_path=str(tmp_path))

    # Verify complete response structure
    assert result["success"] is True
    assert len(result["dependencies"]) == 2
    assert "requests" in result["dependencies"]
    assert "pydantic" in result["dependencies"]
```

## Test Quality Requirements

### Coverage Standards

- **Minimum Overall Coverage**: 80%
- **Critical Path Coverage**: 100% for error handling and security
- **New Code Coverage**: 90% for all new features

#### Check Coverage
```bash
# Generate HTML coverage report
uv run python -m pytest --cov=src --cov-report=html

# Open coverage report in browser
open htmlcov/index.html
```

### Performance Testing

#### Load Testing Example
```python
@pytest.mark.benchmark
def test_cache_performance(self, benchmark, mocker):
    """Benchmark cache operations."""
    # Setup
    mock_path = mocker.patch("pathlib.Path.exists", return_value=True)
    mock_open = mocker.mock_open(read_data='{"test": "data"}')
    mocker.patch("pathlib.Path.open", mock_open)

    cache_manager = CacheManager()

    # Benchmark the operation
    result = benchmark(cache_manager.get, "test-key")

    assert result == {"test": "data"}
```

## Debugging Test Issues

### Common Test Problems

#### 1. Async Test Failures
```bash
# Error: "coroutine was never awaited"
# Solution: Add @pytest.mark.asyncio and use await

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()  # Don't forget await!
```

#### 2. Mock Not Being Called
```bash
# Error: Mock was not called as expected
# Solution: Verify the exact import path

# ❌ Wrong import path
mocker.patch("requests.get")

# ✅ Correct import path
mocker.patch("autodocs_mcp.core.doc_fetcher.requests.get")
```

#### 3. Fixture Not Found
```bash
# Error: "fixture 'mock_services' not found"
# Solution: Import fixtures properly in conftest.py or test files
```

### Debug Test Environment
```bash
# Run tests with full output
uv run python -m pytest -v -s --tb=long

# Run single test with debugging
uv run python -m pytest tests/unit/test_cache_manager.py::test_specific -v -s --pdb
```

## Test Maintenance

### Updating Tests for Code Changes

#### When Adding New Features
1. **Write tests first** (TDD approach recommended)
2. **Test both success and failure paths**
3. **Update integration tests** if the feature affects MCP tools
4. **Verify coverage** doesn't decrease

#### When Refactoring Code
1. **Keep existing tests passing** during refactoring
2. **Update tests** to match new internal structures
3. **Maintain test coverage** at the same level
4. **Remove obsolete tests** for deleted functionality

### Test Data Management

#### Using Temporary Files
```python
def test_with_temp_files(self, tmp_path):
    """Use tmp_path fixture for temporary files."""
    test_file = tmp_path / "test.json"
    test_file.write_text('{"test": "data"}')

    # Test with the temporary file
    result = process_file(test_file)

    assert result["test"] == "data"
    # File automatically cleaned up
```

#### Mock Data Patterns
```python
# Create reusable mock data
MOCK_PYPROJECT_CONTENT = """
[project]
dependencies = ["requests>=2.28.0"]
"""

MOCK_PYPI_RESPONSE = {
    "info": {
        "name": "requests",
        "version": "2.28.0",
        "summary": "HTTP library for Python"
    }
}
```

## Running Tests in CI/CD

The test suite is designed to run reliably in CI/CD environments:

```bash
# CI command for comprehensive testing
uv run python -m pytest \
    --cov=src \
    --cov-report=xml \
    --cov-report=term-missing \
    -n auto \
    --tb=short
```

### Test Reliability

#### Avoiding Flaky Tests
- **Use deterministic mocks** instead of real network calls
- **Clean up resources** properly in teardown
- **Avoid time-dependent tests** or use time mocking
- **Use proper async patterns** for concurrent operations

#### Parallel Test Execution
```bash
# Run tests in parallel safely
uv run python -m pytest -n auto

# Control number of workers
uv run python -m pytest -n 4
```

Following these testing practices ensures high code quality, prevents regressions, and enables confident refactoring and feature development.
