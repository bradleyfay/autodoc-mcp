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

This project uses **GitHub Flow** with feature branches and squash merging:

- **`main` branch**: Production-ready code, always deployable
- **Feature branches**: `feature/description` or `fix/description` for all changes
- **Release process**: Squash-merge feature branches into main, then tag for release

#### Workflow Steps:
1. Create feature branch from `main`: `git checkout -b feature/add-new-feature`
2. Make commits with conventional commit messages (see below)
3. Push feature branch: `git push -u origin feature/add-new-feature`
4. **Create Pull Request on GitHub** - All changes must go through PR review
5. **Wait for PR approval** - No direct commits to `main` branch allowed
6. **Squash-merge** PR into `main` (this creates a single commit)
7. Tag the squashed commit for releases: `git tag v1.2.3`
8. Push tags to trigger CI/CD deployment: `git push --tags`

#### Pull Request Requirements:
- **Mandatory PR review** - All feature branches must be merged via GitHub Pull Request
- **No direct commits to `main`** - Main branch should be protected with branch protection rules
- **PR title must follow conventional commits** - Use same format as commit messages
- **Include clear description** - Explain what changes were made and why
- **Link related issues** - Reference any GitHub issues being addressed

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

### Mandatory Workflow Requirements

When working in this repository, you MUST:

1. **Always use conventional commits** - Every commit message must follow the conventional commits specification
2. **Update CHANGELOG.md with every version bump** - Add entries following Keep a Changelog format
3. **Use feature branches with mandatory PRs** - Never commit directly to main branch, all changes must go through GitHub Pull Request review
4. **Follow SemVer** - Version bumps must match the type of changes made
5. **Require PR approval** - All Pull Requests must be reviewed and approved before merging

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

If pre-commit hooks fail, fix the issues and commit again.

## Future Development

Ready for **Priority 3** (Graceful Degradation) and **Priority 4** (Dependency Context) based on `planning/implementation_priorities.md`. Current implementation already includes significant graceful degradation features.
