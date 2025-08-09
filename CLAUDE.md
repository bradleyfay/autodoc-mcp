# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **AutoDocs MCP Server** project - a **fully implemented** Model Context Protocol (MCP) server that automatically provides AI assistants with contextual, version-specific documentation for Python project dependencies. The goal is to eliminate manual package documentation lookup and provide more accurate AI coding assistance.

## Architecture

The project follows a modular SOLID architecture with these implemented core components:

- **dependency_parser.py**: Handles pyproject.toml parsing with graceful degradation for malformed dependencies
- **doc_fetcher.py**: PyPI JSON API integration with concurrent request handling and AI-optimized formatting
- **cache_manager.py**: Version-based JSON file caching system (no time expiration)
- **version_resolver.py**: Converts version constraints to specific versions using PyPI API
- **main.py**: FastMCP server with four MCP tools and structured logging

## MCP Tools Available

The server exposes four MCP tools:

1. **scan_dependencies**: Parse pyproject.toml and extract dependencies with graceful error handling
2. **get_package_docs**: Retrieve version-specific cached or fresh documentation from PyPI API
3. **refresh_cache**: Clear the entire documentation cache
4. **get_cache_stats**: View cache statistics and cached packages

## Key Technical Decisions

- **Version-Based Caching**: Cache key format `{package_name}-{version}` with no time expiration
- **PyPI Integration**: Uses `https://pypi.org/pypi/{package_name}/json` endpoint for both version resolution and documentation
- **Graceful Degradation**: Continues processing even with malformed dependencies or network failures
- **Transport**: stdio for MCP protocol compliance with stderr-only logging
- **Framework**: FastMCP for MCP server implementation
- **Dependencies**: httpx, pydantic, structlog, packaging, fastmcp

## Implementation Status: COMPLETE ✅

**Priority 1 (Core Validation)**: ✅ Complete
- Dependency parsing with graceful degradation
- MCP protocol integration
- Comprehensive test coverage

**Priority 2 (Documentation Fetching)**: ✅ Complete
- PyPI API integration with version resolution
- Version-based caching system
- AI-optimized documentation formatting
- Successfully tested with requests, pydantic, fastapi

## Installation & Usage

### Install the MCP Server
```bash
# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

### Development & Testing
```bash
# Test dependency scanning
uv run python scripts/dev.py test-scan

# Test documentation fetching
uv run python scripts/dev.py test-docs requests ">=2.28.0"

# Check cache stats
uv run python scripts/dev.py cache-stats

# Clear cache
uv run python scripts/dev.py clear-cache
```

### Run as MCP Server
```bash
# Start the MCP server (stdio protocol)
uv run python -m autodocs_mcp.main
```

## MCP Integration

### For Claude Code Sessions
To install this MCP server in Claude Code sessions:

```bash
# 1. Install the server in current session
uv sync

# 2. Start the MCP server (in background)
uv run python -m autodocs_mcp.main &

