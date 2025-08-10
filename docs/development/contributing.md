# Contributing Guide

This guide walks you through the complete process of contributing to AutoDocs MCP Server, from initial setup to getting your changes merged.

## Quick Start

### 1. Set Up Your Development Environment

**Clone and Install**:
```bash
# Clone the repository
git clone https://github.com/bradleyfay/autodocs.git
cd autodocs

# Install with development dependencies
uv sync

# Verify installation
uv run python -m autodoc_mcp.main --help
```

**Verify Your Setup**:
```bash
# Run the test suite
uv run python -m pytest

# Check code quality
uv run pre-commit run --all-files

# Test MCP server startup
echo '{}' | uv run python -m autodoc_mcp.main
```

### 2. Understand the Codebase

Before making changes, familiarize yourself with:
- **[System Architecture](architecture.md)** - Understanding component organization
- **[Development Standards](standards.md)** - Code conventions and requirements
- **[Testing Guide](testing.md)** - How to write and run tests

## Development Workflow

### Step 1: Branch Management

**Check Current Branch**:
```bash
git status
git branch
```

**Create Feature Branch**:
```bash
# Always branch from develop for new features
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-description

# For bug fixes, you can branch from main if critical
git checkout main
git pull origin main
git checkout -b fix/bug-description
```

### Step 2: Make Your Changes

