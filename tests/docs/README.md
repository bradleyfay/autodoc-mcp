# Documentation Testing Framework

This directory contains a comprehensive testing framework for the AutoDocs documentation site. The framework ensures documentation quality, accessibility, and reliability through automated testing.

## Overview

The documentation testing framework provides:

- **Automated Link Validation**: Tests all internal and external links
- **Content Validation**: Validates HTML structure, code examples, and accessibility
- **Cross-Platform Testing**: Tests across different browsers and device sizes
- **Quality Assurance**: Structured QA checklists and processes
- **CI/CD Integration**: Automated testing in GitHub Actions

## Test Structure

```
tests/docs/
├── __init__.py                    # Package initialization
├── conftest.py                    # Pytest configuration and fixtures
├── test_link_validation.py        # Link validation tests
├── test_content_validation.py     # Content and HTML validation tests
├── test_cross_platform.py         # Cross-platform browser tests
├── qa_checklists.py               # QA checklists and processes
└── README.md                      # This file
```

## Quick Start

### Prerequisites

1. **Install dependencies**:
   ```bash
   uv pip install -e ".[docs-testing]"
   ```

2. **Build documentation** (if not already built):
   ```bash
   mkdocs build
   ```

3. **For cross-platform testing**, install Playwright:
   ```bash
   uv pip install playwright
   playwright install
   ```

### Running Tests

#### Using the Test Script (Recommended)

```bash
# Quick validation tests
python scripts/test_docs.py quick

# Comprehensive test suite
python scripts/test_docs.py full

# External link validation only
python scripts/test_docs.py external-links

# Cross-platform tests only
python scripts/test_docs.py cross-platform
```

#### Using pytest Directly

```bash
# Run all documentation tests
pytest tests/docs/

# Run specific test suites
pytest tests/docs/test_link_validation.py
pytest tests/docs/test_content_validation.py
pytest tests/docs/test_cross_platform.py
pytest tests/docs/qa_checklists.py

# Run with specific markers
pytest tests/docs/ -m "not slow"           # Skip slow tests
pytest tests/docs/ -m "not external"       # Skip external link tests
pytest tests/docs/ -m "not browser"        # Skip browser tests
```

## Test Categories

### 1. Link Validation (`test_link_validation.py`)

Tests all links in the documentation for validity and accessibility.

**Features:**
- Internal link validation against file system
- External link validation with retry logic
- Asset link validation (CSS, JS, images)
- Fragment identifier validation
- Navigation structure testing

**Key Tests:**
- `test_internal_links_validation()` - Validates internal links
- `test_asset_links_validation()` - Validates asset links
- `test_external_links_validation()` - Validates external links
- `test_navigation_structure_completeness()` - Tests navigation
- `test_fragment_links_validation()` - Tests anchor links

### 2. Content Validation (`test_content_validation.py`)

Validates content quality, structure, and accessibility compliance.

**Features:**
- HTML structure and semantic validation
- Code example syntax validation
- Accessibility compliance (WCAG guidelines)
- SEO metadata validation
- Content consistency checking

**Key Tests:**
- `test_html_structure_validation()` - HTML structure and semantics
- `test_code_examples_validation()` - Code block syntax
- `test_accessibility_compliance()` - WCAG accessibility
- `test_seo_metadata_validation()` - SEO and metadata
- `test_content_consistency()` - Cross-page consistency

### 3. Cross-Platform Testing (`test_cross_platform.py`)

Tests functionality across different browsers and devices.

**Features:**
- Multi-browser compatibility (Chrome, Firefox, Safari)
- Mobile responsiveness testing
- Performance benchmarking
- JavaScript functionality validation
- Touch interaction testing

**Key Tests:**
- `test_browser_compatibility()` - Cross-browser testing
- `test_mobile_responsiveness()` - Mobile device testing
- `test_performance_benchmarks()` - Performance testing
- `test_javascript_functionality()` - JS functionality

### 4. Quality Assurance (`qa_checklists.py`)

Structured QA processes and checklists for quality gates.

**Features:**
- Pre-deployment validation checklists
- Content update verification procedures
- Release quality gates
- Automated QA workflow management
- Comprehensive reporting

**Key Checklists:**
- `pre_deployment` - Essential pre-deployment checks
- `content_update` - Post-content-update validation
- `release` - Comprehensive release validation

## Configuration

### Pytest Configuration

The framework uses pytest markers for organizing tests:

```ini
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "external: marks tests requiring network access",
    "browser: marks tests requiring browser automation"
]
```

