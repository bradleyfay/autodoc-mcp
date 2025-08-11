# Cross-Project Shared Standards

**Last Updated**: August 11, 2025
**Standards Owner**: Development Team
**Review Frequency**: Quarterly

## 🎯 Purpose & Scope

### Objectives
- Ensure consistency across all projects in the portfolio
- Reduce cognitive overhead when switching between projects
- Establish quality baselines for all development work
- Facilitate knowledge sharing and team collaboration

### Covered Areas
- Development practices and code standards
- Documentation and communication standards
- Project management and planning processes
- Quality assurance and testing approaches
- Security and compliance requirements

---

## 💻 Development Standards

### Code Quality Standards

#### Python Development (AutoDocs MCP, Task Graph System)
- **Formatter**: Ruff (replaces Black + isort)
- **Linter**: Ruff (replaces Flake8 + various plugins)
- **Type Checking**: MyPy with strict configuration
- **Import Organization**: Ruff with predefined categories

```python
# Standard import order
import os                    # Standard library
import sys

import httpx                 # Third-party
import pydantic

from autodocs_mcp.core import config  # Local imports
from autodocs_mcp.models import Response
```

#### Web Development (Documentation Site)
- **Framework**: Modern JavaScript/TypeScript framework (React, Next.js, etc.)
- **Styling**: CSS-in-JS or Tailwind CSS for consistency
- **Build Tools**: Vite or Next.js build system
- **Package Manager**: npm or yarn with lock file commitment

### Version Control Standards

