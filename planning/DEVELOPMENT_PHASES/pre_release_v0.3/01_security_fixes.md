# Security Fixes - Priority 1 (BLOCKING)

## Overview
Address all security vulnerabilities identified in technical review. These are deployment-blocking issues that create attack vectors for malicious actors.

## Critical Security Issues

### CVE-LEVEL ISSUE #1: Environment Variable Injection Attack
**Severity**: CRITICAL
**Location**: `src/autodocs_mcp/config.py:49`
**Risk**: PyPI URL redirection to malicious servers

#### Task 1.1: Implement PyPI URL Validation
**Assignee**: Senior Backend Developer
**Estimated Time**: 2 hours

**Requirements**:
```python
def validate_pypi_url(url: str) -> str:
    """Validate PyPI URL against allowlist of trusted domains."""
    from urllib.parse import urlparse

    TRUSTED_PYPI_DOMAINS = {
        "pypi.org",
        "test.pypi.org",
        "pypi.python.org"  # Legacy support
    }

    try:
        parsed = urlparse(url)
        if not parsed.scheme or parsed.scheme not in ("http", "https"):
            raise ValueError(f"Invalid URL scheme: {parsed.scheme}")

        if parsed.netloc not in TRUSTED_PYPI_DOMAINS:
            raise ValueError(f"Untrusted PyPI domain: {parsed.netloc}")

        # Ensure HTTPS for production
        if parsed.scheme == "http" and parsed.netloc != "localhost":
            raise ValueError("HTTP URLs not allowed in production")

        return url
    except Exception as e:
        raise ValueError(f"Invalid PyPI URL '{url}': {e}")
```

**Files to Modify**:
- `src/autodocs_mcp/config.py`
- Add `src/autodocs_mcp/security.py` (new file)

**Acceptance Criteria**:
- ✅ URL validation function implemented with comprehensive tests
- ✅ Only trusted PyPI domains allowed
- ✅ HTTPS enforcement for production environments
- ✅ Clear error messages for invalid URLs
- ✅ Backward compatibility maintained for valid URLs

**Testing Requirements**:
- Unit tests for all validation scenarios
- Integration tests with various URL formats
- Security tests with malicious URL attempts

---

### CVE-LEVEL ISSUE #2: Path Traversal Vulnerability
**Severity**: HIGH
**Location**: `src/autodocs_mcp/core/cache_manager.py:59`
**Risk**: File system access outside cache directory

#### Task 1.2: Implement Cache Key Sanitization
**Assignee**: Senior Backend Developer
**Estimated Time**: 3 hours

**Requirements**:
```python
def sanitize_cache_key(cache_key: str) -> str:
    """Sanitize cache key to prevent path traversal attacks."""
    import re
    from pathlib import Path

    # Remove dangerous characters and path components
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', cache_key)
    sanitized = re.sub(r'\.\.+', '.', sanitized)  # Collapse multiple dots
    sanitized = sanitized.strip('. ')  # Remove leading/trailing dots and spaces

    # Ensure reasonable length
    if len(sanitized) > 200:
        sanitized = sanitized[:200]

    # Validate final result
    if not sanitized or sanitized in {'', '.', '..', 'CON', 'PRN', 'AUX', 'NUL'}:
        raise ValueError(f"Invalid cache key after sanitization: {cache_key}")

    return sanitized
```

**Files to Modify**:
- `src/autodocs_mcp/core/cache_manager.py`
- `src/autodocs_mcp/security.py` (add sanitization functions)

**Acceptance Criteria**:
- ✅ All cache key inputs sanitized before file operations
- ✅ Path traversal attempts blocked (../, ..\, etc.)
- ✅ Special characters and reserved names handled
- ✅ Cache functionality preserved for legitimate keys
- ✅ Clear error handling for invalid keys

**Testing Requirements**:
- Security tests with path traversal payloads
- Unit tests for edge cases and malicious inputs
- Integration tests ensuring cache still functions

---

### MEDIUM PRIORITY: Input Validation Framework
**Severity**: MEDIUM
**Location**: Multiple files accepting user input

#### Task 1.3: Implement Comprehensive Input Validation
**Assignee**: Senior Backend Developer
**Estimated Time**: 3 hours

**Requirements**:
```python
class InputValidator:
    """Centralized input validation for all user inputs."""

    @staticmethod
    def validate_package_name(name: str) -> str:
        """Validate PyPI package name format."""
        import re

        if not isinstance(name, str) or not name:
            raise ValueError("Package name must be a non-empty string")

        # PyPI naming rules
        if not re.match(r'^[A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9])?$', name):
            raise ValueError(f"Invalid package name format: {name}")

        if len(name) > 214:  # PyPI limit
            raise ValueError(f"Package name too long: {len(name)} > 214 characters")

        return name.lower()  # Normalize case

    @staticmethod
    def validate_version_constraint(constraint: str) -> str:
        """Validate version constraint syntax."""
        from packaging.specifiers import SpecifierSet

        try:
            SpecifierSet(constraint)
            return constraint
        except Exception as e:
            raise ValueError(f"Invalid version constraint '{constraint}': {e}")

    @staticmethod
    def validate_project_path(path: str) -> Path:
        """Validate and resolve project path."""
        from pathlib import Path

        try:
            resolved = Path(path).resolve()
            if not resolved.exists():
                raise ValueError(f"Path does not exist: {path}")
            return resolved
        except Exception as e:
            raise ValueError(f"Invalid project path '{path}': {e}")
```

**Files to Modify**:
- `src/autodocs_mcp/security.py` (add InputValidator class)
- `src/autodocs_mcp/main.py` (add input validation to all MCP tools)
- `src/autodocs_mcp/core/dependency_parser.py` (add validation)

**Acceptance Criteria**:
- ✅ All MCP tool inputs validated before processing
- ✅ Package names conform to PyPI standards
- ✅ Version constraints validated against packaging library
- ✅ File paths validated and resolved securely
- ✅ Clear error messages for validation failures

## Security Testing Requirements

### Penetration Testing Checklist
- [ ] Path traversal attack attempts
- [ ] URL redirection attacks
- [ ] Malicious package name injection
- [ ] Invalid version constraint handling
- [ ] File system boundary testing
- [ ] Environment variable manipulation
- [ ] Input fuzzing for all MCP tools

### Security Code Review
- [ ] All user inputs validated at entry points
- [ ] No direct file system access without sanitization
- [ ] URL construction uses trusted sources only
- [ ] Error messages don't leak sensitive information
- [ ] No SQL injection vectors (though we don't use SQL)

## Completion Criteria

**Security Gate Requirements**:
1. ✅ All CVE-level vulnerabilities resolved
2. ✅ Input validation framework implemented
3. ✅ Security tests passing (>95% coverage)
4. ✅ Penetration testing completed with no findings
5. ✅ Security code review approved by technical lead

**Time Allocation**:
- Implementation: 6 hours
- Testing: 2 hours
- Security review: 1 hour
- **Total: 1 day**
