# Development Standards

This reference document specifies the development standards, conventions, and requirements for AutoDocs MCP Server. All contributors must follow these standards to maintain code quality and consistency.

## Git Branching Strategy

### GitFlow with Release Branches

The project uses **GitFlow with Release Branches** for flexible development and bundled releases:

#### Branch Hierarchy
- **`main`** - Production-ready code, source of truth, tagged releases only
- **`develop`** - Integration branch for ongoing development work
- **`feature/*`** - Individual features/changes, branched from `develop`
- **`release/v0.x.x`** - Release preparation, branched from `develop`

#### Daily Development Workflow
1. **Work on develop**: Most development happens directly on `develop` branch
2. **Feature branches (optional)**: For larger changes, create `feature/description` from `develop`
3. **Merge features**: `feature/*` → `develop` (via PR or direct merge)
4. **Rapid iteration**: Small changes can be committed directly to `develop`

#### Release Workflow
1. **Prepare release**: `git checkout -b release/v0.x.x` from `develop`
2. **Version bump**: Update version in `pyproject.toml` on release branch
3. **Final tweaks**: Bug fixes, documentation updates in release branch
4. **Deploy**: Push `release/v0.x.x` → triggers CI/CD → PyPI deployment
5. **Complete release**:
   - Merge `release/v0.x.x` → `main`
   - Tag release on `main`: `git tag v0.x.x`
   - Merge `release/v0.x.x` → `develop` (to sync any release fixes)

## Commit Message Standards

**REQUIRED**: All commits MUST follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types
- **feat**: New feature (triggers MINOR version bump)
- **fix**: Bug fix (triggers PATCH version bump)
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring without feature/bug changes
- **test**: Adding or updating tests
- **chore**: Build process, dependency updates, etc.
- **ci**: CI/CD pipeline changes

### Breaking Changes
- Add `!` after type: `feat!: redesign API interface` (triggers MAJOR version bump)
- Or include `BREAKING CHANGE:` in footer

### Examples
```bash
# ✅ GOOD - Conventional commits
feat: add query filtering for documentation search
fix: resolve cache corruption on concurrent access
docs: update installation instructions for Claude Code
chore: bump dependencies to latest versions

# ❌ BAD - Non-conventional commits
Add new feature
Fixed bug
Updated docs
```

## Semantic Versioning

