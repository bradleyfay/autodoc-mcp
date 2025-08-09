# Technical Debt Tracking

This document tracks technical debt items that need to be addressed to improve code quality, maintainability, and consistency.

## Testing Infrastructure Debt

### High Priority

#### Inconsistent Mock Usage (Created: 2025-08-09)
- **Description**: Mixed usage of `unittest.mock` and `pytest-mock` across test files
- **Impact**: Inconsistent testing patterns, harder maintenance, potential for mock-related bugs
- **Scope**: ~40 test files need conversion
- **Root Cause**: Project grew organically without consistent mocking standards
- **Solution**: Convert remaining `unittest.mock.patch`, `AsyncMock`, `MagicMock` usage to pytest-mock patterns
- **Files Affected**:
  - `tests/unit/test_health.py` (18 tests need conversion)
  - `tests/unit/test_main_server.py` (35+ tests need conversion)
  - Other test files using `from unittest.mock import ...`
- **Effort**: Medium (2-3 hours)
- **Dependencies**: None

#### Incomplete Test Fixture Coverage (Created: 2025-08-09)
- **Description**: Not all tests use the `mock_services` fixture where appropriate
- **Impact**: Duplicated mock setup, inconsistent service mocking
- **Solution**: Audit tests that mock MCP services and convert to use `mock_services` fixture
- **Effort**: Low (1 hour)

#### Type Checking Errors in New Code (Created: 2025-08-09 - Stream 5 Validation)
- **Description**: 27 MyPy errors in health.py, observability.py, and config.py
- **Impact**: Type safety compromised, potential runtime errors
- **Root Cause**: New health and observability modules added without full type annotation
- **Solution**: Fix type annotations, add proper return types, resolve union type handling
- **Files Affected**: 
  - `src/autodocs_mcp/health.py` (15 errors)
  - `src/autodocs_mcp/observability.py` (8 errors)  
  - `src/autodocs_mcp/config.py` (4 errors)
- **Effort**: Medium (1-2 hours)
- **Priority**: HIGH (blocks production deployment with strict typing)

### Medium Priority

#### Missing Test Parallelization Configuration (Created: 2025-08-09)
- **Description**: Added `pytest-xdist` but no configuration for optimal parallel execution
- **Impact**: Tests could run faster, CI/CD could be more efficient
- **Solution**: Add pytest configuration for parallel execution and test isolation
- **Effort**: Low (30 minutes)

#### Async Test Cleanup Issues (Created: 2025-08-09)
- **Description**: Some async tests have event loop cleanup warnings
- **Impact**: Test reliability, runtime warnings
- **Solution**: Implement proper async test teardown patterns
- **Effort**: Medium (1-2 hours)

## Code Quality Debt

### Medium Priority

#### Pydantic V1 Patterns Still Present (Created: 2025-08-09)
- **Description**: While validators were updated, some V1 patterns may remain
- **Impact**: Future Pydantic upgrade compatibility
- **Solution**: Audit codebase for remaining V1 patterns
- **Effort**: Low (1 hour)

## Infrastructure Debt

### Low Priority

#### Missing Pytest Configuration Optimization (Created: 2025-08-09)
- **Description**: Could leverage more pytest plugins and configuration
- **Impact**: Developer experience, test reliability
- **Potential Additions**:
  - `pytest-sugar` for better test output
  - `pytest-benchmark` for performance testing
  - `pytest-env` for environment variable management
- **Effort**: Low (1 hour)

## Documentation Debt

### Low Priority

#### Testing Guidelines Missing (Created: 2025-08-09)
- **Description**: No formal testing guidelines for contributors
- **Impact**: Inconsistent test patterns in future contributions
- **Solution**: Create `TESTING.md` with patterns and best practices
- **Effort**: Low (1 hour)

## Tracking Guidelines

### Debt Classification
- **High Priority**: Affects code quality, maintainability, or reliability significantly
- **Medium Priority**: Improves developer experience or performance
- **Low Priority**: Nice-to-have improvements

### Required Information
- **Description**: Clear explanation of the debt
- **Impact**: How it affects the codebase or development
- **Root Cause**: Why the debt exists (when relevant)
- **Solution**: Specific steps to address the debt
- **Effort**: Time estimate (Low: <1hr, Medium: 1-4hrs, High: >4hrs)
- **Dependencies**: Any blockers or prerequisites
- **Created**: Date when debt was identified

### Review Process
- Review this document monthly
- Update status and priorities based on project needs
- Remove completed items
- Add new debt items as they're identified

## Completion Log

### Completed Items

#### Fixed Pydantic V1 Deprecation Warnings (Completed: 2025-08-09)
- **Description**: Updated `@validator` to `@field_validator` and `@model_validator`
- **Solution**: Updated all config validation decorators
- **Effort**: Low (30 minutes)

#### Added Mock Services Fixture (Completed: 2025-08-09)
- **Description**: Missing `mock_services` fixture causing test failures
- **Solution**: Created fixture in `conftest.py` with proper service mocking
- **Effort**: Low (15 minutes)

#### Added Pytest Plugins (Completed: 2025-08-09)
- **Description**: Missing useful pytest plugins for better testing
- **Solution**: Added pytest-xdist, pytest-timeout, pytest-httpx, pytest-randomly
- **Effort**: Low (15 minutes)