### Test Selection

```bash
# Quick tests only
pytest tests/docs/ -m "not slow"

# Skip network-dependent tests
pytest tests/docs/ -m "not external"

# Skip browser tests
pytest tests/docs/ -m "not browser"

# Run only specific severity
pytest tests/docs/ -k "not external_links"
```

## CI/CD Integration

### GitHub Actions Workflow

The framework integrates with GitHub Actions via `.github/workflows/docs-testing.yml`:

- **Quick Validation**: Runs on every commit
- **Comprehensive Testing**: Runs on main/develop branches and PRs
- **External Link Validation**: Runs daily to catch link rot
- **Performance Testing**: Runs on main branch pushes

### Workflow Triggers

- **Push to main/develop**: Full test suite
- **Pull Requests**: Comprehensive testing with PR comments
- **Daily Schedule**: External link validation
- **Manual Trigger**: Configurable test levels

## Reporting

### Test Reports

The framework generates multiple report formats:

- **HTML Reports**: Human-readable test results
- **JSON Reports**: Machine-readable for CI integration
- **Summary Reports**: High-level overview
- **Performance Reports**: Lighthouse performance data

### Report Locations

```bash
reports/
├── link-validation-report.html
├── link-validation.json
├── content-validation-report.html
├── content-validation.json
├── cross-platform-report.html
├── cross-platform.json
├── qa-checklists-report.html
├── qa-checklists.json
└── test-summary.json
```

## Extending the Framework

### Adding New Tests

1. **Create test file** in `tests/docs/`
2. **Follow naming convention**: `test_*.py`
3. **Use existing fixtures** from `conftest.py`
4. **Add appropriate markers**
5. **Update CI workflow** if needed

### Adding New QA Checks

```python
def check_custom_requirement(qa_validator: QAValidator) -> QACheckResult:
    """Custom QA check implementation."""
    # Implement your check logic
    return QACheckResult(
        check_name="custom_requirement",
        status=QAStatus.PASSED,  # or FAILED
        severity=QASeverity.MEDIUM,
        message="Check description"
    )
```

### Creating Custom Checklists

```python
def create_custom_checklist() -> QAChecklist:
    """Create custom QA checklist."""
    return QAChecklist(
        name="custom_checklist",
        description="Description of checklist purpose",
        checks=[
            check_custom_requirement,
            # Add more checks
        ]
    )
```

## Troubleshooting

### Common Issues

1. **Site not built**: Run `mkdocs build` first
2. **Missing dependencies**: Install with `uv pip install -e ".[docs-testing]"`
3. **Playwright issues**: Run `playwright install` after installing
4. **Network timeouts**: Some external link tests may be flaky

### Debug Mode

```bash
# Verbose output
pytest tests/docs/ -v -s

# Stop on first failure
pytest tests/docs/ -x

# Show local variables on failure
pytest tests/docs/ -l

# Debug specific test
pytest tests/docs/test_link_validation.py::test_internal_links_validation -v -s
```

### Performance Optimization

```bash
# Parallel test execution
pytest tests/docs/ -n auto

# Skip slow tests during development
pytest tests/docs/ -m "not slow"

# Run specific test categories
pytest tests/docs/test_content_validation.py -k "not accessibility"
```

## Best Practices

### Writing Tests

1. **Use descriptive test names** that explain what is being tested
2. **Follow the AAA pattern**: Arrange, Act, Assert
3. **Use appropriate fixtures** for setup and teardown
4. **Add proper error messages** for failed assertions
5. **Mark tests appropriately** with pytest markers

### QA Processes

1. **Run quick tests** during development
2. **Run comprehensive tests** before commits
3. **Check external links** regularly
4. **Review test reports** for insights
5. **Update tests** when documentation changes

### CI Integration

1. **Use appropriate triggers** for different test levels
2. **Cache dependencies** for faster builds
3. **Upload artifacts** for debugging
4. **Create informative PR comments**
5. **Set appropriate timeouts**

## Contributing

When contributing to the testing framework:

1. **Follow existing patterns** and conventions
2. **Add tests for new functionality**
3. **Update documentation** as needed
4. **Test changes** locally before submitting
5. **Ensure CI passes** on all platforms

## Support

For issues or questions about the testing framework:

1. Check the **troubleshooting section** above
2. Review **existing test implementations** for patterns
3. Check **CI workflow logs** for specific failures
4. Open an issue with **detailed reproduction steps**