**REQUIRED**: This project strictly follows [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** (`1.0.0`): Breaking changes, incompatible API changes
- **MINOR** (`0.1.0`): New features, backward-compatible functionality
- **PATCH** (`0.0.1`): Bug fixes, backward-compatible fixes

### Version Bumping Rules
- `feat:` commits → MINOR version bump
- `fix:` commits → PATCH version bump
- `feat!:` or `BREAKING CHANGE:` → MAJOR version bump
- Other commit types → No automatic version bump

## Code Quality Standards

### Type Safety
- **MyPy Required**: All code must pass strict MyPy type checking
- **Type Annotations**: All function parameters and return types must be annotated
- **Pydantic Models**: Use Pydantic v2 for all data structures and validation

### Code Style
- **Ruff Linting**: All code must pass Ruff linting without warnings
- **Automatic Formatting**: Use Ruff format for consistent code formatting
- **Import Organization**: Follow Ruff's import sorting rules

### Documentation
- **Docstrings**: All public functions and classes must have comprehensive docstrings
- **Inline Comments**: Complex logic should include explanatory comments
- **Type Hints**: Prefer type hints over docstring type documentation

## Testing Standards

### Coverage Requirements
- **Minimum Coverage**: 80% overall test coverage required
- **Critical Path Coverage**: 100% coverage for error handling and security validation
- **Integration Tests**: All MCP tools must have integration test coverage

### Testing Patterns
- **pytest-mock Required**: Use `pytest-mock` exclusively, never `unittest.mock`
- **Async Testing**: Use `@pytest.mark.asyncio` for all async test functions
- **Mock Services**: Use provided `mock_services` fixture for MCP tool tests
- **Clear Assertions**: Use descriptive assertions with clear failure messages

### Test Organization
```
tests/
├── unit/           # Unit tests for individual modules
├── integration/    # Integration tests for MCP tools and end-to-end flows
└── conftest.py     # Shared fixtures and test configuration
```

## Dependency Management

### Philosophy
**Principle**: Lean heavily on widely-accepted third-party packages. Do NOT reinvent the wheel.

### Dependency Guidelines
1. **Favor Established Ecosystems**: Prefer packages from well-known ecosystems (pytest plugins, FastAPI ecosystem)
2. **Quality Indicators**: Look for packages with:
   - Active maintenance (recent commits/releases)
   - Good documentation and community adoption
   - Comprehensive test coverage
   - Clear versioning/changelog

### When to Add Dependencies
- **Testing Improvements**: Always acceptable
- **Developer Experience**: Tools that speed up development
- **Standard Patterns**: Libraries that implement well-established patterns
- **Security**: Libraries that improve security posture
- **Performance**: Well-maintained libraries that solve performance issues

## Pre-commit Requirements

### Automated Checks
All commits automatically run:
- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **File Hygiene**: File permissions, line endings, YAML validation

### Critical Rule
**STRICTLY FORBIDDEN**: Never use `git commit --no-verify` or `git commit -n` to bypass pre-commit hooks.

**Required Process**:
1. Run `pre-commit run --all-files` to identify issues
2. Fix each identified issue properly in the code
3. Commit normally with all hooks passing
4. If you accidentally bypassed hooks, amend the commit with fixes immediately

## Technical Debt Management

### Documentation Requirement
**MANDATORY**: All technical debt MUST be documented in `planning/technical_debt.md`

### When to Log Technical Debt
- During development when making compromises due to time constraints
- During refactoring when identifying improvement opportunities
- During code review when spotting inconsistencies or anti-patterns
- During bug fixes when finding root causes that indicate deeper issues

### Required Documentation Fields
- **Description**: Clear explanation of the debt
- **Impact**: How it affects the codebase or development
- **Root Cause**: Why the debt exists (when relevant)
- **Solution**: Specific steps to address the debt
- **Effort**: Time estimate (Low: <1hr, Medium: 1-4hrs, High: >4hrs)
- **Created**: Date when debt was identified

### Technical Debt Categories
- **Code Quality**: Inconsistent patterns, deprecated usage, code smells
- **Testing Infrastructure**: Missing tests, inconsistent mocking, test reliability
- **Documentation**: Missing or outdated docs, unclear APIs
- **Infrastructure**: Build issues, deployment problems, environment inconsistencies
- **Performance**: Known bottlenecks, scalability concerns
- **Security**: Vulnerabilities, insecure patterns, missing validations

## Code Organization Standards

### Module Structure
```
src/autodocs_mcp/
├── main.py              # FastMCP server entry point
├── config.py            # Configuration management
├── models.py            # Pydantic data models
├── exceptions.py        # Custom exception hierarchy
├── security.py          # Input validation and security
├── health.py            # Health checks and monitoring
├── observability.py     # Metrics and logging
└── core/                # Core business logic
    ├── dependency_parser.py
    ├── version_resolver.py
    ├── doc_fetcher.py
    ├── cache_manager.py
    └── ...
```

### Import Standards
```python
# Standard library imports first
import asyncio
import json
from pathlib import Path

# Third-party imports second
import httpx
from pydantic import BaseModel

# Local imports last
from autodocs_mcp.config import Config
from autodocs_mcp.core.cache_manager import CacheManager
```

### Naming Conventions
- **Files**: Snake case (`dependency_parser.py`)
- **Classes**: PascalCase (`DependencyParser`)
- **Functions/Variables**: Snake case (`parse_dependencies`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_CACHE_SIZE`)

## Error Handling Standards

### Exception Hierarchy
- Use custom exceptions from `exceptions.py`
- Include context information in all custom exceptions
- Provide actionable error messages with recovery suggestions

### Logging Standards
- Use structured logging with context preservation
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Never log sensitive information (API keys, user data)
- Include request context in all log messages

## Performance Standards

### Resource Management
- Use async context managers for all resources
- Implement proper connection pooling
- Set appropriate timeouts for all external requests
- Monitor memory usage and implement cleanup

### Caching Standards
- Use version-based immutable cache keys
- Implement cache corruption detection and recovery
- Monitor cache hit rates and performance
- Set appropriate cache size limits

## Security Standards

### Input Validation
- Validate and sanitize all user inputs
- Use Pydantic models for structured validation
- Implement path traversal prevention
- Validate all external URLs and endpoints

### Resource Protection
- Implement rate limiting for external API calls
- Set memory usage limits and monitoring
- Use secure temporary file handling
- Prevent information disclosure in error messages

## Configuration Standards

### Environment Variables
- Use clear, descriptive environment variable names
- Provide sensible defaults for all configuration
- Validate all configuration at startup
- Support multiple environments (dev, test, prod)

### Configuration Management
```python
# Use Pydantic for configuration validation
class Config(BaseModel):
    cache_dir: Path = Path.home() / ".cache" / "autodoc-mcp"
    max_cache_size: int = 1000
    request_timeout: int = 30

    @field_validator('cache_dir')
    @classmethod
    def validate_cache_dir(cls, v: Path) -> Path:
        v.mkdir(parents=True, exist_ok=True)
        return v
```

These standards ensure consistent, high-quality code that is maintainable, secure, and performant. All contributors must adhere to these standards, and pull requests that don't meet these requirements will be rejected.
