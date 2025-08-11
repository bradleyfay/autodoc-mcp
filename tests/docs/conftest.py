"""
Pytest configuration and fixtures for documentation testing.

Provides shared fixtures and configuration for all documentation tests.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture(scope="session")
def site_dir(project_root):
    """Get the site directory (built documentation)."""
    site_path = project_root / "site"

    # Check if site exists, if not try to build it
    if not site_path.exists():
        docs_build_result = subprocess.run(
            [sys.executable, "-m", "mkdocs", "build"],
            cwd=project_root,
            capture_output=True,
            text=True,
        )

        if docs_build_result.returncode != 0:
            pytest.skip(
                f"Could not build documentation site. Error: {docs_build_result.stderr}"
            )

    return site_path


@pytest.fixture(scope="session")
def docs_dir(project_root):
    """Get the docs source directory."""
    return project_root / "docs"


@pytest.fixture(scope="session")
def mkdocs_config(project_root):
    """Get the MkDocs configuration file."""
    return project_root / "mkdocs.yml"


@pytest.fixture
def temp_site_dir():
    """Create a temporary site directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        yield temp_path


@pytest.fixture
def sample_html_page():
    """Create a sample HTML page for testing."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Sample page for testing">
        <title>Sample Page</title>
        <link rel="stylesheet" href="assets/stylesheets/main.css">
    </head>
    <body>
        <nav>
            <a href="/">Home</a>
            <a href="/about/">About</a>
            <a href="/contact/">Contact</a>
        </nav>

        <main>
            <h1>Sample Page</h1>
            <p>This is a sample page for testing purposes.</p>

            <h2>Code Example</h2>
            <pre><code class="language-python">
def hello_world():
    print("Hello, world!")
    return "Hello, world!"
            </code></pre>

            <h3>External Link</h3>
            <p>Visit <a href="https://github.com/bradleyfay/autodoc-mcp">our GitHub</a>.</p>

            <h3>Internal Link</h3>
            <p>Go to <a href="/docs/getting-started/">Getting Started</a>.</p>

            <img src="assets/images/logo.png" alt="AutoDocs Logo">
        </main>

        <footer>
            <p>© 2025 AutoDocs</p>
        </footer>

        <script src="assets/javascripts/bundle.js"></script>
    </body>
    </html>
    """
    return html_content


@pytest.fixture
def sample_markdown_content():
    """Sample markdown content for testing."""
    return """
# Sample Documentation

This is a sample documentation page for testing.

## Features

- Link validation
- Content validation
- Cross-platform testing

## Code Example

```python
import pytest

def test_example():
    assert True
```

## External Links

- [Python](https://python.org)
- [PyPI](https://pypi.org)

## Internal Links

- [Installation](installation.md)
- [Configuration](configuration.md)
"""


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch, project_root):
    """Set up test environment variables."""
    # Ensure we're testing in the right directory
    monkeypatch.chdir(project_root)

    # Set environment variables for consistent testing
    monkeypatch.setenv("PYTHONPATH", str(project_root / "src"))

    # Disable interactive prompts during testing
    monkeypatch.setenv("CI", "true")


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "external: marks tests that require external network access"
    )
    config.addinivalue_line(
        "markers", "browser: marks tests that require browser automation"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Mark external link tests
        if "external" in item.name:
            item.add_marker(pytest.mark.external)

        # Mark browser tests
        if "cross_platform" in str(item.fspath) or "browser" in item.name:
            item.add_marker(pytest.mark.browser)

        # Mark slow tests
        if any(
            slow_keyword in item.name
            for slow_keyword in ["comprehensive", "cross_platform", "external"]
        ):
            item.add_marker(pytest.mark.slow)


@pytest.fixture
def mock_http_server():
    """Mock HTTP server for testing external links."""
    try:
        import importlib.util
        from unittest.mock import Mock

        if importlib.util.find_spec("httpx") is None:
            pytest.skip("httpx not available for HTTP mocking")

        # Create a mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.is_success = True
        mock_response.headers = {"content-type": "text/html"}

        return mock_response
    except ImportError:
        pytest.skip("httpx not available for HTTP mocking")


# Skip certain tests if optional dependencies are not available
def pytest_runtest_setup(item):
    """Skip tests based on available dependencies."""
    import importlib.util

    # Skip Playwright tests if not installed
    if (
        "cross_platform" in str(item.fspath)
        and importlib.util.find_spec("playwright") is None
    ):
        pytest.skip("Playwright not installed")

    # Skip BeautifulSoup tests if not available
    if (
        any(marker in item.name for marker in ["content_validation", "link_validation"])
        and importlib.util.find_spec("bs4") is None
    ):
        pytest.skip("BeautifulSoup4 not installed")