**Follow Development Standards**:
- Write tests for new functionality (see [Testing Guide](testing.md))
- Follow [code quality standards](standards.md#code-quality-standards)
- Use [conventional commit messages](standards.md#commit-message-standards)
- Document technical debt if making compromises

**Test Your Changes**:
```bash
# Run tests frequently during development
uv run python -m pytest tests/unit/

# Run specific tests for your changes
uv run python -m pytest tests/unit/test_your_module.py -v

# Check code quality
uv run pre-commit run --all-files
```

### Step 3: Commit Your Changes

**Stage and Commit**:
```bash
# Review your changes
git diff

# Stage changes
git add .

# Commit with conventional message
git commit -m "feat: add smart dependency context filtering

- Implement token-aware context selection
- Add runtime vs dev dependency classification
- Include configurable context scoping options

Closes #123"
```

**Pre-commit Hook Compliance**:
- Pre-commit hooks run automatically on every commit
- If hooks fail, fix the issues and commit again
- **NEVER** use `--no-verify` to bypass hooks

### Step 4: Push and Create Pull Request

**Push Your Branch**:
```bash
git push -u origin feature/your-feature-description
```

**Create Pull Request**:
1. Navigate to the GitHub repository
2. Click "Compare & pull request" for your branch
3. Fill out the PR template with:
   - Clear description of changes
   - Testing performed
   - Related issues
   - Breaking changes (if any)

## Types of Contributions

### Bug Fixes

**Process for Bug Fixes**:
1. **Reproduce the Issue**: Create a failing test that demonstrates the bug
2. **Fix the Code**: Implement the minimal fix needed
3. **Verify the Fix**: Ensure the test passes and no regressions
4. **Update Documentation**: If the bug was in documented behavior

**Example Bug Fix Workflow**:
```bash
# Create bug fix branch
git checkout -b fix/cache-corruption-on-concurrent-access

# Write failing test
# Edit tests/unit/test_cache_manager.py

# Run test to confirm failure
uv run python -m pytest tests/unit/test_cache_manager.py::test_concurrent_access -v

# Implement fix
# Edit src/autodoc_mcp/core/cache_manager.py

# Verify fix
uv run python -m pytest tests/unit/test_cache_manager.py::test_concurrent_access -v

# Commit fix
git commit -m "fix: resolve cache corruption on concurrent access

- Add file locking for cache write operations
- Implement retry logic for lock contention
- Add test coverage for concurrent cache access

Fixes #456"
```

### New Features

**Process for New Features**:
1. **Design First**: Consider architectural impact and create issue for discussion
2. **Test-Driven Development**: Write tests before implementation
3. **Incremental Implementation**: Break large features into smaller commits
4. **Documentation**: Update relevant documentation

**Example Feature Implementation**:
```bash
# Create feature branch
git checkout -b feature/add-semantic-search-filtering

# Write tests first (TDD)
# Edit tests/unit/test_context_formatter.py

# Implement feature incrementally
# Edit src/autodoc_mcp/core/context_formatter.py

# Test continuously
uv run python -m pytest tests/unit/test_context_formatter.py -v

# Update integration tests
# Edit tests/integration/test_mcp_server.py

# Update documentation
# Edit docs/product/mcp-tools.md

# Commit with conventional message
git commit -m "feat: add semantic search filtering for documentation

- Implement query-based section filtering
- Add relevance scoring for documentation sections
- Include configurable similarity threshold
- Update MCP tool to accept search queries

Closes #789"
```

### Documentation Improvements

**Types of Documentation**:
- **Code Documentation**: Docstrings, inline comments
- **User Documentation**: Setup guides, tutorials, how-to guides
- **Developer Documentation**: Architecture, contributing guides

**Documentation Standards**:
- Follow [Diátaxis framework](https://diataxis.fr/) for user documentation
- Use clear, concise language appropriate for the audience
- Include code examples and practical guidance
- Test all code examples to ensure they work

## Code Review Process

### Submitting for Review

**Before Requesting Review**:
- [ ] All tests pass locally
- [ ] Code meets quality standards (Ruff, MyPy clean)
- [ ] Documentation updated if needed
- [ ] Conventional commit messages used
- [ ] PR description is complete

**PR Description Template**:
```markdown
## Summary
Brief description of the changes and why they're needed.

## Changes Made
- Bullet point list of specific changes
- Focus on what changed, not how it was implemented

## Testing Performed
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing performed

## Related Issues
Closes #123
Related to #456

## Breaking Changes
None / Describe any breaking changes

## Additional Notes
Any additional context, deployment notes, or follow-up work needed.
```

### Review Criteria

**Technical Requirements**:
- [ ] Code follows established patterns and architecture
- [ ] Tests provide adequate coverage
- [ ] Error handling is comprehensive
- [ ] Performance impact is acceptable
- [ ] Security considerations addressed

**Quality Standards**:
- [ ] Code is readable and well-documented
- [ ] Commit messages follow conventional commits
- [ ] No pre-commit hook violations
- [ ] Technical debt is documented if introduced

### Addressing Review Feedback

**Responding to Feedback**:
1. **Address All Comments**: Respond to each review comment
2. **Make Requested Changes**: Implement suggested improvements
3. **Explain Decisions**: If you disagree, explain your reasoning
4. **Request Re-review**: After addressing feedback, request another review

**Making Review Changes**:
```bash
# Make requested changes
# Edit relevant files

# Test changes
uv run python -m pytest

# Commit additional changes
git commit -m "refactor: address review feedback

- Extract complex method into smaller functions
- Add missing error handling for edge cases
- Improve variable naming for clarity"

# Push updates
git push origin feature/your-feature-description
```

## Advanced Contributing Scenarios

### Working with Existing Issues

**Finding Issues to Work On**:
- Look for issues labeled `good-first-issue` for beginners
- Check issues labeled `help-wanted` for intermediate contributors
- Review the project roadmap for strategic contributions

**Claiming an Issue**:
1. Comment on the issue expressing interest
2. Ask questions about requirements or approach
3. Wait for maintainer acknowledgment before starting work

### Contributing to Architecture

**Major Architectural Changes**:
1. **Create RFC**: For significant changes, create a Request for Comments
2. **Discuss First**: Use GitHub Discussions for architectural conversations
3. **Prototype**: Create proof-of-concept implementations
4. **Incremental Migration**: Break changes into manageable steps

### Performance Improvements

**Performance Contribution Process**:
1. **Measure First**: Establish baseline performance metrics
2. **Identify Bottlenecks**: Use profiling tools to find actual issues
3. **Implement Optimization**: Make targeted improvements
4. **Verify Improvement**: Measure performance impact
5. **Add Benchmarks**: Include performance tests to prevent regressions

## Troubleshooting Common Issues

### Development Environment Issues

**uv Installation Problems**:
```bash
# Reinstall uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clear uv cache
uv cache clean

# Reinstall dependencies
rm -rf .venv
uv sync
```

**Test Failures**:
```bash
# Run tests with verbose output
uv run python -m pytest -v -s

# Run specific failing test
uv run python -m pytest tests/unit/test_specific.py::test_method -v -s

# Check test isolation
uv run python -m pytest --lf --tb=short
```

**Pre-commit Hook Issues**:
```bash
# Install pre-commit hooks
uv run pre-commit install

# Run hooks manually
uv run pre-commit run --all-files

# Skip specific hooks if needed (debugging only)
SKIP=mypy git commit -m "debug: temporary commit to test changes"
```

### Git Workflow Issues

**Branch Management**:
```bash
# Switch to develop branch
git checkout develop

# Update develop branch
git pull origin develop

# Rebase feature branch on latest develop
git checkout feature/your-feature
git rebase develop

# Resolve conflicts if needed
git add .
git rebase --continue
```

**Commit Message Issues**:
```bash
# Fix the last commit message
git commit --amend -m "feat: correct conventional commit message"

# Interactive rebase to fix multiple commits
git rebase -i HEAD~3
```

## Getting Help

### Resources for Contributors

- **Architecture Questions**: Review [System Architecture](architecture.md)
- **Code Standards**: Check [Development Standards](standards.md)
- **Testing Help**: See [Testing Guide](testing.md)
- **Technical Decisions**: Read [Technical Decisions](technical-decisions.md)

### Communication Channels

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For architectural discussions and questions
- **Pull Request Comments**: For code-specific discussions
- **Code Documentation**: Inline comments and docstrings for implementation details

### Contribution Recognition

Contributors are recognized through:
- GitHub contributor statistics
- Release notes acknowledgments
- Code author attribution in git history
- Community recognition for significant contributions

Thank you for contributing to AutoDocs MCP Server! Your contributions help improve AI-assisted development for the entire Python community.