# 3. The server will be available with these tools:
#    - scan_dependencies: Parse project dependencies
#    - get_package_docs: Fetch package documentation
#    - refresh_cache: Clear documentation cache
#    - get_cache_stats: View cache statistics
```

### For Other AI Clients (Cursor, etc.)
MCP server configuration:
```json
{
  "mcpServers": {
    "autodocs-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "autodocs_mcp.main"],
      "cwd": "/Users/bradleyfay/autodocs",
      "env": {
        "CACHE_DIR": "~/.cache/autodocs-mcp"
      }
    }
  }
}
```

## Cache Configuration

- **Default Location**: `~/.cache/autodocs-mcp/`
- **Format**: JSON files named `{package}-{version}.json`
- **Expiration**: No time-based expiration (versions are immutable)
- **Performance**: Instant cache hits for previously fetched versions

## Development Workflow & Standards

### Git Branching Strategy

This project uses **GitFlow with Release Branches** for flexible development and bundled releases:

#### Branch Hierarchy:
- **`main`** - Production-ready code, source of truth, tagged releases only
- **`develop`** - Integration branch for ongoing development work
- **`feature/*`** - Individual features/changes, branched from `develop`
- **`release/v0.x.x`** - Release preparation, branched from `develop`

#### Daily Development Workflow:
1. **Work on develop**: Most development happens directly on `develop` branch
2. **Feature branches (optional)**: For larger changes, create `feature/description` from `develop`
3. **Merge features**: `feature/*` → `develop` (via PR or direct merge)
4. **Rapid iteration**: Small changes can be committed directly to `develop`

#### Release Workflow:
1. **Prepare release**: `git checkout -b release/v0.x.x` from `develop`
2. **Version bump**: Update version in `pyproject.toml` on release branch
3. **Final tweaks**: Bug fixes, documentation updates in release branch
4. **Deploy**: Push `release/v0.x.x` → triggers CI/CD → PyPI deployment
5. **Complete release**:
   - Merge `release/v0.x.x` → `main`
   - Tag release on `main`: `git tag v0.x.x`
   - Merge `release/v0.x.x` → `develop` (to sync any release fixes)

#### Benefits:
- **Rapid development** on `develop` without deployment pressure
- **Bundle changes** by choosing what goes into each release
- **`main` stays clean** with only completed, tested releases
- **No accidental deployments** from development work

### Commit Message Standards

**REQUIRED**: All commits MUST follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Commit Types:
- **feat**: New feature (triggers MINOR version bump)
- **fix**: Bug fix (triggers PATCH version bump)
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring without feature/bug changes
- **test**: Adding or updating tests
- **chore**: Build process, dependency updates, etc.
- **ci**: CI/CD pipeline changes

#### Breaking Changes:
- Add `!` after type: `feat!: redesign API interface` (triggers MAJOR version bump)
- Or include `BREAKING CHANGE:` in footer

#### Examples:
```bash
feat: add semantic search for package documentation
fix: resolve cache corruption on network timeouts
docs: update MCP integration examples
chore: bump dependencies to latest versions
ci: add automated security scanning
```

### Semantic Versioning (SemVer)

This project strictly follows [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** (`1.0.0`): Breaking changes, incompatible API changes
- **MINOR** (`0.1.0`): New features, backward-compatible functionality
- **PATCH** (`0.0.1`): Bug fixes, backward-compatible fixes

#### Version Bumping Rules:
- `feat:` commits → MINOR version bump
- `fix:` commits → PATCH version bump
- `feat!:` or `BREAKING CHANGE:` → MAJOR version bump
- Other commit types → No automatic version bump

#### Release Process:
1. Update `CHANGELOG.md` with all changes since last version
2. Bump version in `pyproject.toml`
3. Commit: `chore: bump version to v1.2.3`
4. Create and push tag: `git tag v1.2.3 && git push --tags`
5. GitHub Actions automatically deploys to PyPI

### Changelog Management

**REQUIRED**: Update `CHANGELOG.md` with every version bump using [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [1.2.3] - 2025-08-07

### Added
- New features and capabilities

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Now removed features

### Fixed
- Bug fixes

### Security
- Vulnerability fixes
```

## Claude Code Instructions

### Technical Debt Management

**MANDATORY**: All technical debt MUST be documented using disciplined tracking strategies:

#### When to Log Technical Debt
- **During Development**: When making compromises due to time constraints
- **During Refactoring**: When identifying improvement opportunities
- **During Code Review**: When spotting inconsistencies or anti-patterns
- **During Bug Fixes**: When finding root causes that indicate deeper issues

#### Technical Debt Documentation Requirements
1. **Location**: Document in `planning/technical_debt.md`
2. **Classification**: High/Medium/Low priority based on impact
3. **Required Fields**: Description, Impact, Root Cause, Solution, Effort Estimate, Dependencies
4. **Dating**: Always include creation date
5. **Ownership**: Assign to specific areas (testing, infrastructure, code quality, etc.)

#### Standard Technical Debt Categories
- **Code Quality**: Inconsistent patterns, deprecated usage, code smells
- **Testing Infrastructure**: Missing tests, inconsistent mocking, test reliability
- **Documentation**: Missing or outdated docs, unclear APIs
- **Infrastructure**: Build issues, deployment problems, environment inconsistencies
- **Performance**: Known bottlenecks, scalability concerns
- **Security**: Vulnerabilities, insecure patterns, missing validations

#### Technical Debt Review Process
- **Monthly Reviews**: Assess priority and status
- **Before Major Releases**: Address high-priority items
- **During Refactoring**: Target related debt items
- **Completion Logging**: Move completed items to completion log

### Third-Party Dependencies Philosophy

**PRINCIPLE**: Lean heavily on widely-accepted third-party packages to build robust software. Do NOT reinvent the wheel.

#### Dependency Guidelines
1. **Favor Established Ecosystems**: Prefer packages from well-known ecosystems (pytest plugins, FastAPI ecosystem, etc.)
2. **Quality Indicators**: Look for packages with:
   - Active maintenance (recent commits/releases)
   - Good documentation
   - Strong community adoption
   - Comprehensive test coverage
   - Clear versioning/changelog
3. **Testing Dependencies**: Be especially liberal with testing dependencies - they don't affect production
4. **Development Dependencies**: Add tooling that improves developer experience without hesitation

#### Pytest Plugin Philosophy
The pytest ecosystem is mature and battle-tested. **Always prefer pytest plugins** over custom solutions:

- **pytest-mock**: For all mocking needs (never use unittest.mock directly)
- **pytest-asyncio**: For async test handling
- **pytest-cov**: For coverage reporting
- **pytest-xdist**: For parallel test execution
- **pytest-timeout**: For test timeout management
- **pytest-httpx**: For HTTP client mocking
- **pytest-randomly**: For test order randomization
- **pytest-sugar**: For better test output
- **pytest-benchmark**: For performance testing

#### When to Add Dependencies
- **Testing Improvements**: Always acceptable
- **Developer Experience**: Tools that speed up development
- **Standard Patterns**: Libraries that implement well-established patterns
- **Security**: Libraries that improve security posture
- **Performance**: Well-maintained libraries that solve performance issues

#### When to be Cautious
- **Core Runtime Dependencies**: Evaluate carefully but don't avoid unnecessarily
- **Bleeding Edge**: Avoid alpha/beta packages for core functionality
- **Unmaintained**: Check maintenance status before adding
- **License Conflicts**: Ensure license compatibility

### Mandatory Workflow Requirements

When working in this repository, you MUST:

1. **Work primarily on `develop` branch** - Most development happens on `develop`, not `main`
2. **Always use conventional commits** - Every commit message must follow the conventional commits specification
3. **Use release branches for deployment** - Only `release/v0.x.x` branches trigger PyPI deployment
4. **Follow SemVer** - Version bumps must match the type of changes made
5. **Update CHANGELOG.md with releases** - Add entries when creating release branches
6. **Document technical debt** - Log any compromises or future improvements in `planning/technical_debt.md`

### Branch Management for Development

**MANDATORY**: Before making any code changes, you MUST:

1. **Check current branch**: Always run `git branch` or `git status` first
2. **Default to develop branch**: Most work should happen on `develop` branch
3. **Create feature branch for large changes**: For significant features, create `feature/description` from `develop`
4. **Never commit directly to main** - `main` is only for completed releases

### Branch Management for Development

**MANDATORY**: Before making any code changes, you MUST:

1. **Check current branch**: Always run `git branch` or `git status` first
2. **Create feature branch if on main**: If currently on `main` branch, immediately create and switch to a feature branch before any code modifications:
   ```bash
   git checkout -b feature/description-of-changes
   ```
3. **Use descriptive branch names**: `feature/add-search`, `fix/cache-corruption`, `docs/update-readme`
4. **Never commit directly to main** - All development work must happen on feature branches

This ensures we follow the mandatory PR workflow from the start of development.

### Commit Message Examples

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

### Version Bump Protocol

When bumping versions:

1. **Update CHANGELOG.md first** with all changes since last version
2. **Bump version in pyproject.toml** following SemVer rules
3. **Commit with conventional message**: `chore: bump version to v1.2.3`
4. **Create and push tag**: `git tag v1.2.3 && git push --tags`

### Pre-commit Hook Integration

All commits automatically run:
- Ruff linting and formatting
- MyPy type checking
- File hygiene checks
- YAML validation

**CRITICAL RULE**: If pre-commit hooks fail, you MUST fix the issues and commit again.

**STRICTLY FORBIDDEN**: Never use `git commit --no-verify` or `git commit -n` to bypass pre-commit hooks. This defeats the purpose of code quality enforcement and can introduce bugs, formatting inconsistencies, and security vulnerabilities.

**Required Process**:
1. Run `pre-commit run --all-files` to identify all issues
2. Fix each identified issue properly in the code
3. Commit normally with all hooks passing
4. If you accidentally bypassed hooks, amend the commit with fixes immediately

### Testing Standards and Consistency

**MANDATORY**: All testing must follow consistent patterns and use pytest ecosystem tools:

#### Mock Usage Standards
- **ALWAYS use pytest-mock**: Import `mocker` fixture, never `from unittest.mock import`
- **Use mock_services fixture**: For MCP tool tests, use the provided `mock_services` fixture from conftest.py
- **Pattern**: `def test_something(self, mocker):` or `def test_something(self, mock_services, mocker):`
- **No unittest.mock**: The following are **FORBIDDEN** in new code:
  ```python
  # FORBIDDEN
  from unittest.mock import patch, AsyncMock, MagicMock
  with patch("module.service") as mock:
      pass

  # CORRECT
  def test_something(self, mocker):
      mock_service = mocker.patch("module.service")
      mock_async = mocker.AsyncMock()
      mock_regular = mocker.MagicMock()
  ```

#### Test Fixture Usage
- **Use mock_services**: For tests involving MCP tools (scan_dependencies, get_package_docs, etc.)
- **Consistent Setup**: Don't duplicate service mocking when fixtures exist
- **Proper Isolation**: Each test should be independent

#### Testing Patterns
- **Async Tests**: Always use `@pytest.mark.asyncio` for async test functions
- **Error Testing**: Test both success and failure paths
- **Mock Verification**: Verify mock calls when testing interactions
- **Clear Assertions**: Use descriptive assertions with clear failure messages

#### When Adding New Tests
1. Check if existing fixtures can be reused
2. Use pytest-mock patterns exclusively
3. Follow the established naming conventions
4. Include both positive and negative test cases
5. Document any new fixtures in conftest.py

## Future Development

Ready for **Priority 3** (Graceful Degradation) and **Priority 4** (Dependency Context) based on `planning/implementation_priorities.md`. Current implementation already includes significant graceful degradation features.