#### Commit Message Convention
**MANDATORY**: All projects use [Conventional Commits](https://www.conventionalcommits.org/)

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types**:
- `feat`: New feature (MINOR version bump)
- `fix`: Bug fix (PATCH version bump)
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/modifications
- `chore`: Build process, dependencies, etc.
- `ci`: CI/CD pipeline changes

**Breaking Changes**: Add `!` after type or include `BREAKING CHANGE:` in footer (MAJOR version bump)

#### Branch Strategy
All projects follow **GitFlow with Release Branches**:
- **`main`**: Production-ready code only
- **`develop`**: Integration branch for ongoing development
- **`feature/*`**: Individual features from `develop`
- **`release/v0.x.x`**: Release preparation from `develop`

### Pre-commit Standards

#### Required Pre-commit Hooks (All Projects)
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

**CRITICAL RULE**: Never use `--no-verify` or `-n` flags to bypass pre-commit hooks
**Process**: Fix issues identified by hooks before committing

---

## 📚 Documentation Standards

### Documentation Hierarchy
All projects maintain consistent documentation structure:

```
docs/
├── README.md              # Quick start and overview
├── ARCHITECTURE.md        # System design and components
├── DEVELOPMENT.md         # Developer setup and workflows
├── API.md                # API documentation (if applicable)
├── DEPLOYMENT.md          # Deployment and operations
└── CHANGELOG.md           # Version history
```

### Markdown Standards

#### Required Front Matter (Planning Documents)
```markdown
# Document Title

**Last Updated**: [Date]
**Owner**: [Responsible person/team]
**Review Date**: [Next scheduled review]
```

#### Documentation Quality Standards
- **Clarity**: Use simple, direct language
- **Completeness**: Cover all necessary information for target audience
- **Accuracy**: Keep documentation synchronized with implementation
- **Accessibility**: Structure for easy navigation and search

### Code Documentation

#### Python Docstring Standard
```python
def get_package_docs(package_name: str, version_constraint: str = None) -> dict:
    """Retrieve documentation for a package with version-based caching.

    Args:
        package_name: Name of the package to fetch documentation for
        version_constraint: Version constraint from dependency scanning

    Returns:
        Formatted documentation with package metadata

    Raises:
        ValidationError: If package_name is invalid
        NetworkError: If PyPI API is unavailable
    """
```

#### API Documentation
- **OpenAPI/Swagger**: For REST APIs
- **MCP Tool Schemas**: JSON Schema for MCP tools
- **Examples**: Always include usage examples
- **Error Codes**: Document all error conditions

---

## 🏗️ Project Structure Standards

### Standard Project Layout

#### Python Projects
```
project-name/
├── src/project_name/      # Source code
├── tests/                 # Test suite
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── .github/               # GitHub workflows
├── pyproject.toml         # Project configuration
├── README.md              # Project overview
└── CLAUDE.md              # Claude Code instructions
```

#### Web Projects
```
project-name/
├── src/                   # Source code
├── public/                # Static assets
├── tests/                 # Test suite
├── docs/                  # Documentation
├── .github/               # GitHub workflows
├── package.json           # Dependencies and scripts
├── README.md              # Project overview
└── CLAUDE.md              # Claude Code instructions
```

### Configuration Management
- **Environment Variables**: Use `.env` files for local development
- **Configuration Classes**: Pydantic models for Python projects
- **Validation**: All configuration inputs must be validated
- **Documentation**: Document all configuration options

---

## 🧪 Testing Standards

### Testing Framework Standards

#### Python Projects (pytest ecosystem)
```python
# Required testing dependencies
pytest
pytest-asyncio            # Async test support
pytest-mock              # Mocking (replaces unittest.mock)
pytest-cov               # Coverage reporting
pytest-xdist             # Parallel test execution
pytest-httpx             # HTTP client testing
```

**MANDATORY**: Always use `pytest-mock` fixture, never `unittest.mock` directly
```python
# CORRECT
def test_something(mocker):
    mock_service = mocker.patch("module.service")

# INCORRECT
from unittest.mock import patch
```

#### Testing Patterns
- **Arrange-Act-Assert**: Clear test structure
- **Descriptive Names**: Test names describe what they verify
- **Independent Tests**: No test dependencies or shared state
- **Comprehensive Coverage**: >90% code coverage target

### Quality Gates
All projects maintain these quality standards:
- **Test Coverage**: Minimum 90%, target 95%+
- **Type Coverage**: 100% type annotations in Python
- **Linting**: Zero linting errors or warnings
- **Security**: No known vulnerabilities in dependencies

---

## 🔒 Security Standards

### Security Practices
- **Input Validation**: All external inputs validated and sanitized
- **Error Handling**: No sensitive information in error messages
- **Dependencies**: Regular security scanning and updates
- **Secrets Management**: No secrets in code or configuration files

### Security Tools
- **Dependency Scanning**: Regular vulnerability assessments
- **Static Analysis**: Security-focused code analysis
- **Environment Isolation**: Development/staging/production separation
- **Access Control**: Principle of least privilege

---

## 📊 Quality Assurance Standards

### Definition of Done
Every deliverable meets these criteria:
- [ ] **Functional**: All acceptance criteria met
- [ ] **Tested**: Comprehensive test coverage with passing tests
- [ ] **Documented**: User and developer documentation updated
- [ ] **Reviewed**: Code review completed and approved
- [ ] **Quality**: Passes all quality gates (linting, type checking, security)
- [ ] **Performance**: Meets performance requirements
- [ ] **Accessible**: Documentation and interfaces are accessible

### Code Review Standards
- **Mandatory Reviews**: All code changes require review
- **Review Criteria**: Functionality, design, tests, documentation
- **Feedback Quality**: Constructive, specific, actionable feedback
- **Response Time**: Reviews completed within 24 hours

### Performance Standards
- **Response Times**: API endpoints respond within 2 seconds
- **Memory Usage**: Efficient memory utilization with proper cleanup
- **Scalability**: Design for expected load with room for growth
- **Monitoring**: Performance metrics collection and alerting

---

## 🚀 Deployment & Operations Standards

### Deployment Practices
- **Automated Deployment**: CI/CD pipelines for all projects
- **Environment Consistency**: Infrastructure as code where possible
- **Rollback Capability**: Ability to revert deployments quickly
- **Health Checks**: Comprehensive health and readiness checks

### Monitoring & Observability
- **Logging**: Structured logging with consistent formats
- **Metrics**: Key performance and business metrics collection
- **Alerting**: Proactive alerting for critical issues
- **Tracing**: Request tracing for complex interactions

### Configuration Management
- **Environment Variables**: Consistent configuration approach
- **Secrets Management**: Secure handling of sensitive configuration
- **Feature Flags**: Ability to enable/disable features dynamically
- **Documentation**: All configuration options documented

---

## 📈 Process Standards

### Agile Practices
- **Sprint Planning**: Regular planning sessions with clear objectives
- **Daily Stand-ups**: Brief progress and blocker discussions
- **Retrospectives**: Regular process improvement sessions
- **Continuous Improvement**: Apply lessons learned to future work

### Communication Standards
- **Status Updates**: Regular project status communication
- **Decision Documentation**: Record important decisions and rationale
- **Knowledge Sharing**: Regular sharing of learnings and best practices
- **Stakeholder Updates**: Consistent communication with stakeholders

### Planning & Tracking
- **User Stories**: Clear, testable acceptance criteria
- **Estimation**: Consistent estimation approaches across projects
- **Progress Tracking**: Regular milestone and progress assessment
- **Risk Management**: Proactive risk identification and mitigation

---

## 🔄 Standards Evolution & Compliance

### Standards Maintenance
- **Quarterly Reviews**: Assess standards effectiveness and relevance
- **Industry Alignment**: Keep standards aligned with industry best practices
- **Tool Updates**: Regularly update tools and dependencies
- **Team Feedback**: Incorporate team suggestions for improvements

### Compliance Monitoring
- **Automated Checks**: Use tools to enforce standards automatically
- **Regular Audits**: Periodic compliance assessment across projects
- **Training**: Ensure team understands and can apply standards
- **Continuous Improvement**: Refine standards based on experience

### Exception Process
- **Justification Required**: Documented rationale for standards exceptions
- **Time-Limited**: Exceptions have expiration dates
- **Review Process**: Regular review of active exceptions
- **Migration Plan**: Plan to return to standard practices

---

## 📞 Standards Support

### Getting Help
- **Documentation**: Comprehensive standards documentation and examples
- **Team Consultation**: Discuss standards questions with team leads
- **Tool Support**: Automated tooling to enforce and guide standards
- **Training Resources**: Learning materials for standards adoption

### Feedback & Improvement
- **Standards Feedback**: Process for suggesting improvements
- **Implementation Support**: Help with standards adoption
- **Tool Requests**: Process for requesting new tools or capabilities
- **Best Practice Sharing**: Mechanisms for sharing successful patterns

---

*Shared standards established: August 11, 2025*
*Next review: November 11, 2025*
*Standards version: 1.0*
