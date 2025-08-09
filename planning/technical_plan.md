# AutoDocs MCP Server - Technical Implementation Plan

## 1. Project Setup & Infrastructure

### 1.1 Development Environment Setup

#### Package Management with Hatch & UV
```bash
# Initialize project with hatch
hatch new --init autodocs-mcp

# Install uv for fast dependency resolution
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Project Structure
```
autodocs-mcp/
├── pyproject.toml              # Hatch configuration with FastMCP dependencies
├── src/
│   └── autodocs_mcp/
│       ├── __init__.py
│       ├── main.py             # FastMCP server entry point
│       ├── config.py           # Configuration management
│       ├── exceptions.py       # Custom exception hierarchy
│       └── core/
│           ├── __init__.py
│           ├── dependency_parser.py
│           ├── doc_fetcher.py
│           ├── cache_manager.py
│           ├── version_resolver.py  # Version-based caching logic
│           ├── dependency_resolver.py  # Context dependency resolution
│           └── models.py       # Data models and schemas
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   ├── unit/
│   ├── integration/
│   └── fixtures/              # Test data files
├── scripts/
│   └── dev.py                 # Development utilities
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI/CD
└── docs/
    └── README.md              # Setup and usage instructions
```

#### pyproject.toml Configuration
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "autodocs-mcp"
version = "0.1.0"
description = "MCP server for automatic Python package documentation context"
authors = [{name = "AutoDocs Team"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastmcp>=2.0.0",
    "httpx>=0.25.0",
    "tomlkit>=0.12.0",
    "pydantic>=2.0.0",
    "structlog>=23.2.0",
    "packaging>=23.0",  # For version constraint parsing
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-mock>=3.11.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.6.0",
    "pre-commit>=3.5.0",
]

[project.scripts]
autodocs-mcp = "autodocs_mcp.main:main"

[tool.hatch.envs.default]
dependencies = [
    "pytest",
    "pytest-asyncio",
    "pytest-mock",
    "pytest-cov",
]

[tool.hatch.envs.default.scripts]
test = "pytest {args:tests}"
test-cov = "pytest --cov=src/autodocs_mcp {args:tests}"
lint = "ruff check {args:src tests}"
format = "ruff format {args:src tests}"
typecheck = "mypy {args:src}"

[tool.ruff]
target-version = "py311"
line-length = 88
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM", "TCH"]
ignore = ["E501", "N805"]

[tool.ruff.per-file-ignores]
"tests/*" = ["S101"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --strict-markers"
testpaths = ["tests"]
asyncio_mode = "auto"
```

### 1.2 CI/CD Pipeline Setup

#### GitHub Actions Workflow
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4
    - name: Install uv
      uses: astral-sh/setup-uv@v2
    - name: Set up Python ${{ matrix.python-version }}
      run: uv python install ${{ matrix.python-version }}
    - name: Install dependencies
      run: uv sync --all-extras
    - name: Lint with ruff
      run: uv run ruff check
    - name: Check formatting
      run: uv run ruff format --check
    - name: Type check with mypy
      run: uv run mypy src
    - name: Test with pytest
      run: uv run pytest --cov=src --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  integration-test:
    runs-on: ubuntu-latest
    needs: test
    steps:
    - uses: actions/checkout@v4
    - name: Install uv
      uses: astral-sh/setup-uv@v2
    - name: Set up Python 3.11
      run: uv python install 3.11
    - name: Install dependencies
      run: uv sync
    - name: Run integration tests
      run: uv run pytest tests/integration/ -v
```

## 2. Implementation Phases (Updated with Refined Strategies)

### Phase 1: Core Infrastructure & Version-Based Caching (Week 1)

#### 1.1 Project Setup and Configuration
- [ ] Initialize hatch project structure
- [ ] Configure pyproject.toml with all dependencies
- [ ] Setup ruff for linting and formatting
- [ ] Configure mypy for type checking
- [ ] Create basic package structure

#### 1.2 Data Models and Configuration
```python
# src/autodocs_mcp/models.py
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from pathlib import Path

class DependencySpec(BaseModel):
    """Represents a single dependency specification"""
    model_config = ConfigDict(frozen=True)

    name: str = Field(..., min_length=1)
    version_constraint: Optional[str] = None
    extras: List[str] = Field(default_factory=list)
    source: str = Field(default="project")  # project, dev, build

class PackageInfo(BaseModel):
    """PyPI package information"""
    model_config = ConfigDict(frozen=True)

    name: str
    version: str
    summary: Optional[str] = None
    description: Optional[str] = None
    home_page: Optional[str] = None
    project_urls: Dict[str, str] = Field(default_factory=dict)
    author: Optional[str] = None
    license: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    classifiers: List[str] = Field(default_factory=list)

class DocumentationContext(BaseModel):
    """Complete documentation context for AI consumption"""

    # Primary package (the one explicitly requested)
    primary_package: 'PackageDocumentation'

    # Direct dependencies (runtime dependencies)
    runtime_dependencies: List['PackageDocumentation'] = Field(default_factory=list)

    # Development dependencies (if relevant to query)
    dev_dependencies: List['PackageDocumentation'] = Field(default_factory=list)

    # Context metadata
    context_scope: str  # "primary_only", "with_runtime", "with_dev"
    total_packages: int
    truncated_packages: List[str] = Field(default_factory=list)  # Packages skipped due to limits

    @property
    def token_estimate(self) -> int:
        """Rough token count estimate for context window management"""
        return sum(doc.token_estimate for doc in self.all_packages)

    @property
    def all_packages(self) -> List['PackageDocumentation']:
        return [self.primary_package] + self.runtime_dependencies + self.dev_dependencies

class PackageDocumentation(BaseModel):
    """Documentation for a single package"""
    name: str
    version: str
    relationship: str  # "primary", "runtime_dependency", "dev_dependency"

    # Core documentation sections
    summary: Optional[str] = None
    key_features: List[str] = Field(default_factory=list)
    main_classes: List[str] = Field(default_factory=list)
    main_functions: List[str] = Field(default_factory=list)
    usage_examples: Optional[str] = None

    # Relationship context
    why_included: str  # "Requested package", "Required by fastapi", etc.
    dependency_level: int  # 0=primary, 1=direct dep, 2=transitive, etc.

    @property
    def token_estimate(self) -> int:
        """Rough token count for this documentation"""
        content = f"{self.summary} {self.usage_examples}"
        return int(len(content.split()) * 1.3)  # Rough tokens per word

class CacheEntry(BaseModel):
    """Version-based cache entry (no time expiration)"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: PackageInfo
    timestamp: datetime  # For metadata only, not expiration
    version: str  # Exact version for cache key

    # No is_expired property - version-based invalidation only

class ScanResult(BaseModel):
    """Enhanced result model supporting graceful degradation"""
    project_path: Path
    dependencies: List[DependencySpec]
    project_name: Optional[str] = None
    scan_timestamp: datetime

    # Graceful degradation fields
    successful_deps: int = 0
    failed_deps: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    partial_success: bool = False
```

#### 1.3 Configuration Management
```python
# src/autodocs_mcp/config.py
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from functools import lru_cache

class AutoDocsConfig(BaseModel):
    """Application configuration (updated for version-based caching)"""
    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".autodocs" / "cache")
    max_concurrent: int = Field(default=10)
    request_timeout: int = Field(default=30)
    log_level: str = Field(default="INFO")
    pypi_base_url: str = Field(default="https://pypi.org/pypi")

    # Version-based caching settings
    max_cached_versions_per_package: int = Field(default=3)
    cache_cleanup_days: int = Field(default=90)  # Remove unused packages after 90 days

    # Context settings
    max_dependency_context: int = Field(default=8)
    max_context_tokens: int = Field(default=30000)

    @classmethod
    def from_env(cls) -> 'AutoDocsConfig':
        """Load configuration from environment variables"""
        return cls(
            cache_dir=Path(os.getenv("AUTODOCS_CACHE_DIR", str(cls.model_fields['cache_dir'].default()))),
            max_concurrent=int(os.getenv("AUTODOCS_MAX_CONCURRENT", str(cls.model_fields['max_concurrent'].default))),
            request_timeout=int(os.getenv("AUTODOCS_REQUEST_TIMEOUT", str(cls.model_fields['request_timeout'].default))),
            log_level=os.getenv("AUTODOCS_LOG_LEVEL", cls.model_fields['log_level'].default),
            pypi_base_url=os.getenv("AUTODOCS_PYPI_URL", cls.model_fields['pypi_base_url'].default),
            max_cached_versions_per_package=int(os.getenv("AUTODOCS_MAX_VERSIONS", str(cls.model_fields['max_cached_versions_per_package'].default))),
            cache_cleanup_days=int(os.getenv("AUTODOCS_CLEANUP_DAYS", str(cls.model_fields['cache_cleanup_days'].default))),
            max_dependency_context=int(os.getenv("AUTODOCS_MAX_DEPS", str(cls.model_fields['max_dependency_context'].default))),
            max_context_tokens=int(os.getenv("AUTODOCS_MAX_TOKENS", str(cls.model_fields['max_context_tokens'].default))),
        )

    def model_post_init(self, __context: Any) -> None:
        """Ensure cache directory exists"""
        self.cache_dir.mkdir(parents=True, exist_ok=True)

@lru_cache()
def get_config() -> AutoDocsConfig:
    """Get cached configuration instance"""
    return AutoDocsConfig.from_env()
```

### Phase 2: Core Services with Graceful Degradation (Week 2)

#### 2.1 Dependency Parser Implementation
```python
# src/autodocs_mcp/core/dependency_parser.py
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional
import tomlkit
from tomlkit.exceptions import TOMLKitError

from ..models import DependencySpec, ScanResult
from ..exceptions import ProjectParsingError

class DependencyParserInterface(ABC):
    """Interface for dependency parsing"""

    @abstractmethod
    async def parse_project(self, project_path: Path) -> ScanResult:
        """Parse project dependencies from configuration files"""

    @abstractmethod
    def validate_file(self, file_path: Path) -> bool:
        """Validate project configuration file"""

class PyProjectParser(DependencyParserInterface):
    """Parser for pyproject.toml files"""

    VERSION_PATTERN = re.compile(r'^([><=!~^]+)?([\d\w.-]+)$')

    async def parse_project(self, project_path: Path) -> ScanResult:
        """Parse pyproject.toml with graceful degradation"""
        pyproject_path = project_path / "pyproject.toml"

        if not pyproject_path.exists():
            raise ProjectParsingError(
                f"pyproject.toml not found in {project_path}",
                file_path=pyproject_path
            )

        dependencies = []
        failed_deps = []
        warnings = []
        errors = []

        try:
            content = pyproject_path.read_text(encoding='utf-8')
            parsed = tomlkit.parse(content)
        except TOMLKitError as e:
            raise ProjectParsingError(
                f"Invalid TOML syntax: {e}",
                file_path=pyproject_path
            ) from e

        # Parse main dependencies with error handling
        project_section = parsed.get('project', {})
        project_name = project_section.get('name')

        if 'dependencies' in project_section:
            deps, failed = self._parse_dependency_list_safe(
                project_section['dependencies'], 'project'
            )
            dependencies.extend(deps)
            failed_deps.extend(failed)

        # Parse optional dependencies with error handling
        optional_deps = project_section.get('optional-dependencies', {})
        for group_name, dep_list in optional_deps.items():
            deps, failed = self._parse_dependency_list_safe(
                dep_list, f'optional-{group_name}'
            )
            dependencies.extend(deps)
            failed_deps.extend(failed)

        # Generate warnings for failed deps
        if failed_deps:
            warnings.extend([
                f"Skipped malformed dependency: {f['dependency_string']}"
                for f in failed_deps
            ])

        return ScanResult(
            project_path=project_path,
            dependencies=dependencies,
            project_name=project_name,
            successful_deps=len(dependencies),
            failed_deps=failed_deps,
            warnings=warnings,
            errors=errors,
            partial_success=len(failed_deps) > 0 or len(warnings) > 0,
            scan_timestamp=datetime.now()
        )

    def validate_file(self, file_path: Path) -> bool:
        """Validate pyproject.toml structure"""
        try:
            content = file_path.read_text(encoding='utf-8')
            parsed = tomlkit.parse(content)
            return 'project' in parsed
        except (OSError, TOMLKitError):
            return False

    def _parse_dependency_list_safe(self, deps: List[str], source: str) -> Tuple[List[DependencySpec], List[Dict[str, Any]]]:
        """Parse dependency list with error collection"""
        parsed_deps = []
        failed_deps = []

        for dep_str in deps:
            try:
                spec = self._parse_dependency_string(dep_str, source)
                parsed_deps.append(spec)
            except ValueError as e:
                failed_deps.append({
                    "dependency_string": dep_str,
                    "error": str(e),
                    "source": source
                })
                continue  # Keep processing other deps

        return parsed_deps, failed_deps

    def _parse_dependency_string(self, dep_str: str, source: str) -> DependencySpec:
        """Parse a single dependency string like 'requests>=2.0.0[security]'"""
        # Handle extras
        extras = []
        if '[' in dep_str and ']' in dep_str:
            name_part, extra_part = dep_str.split('[', 1)
            extra_part = extra_part.rstrip(']')
            extras = [e.strip() for e in extra_part.split(',')]
            dep_str = name_part

        # Handle version constraints
        version_constraint = None
        if any(op in dep_str for op in ['>=', '<=', '==', '!=', '~=', '>', '<']):
            for i, char in enumerate(dep_str):
                if char in '>=<!~':
                    name = dep_str[:i].strip()
                    version_constraint = dep_str[i:].strip()
                    break
        else:
            name = dep_str.strip()

        return DependencySpec(
            name=name,
            version_constraint=version_constraint,
            extras=extras,
            source=source
        )
```

#### 2.2 Documentation Fetcher Implementation
```python
# src/autodocs_mcp/core/doc_fetcher.py
import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import httpx
from structlog import get_logger

from ..models import PackageInfo
from ..config import get_config
from ..exceptions import NetworkError, PackageNotFoundError

logger = get_logger(__name__)

class DocumentationFetcherInterface(ABC):
    """Interface for documentation fetching"""

    @abstractmethod
    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        """Fetch package information from external source"""

    @abstractmethod
    def format_documentation(self, package_info: PackageInfo, query: Optional[str] = None) -> str:
        """Format package info for AI consumption"""

class PyPIDocumentationFetcher(DocumentationFetcherInterface):
    """Fetches documentation from PyPI JSON API"""

    def __init__(self, semaphore: Optional[asyncio.Semaphore] = None):
        self.config = get_config()
        self.semaphore = semaphore or asyncio.Semaphore(self.config.max_concurrent)
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.config.request_timeout),
            follow_redirects=True
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        """Fetch package information from PyPI JSON API"""
        async with self.semaphore:
            url = f"{self.config.pypi_base_url}/{package_name}/json"

            logger.info("Fetching package info", package=package_name, url=url)

            try:
                response = await self._client.get(url)
                response.raise_for_status()
                data = response.json()

                return self._parse_pypi_response(data)

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise PackageNotFoundError(f"Package '{package_name}' not found on PyPI")
                raise NetworkError(f"PyPI API error: {e.response.status_code}")

            except httpx.RequestError as e:
                raise NetworkError(f"Network error fetching {package_name}: {e}")

    def format_documentation(self, package_info: PackageInfo, query: Optional[str] = None) -> str:
        """Format package info for AI consumption with optional query filtering"""
        sections = []

        # Basic info
        sections.append(f"# {package_info.name} v{package_info.version}")

        if package_info.summary:
            sections.append(f"**Summary**: {package_info.summary}")

        if package_info.author:
            sections.append(f"**Author**: {package_info.author}")

        # Description (truncated if too long)
        if package_info.description:
            desc = package_info.description
            if len(desc) > 2000:  # Truncate very long descriptions
                desc = desc[:2000] + "..."
            sections.append(f"## Description\n{desc}")

        # Project URLs
        if package_info.project_urls:
            sections.append("## Links")
            for label, url in package_info.project_urls.items():
                sections.append(f"- **{label}**: {url}")

        if package_info.home_page:
            sections.append(f"- **Homepage**: {package_info.home_page}")

        # Keywords and classifiers (if relevant to query)
        if package_info.keywords and (not query or any(kw in query.lower() for kw in package_info.keywords)):
            sections.append(f"**Keywords**: {', '.join(package_info.keywords)}")

        formatted = "\n\n".join(sections)

        # Apply query filtering if provided
        if query:
            formatted = self._apply_query_filter(formatted, query)

        return formatted

    def _parse_pypi_response(self, data: Dict[str, Any]) -> PackageInfo:
        """Parse PyPI JSON response into PackageInfo model"""
        info = data.get('info', {})

        return PackageInfo(
            name=info.get('name', ''),
            version=info.get('version', ''),
            summary=info.get('summary'),
            description=info.get('description'),
            home_page=info.get('home_page'),
            project_urls=info.get('project_urls', {}),
            author=info.get('author'),
            license=info.get('license'),
            keywords=info.get('keywords', '').split() if info.get('keywords') else [],
            classifiers=info.get('classifiers', [])
        )

    def _apply_query_filter(self, content: str, query: str) -> str:
        """Apply simple query-based filtering to content"""
        query_terms = query.lower().split()

        # Split content into sections and score by relevance
        sections = content.split('\n\n')
        relevant_sections = []

        for section in sections:
            section_lower = section.lower()
            score = sum(1 for term in query_terms if term in section_lower)

            if score > 0:
                relevant_sections.append((score, section))

        # Sort by relevance and return top sections
        relevant_sections.sort(key=lambda x: x[0], reverse=True)

        return '\n\n'.join([section for _, section in relevant_sections[:5]])
```

#### 2.3 Version Resolution and Dependency Context Components
```python
# src/autodocs_mcp/core/version_resolver.py
import httpx
from typing import Optional
from packaging import version
from packaging.specifiers import SpecifierSet
from structlog import get_logger

from ..config import get_config
from ..exceptions import NetworkError, PackageNotFoundError

logger = get_logger(__name__)

class VersionResolver:
    """Resolve version constraints to specific versions"""

    @staticmethod
    async def resolve_version(package_name: str, constraint: Optional[str] = None) -> str:
        """
        Resolve version constraint to specific version

        Args:
            package_name: Package to resolve
            constraint: Version constraint like ">=2.0.0" or None for latest

        Returns:
            Specific version string like "2.28.2"
        """
        config = get_config()

        async with httpx.AsyncClient(timeout=httpx.Timeout(config.request_timeout)) as client:
            try:
                response = await client.get(f"{config.pypi_base_url}/{package_name}/json")
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise PackageNotFoundError(f"Package '{package_name}' not found on PyPI")
                raise NetworkError(f"PyPI API error: {e.response.status_code}")
            except httpx.RequestError as e:
                raise NetworkError(f"Network error resolving {package_name}: {e}")

        latest_version = data["info"]["version"]

        if constraint is None:
            return latest_version

        # Parse and validate constraint
        try:
            specifier = SpecifierSet(constraint)
            if latest_version in specifier:
                return latest_version
            else:
                # For MVP, raise error if latest doesn't match
                # Future: implement full version resolution from all releases
                raise ValueError(f"Latest version {latest_version} doesn't satisfy constraint {constraint}")
        except Exception as e:
            logger.warning("Version constraint parsing failed",
                          package=package_name, constraint=constraint, error=str(e))
            return latest_version  # Fallback to latest

    @staticmethod
    def generate_cache_key(package_name: str, version: str) -> str:
        """Generate cache key for specific version"""
        return f"{package_name}-{version}"


# src/autodocs_mcp/core/dependency_resolver.py
from typing import List, Dict, Any, Tuple
from structlog import get_logger

from ..models import DependencySpec
from .version_resolver import VersionResolver
from .cache_manager import FileCacheManager

logger = get_logger(__name__)

# Pre-defined package categories for relevance scoring
CORE_FRAMEWORKS = {
    "pydantic", "fastapi", "django", "flask", "requests", "httpx",
    "sqlalchemy", "pandas", "numpy", "click", "typer"
}

COMMON_UTILITIES = {
    "rich", "typer", "click", "jinja2", "pyyaml", "python-dotenv",
    "structlog", "loguru", "pytest", "black", "ruff"
}

LOW_PRIORITY_DEPS = {
    "setuptools", "wheel", "pip", "build", "hatchling", "setuptools-scm",
    "tomli", "typing-extensions", "importlib-metadata"
}

WELL_DOCUMENTED = {
    "requests", "pydantic", "fastapi", "click", "typer", "rich",
    "pandas", "numpy", "sqlalchemy", "jinja2", "pytest"
}

class DependencyResolver:
    """Resolve package dependencies with intelligent context scoping"""

    def __init__(self, cache_manager: FileCacheManager):
        self.cache_manager = cache_manager

    async def resolve_context_dependencies(
        self,
        package_name: str,
        version: str,
        max_dependencies: int = 8,
        max_tokens: int = 30000
    ) -> List[str]:
        """
        Resolve which dependencies to include in context

        Args:
            package_name: Primary package
            version: Specific version
            max_dependencies: Maximum number of deps to include
            max_tokens: Token budget for dependency context

        Returns:
            List of dependency package names to fetch
        """
        try:
            # Get dependency metadata from PyPI (simplified for MVP)
            deps_metadata = await self._get_dependency_metadata(package_name, version)

            # Score dependencies by relevance
            scored_deps = []
            for dep_name in deps_metadata.get('requires_dist', []):
                # Parse dependency name (ignore version constraints for scoring)
                dep_name_clean = dep_name.split()[0] if dep_name else ""
                if dep_name_clean:
                    score = self._calculate_dependency_relevance(dep_name_clean, package_name)
                    scored_deps.append((score, dep_name_clean))

            # Sort by relevance and apply limits
            scored_deps.sort(reverse=True, key=lambda x: x[0])  # Highest score first

            selected_deps = []
            for score, dep_name in scored_deps:
                if len(selected_deps) >= max_dependencies:
                    break
                if score > 0:  # Only include positively scored deps
                    selected_deps.append(dep_name)

            logger.info("Resolved context dependencies",
                       package=package_name,
                       selected_count=len(selected_deps),
                       total_available=len(scored_deps))

            return selected_deps

        except Exception as e:
            logger.warning("Dependency context resolution failed",
                          package=package_name, error=str(e))
            return []  # Return empty list on failure

    def _calculate_dependency_relevance(self, dep_name: str, primary_package: str) -> float:
        """Score dependency relevance for context inclusion"""
        score = 0.0

        # Core framework dependencies get high priority
        if dep_name in CORE_FRAMEWORKS:
            score += 10.0

        # Common utility libraries
        if dep_name in COMMON_UTILITIES:
            score += 5.0

        # Package-specific boost for known important relationships
        package_boosts = {
            "fastapi": {"pydantic": 8.0, "starlette": 8.0, "uvicorn": 6.0},
            "django": {"django-rest-framework": 7.0, "psycopg2": 6.0},
            "flask": {"jinja2": 7.0, "werkzeug": 7.0},
            "requests": {"urllib3": 8.0, "certifi": 6.0}
        }

        if primary_package in package_boosts:
            score += package_boosts[primary_package].get(dep_name, 0.0)

        # Penalty for very low-level or build dependencies
        if dep_name in LOW_PRIORITY_DEPS:
            score -= 5.0

        # Boost for packages with good documentation
        if dep_name in WELL_DOCUMENTED:
            score += 2.0

        return max(0.0, score)  # Don't go negative

    async def _get_dependency_metadata(self, package_name: str, version: str) -> Dict[str, Any]:
        """Get dependency metadata from PyPI (simplified version)"""
        # For MVP: return basic metadata structure
        # Future: implement full dependency tree resolution
        return {
            "requires_dist": []  # Would be populated from PyPI API
        }
```

### Phase 3: Enhanced MCP Integration with Context (Week 3)

#### 3.1 Enhanced FastMCP Server with Context Support
```python
# src/autodocs_mcp/main.py
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
import structlog
from fastmcp import FastMCP

from .config import get_config
from .core.dependency_parser import PyProjectParser
from .core.doc_fetcher import PyPIDocumentationFetcher
from .core.cache_manager import FileCacheManager
from .exceptions import AutoDocsError

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),
    wrapper_class=structlog.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# Initialize FastMCP server
mcp = FastMCP("AutoDocs MCP Server 🚀")

# Global services (initialized in main)
parser: PyProjectParser = None
cache_manager: FileCacheManager = None
version_resolver: VersionResolver = None
dependency_resolver: DependencyResolver = None

@mcp.tool
async def scan_dependencies(project_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Scan project dependencies from pyproject.toml

    Args:
        project_path: Path to project directory (defaults to current directory)

    Returns:
        JSON with dependency specifications and project metadata
    """
    try:
        path = Path(project_path) if project_path else Path.cwd()
        logger.info("Scanning dependencies", project_path=str(path))

        result = await parser.parse_project(path)

        return {
            "success": True,
            "partial_success": result.partial_success,
            "project_path": str(result.project_path),
            "project_name": result.project_name,
            "dependencies": [
                {
                    "name": dep.name,
                    "version_constraint": dep.version_constraint,
                    "extras": dep.extras,
                    "source": dep.source
                }
                for dep in result.dependencies
            ],
            "scan_timestamp": result.scan_timestamp.isoformat(),
            "successful_deps": result.successful_deps,
            "total_dependencies": len(result.dependencies),
            "failed_deps": result.failed_deps,
            "warnings": result.warnings,
            "errors": result.errors
        }

    except AutoDocsError as e:
        logger.error("Dependency scanning failed", error=str(e))
        return {
            "success": False,
            "error": {
                "type": type(e).__name__,
                "message": str(e)
            }
        }

@mcp.tool
async def get_package_docs_with_context(
    package_name: str,
    version_constraint: Optional[str] = None,
    include_dependencies: bool = True,
    query: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve comprehensive documentation context including dependencies

    Args:
        package_name: Name of the package to fetch documentation for
        version_constraint: Version constraint from dependency scanning
        include_dependencies: Whether to include dependency context
        query: Optional query to filter documentation sections

    Returns:
        Rich documentation context with primary package and dependencies
    """
    try:
        logger.info("Fetching package docs with context",
                   package=package_name,
                   constraint=version_constraint,
                   include_deps=include_dependencies,
                   query=query)

        # Step 1: Resolve to specific version
        resolved_version = await version_resolver.resolve_version(package_name, version_constraint)

        # Step 2: Check version-specific cache
        cache_key = version_resolver.generate_cache_key(package_name, resolved_version)
        cached_entry = await cache_manager.get(cache_key)

        if cached_entry:
            logger.info("Version-specific cache hit",
                       package=package_name,
                       version=resolved_version)
            primary_info = cached_entry.data
            from_cache = True
        else:
            logger.info("Fetching fresh package info",
                       package=package_name,
                       version=resolved_version)

            async with PyPIDocumentationFetcher() as fetcher:
                primary_info = await fetcher.fetch_package_info(package_name)
                await cache_manager.set(cache_key, primary_info)
            from_cache = False

        # Step 3: Build documentation context
        context = {
            "primary_package": {
                "name": primary_info.name,
                "version": primary_info.version,
                "resolved_version": resolved_version,
                "version_constraint": version_constraint,
                "relationship": "primary",
                "summary": primary_info.summary,
                "documentation": await _format_primary_documentation(primary_info, query)
            },
            "dependencies": [],
            "context_scope": "primary_only",
            "total_packages": 1,
            "from_cache": from_cache
        }

        # Step 4: Add dependency context if requested
        if include_dependencies:
            try:
                dependency_names = await dependency_resolver.resolve_context_dependencies(
                    package_name=primary_info.name,
                    version=primary_info.version,
                    max_dependencies=8
                )

                if dependency_names:
                    dependency_docs = await _fetch_dependency_documentation_batch(
                        dependency_names, primary_info.name
                    )

                    context["dependencies"] = dependency_docs["successful"]
                    context["context_scope"] = f"with_runtime ({len(dependency_docs['successful'])} deps)"
                    context["total_packages"] = 1 + len(dependency_docs["successful"])

                    if dependency_docs["failed"]:
                        context["dependency_errors"] = dependency_docs["failed"]

            except Exception as e:
                logger.warning("Dependency context failed", error=str(e))
                context["context_scope"] = "primary_only (deps_failed)"
                context["dependency_error"] = str(e)

        return {
            "success": True,
            "context": context,
            "performance": {
                "resolved_version": resolved_version,
                "cache_hit": from_cache,
                "dependency_count": len(context.get("dependencies", []))
            }
        }

    except Exception as e:
        logger.error("Documentation fetch failed", package=package_name, error=str(e))
        return {
            "success": False,
            "error": {
                "type": type(e).__name__,
                "message": str(e)
            }
        }

# Maintain backward compatibility with simple tool
@mcp.tool
async def get_package_docs(package_name: str, query: Optional[str] = None) -> Dict[str, Any]:
    """
    Simple package documentation fetch (backward compatibility)

    Args:
        package_name: Name of package
        query: Optional query filter

    Returns:
        Basic package documentation
    """
    result = await get_package_docs_with_context(
        package_name=package_name,
        include_dependencies=False,
        query=query
    )

    if result["success"]:
        primary = result["context"]["primary_package"]
        return {
            "success": True,
            "package_name": primary["name"],
            "version": primary["version"],
            "documentation": primary["documentation"],
            "from_cache": result["performance"]["cache_hit"]
        }
    else:
        return result

# Helper functions for context building
async def _format_primary_documentation(package_info: PackageInfo, query: Optional[str] = None) -> str:
    """Format primary package documentation"""
    async with PyPIDocumentationFetcher() as fetcher:
        return fetcher.format_documentation(package_info, query)

async def _fetch_dependency_documentation_batch(dependency_names: List[str], primary_package: str) -> Dict[str, List]:
    """Fetch documentation for multiple dependencies concurrently"""
    tasks = [
        _fetch_single_dependency_docs(dep_name, primary_package)
        for dep_name in dependency_names
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    successful = []
    failed = []

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            failed.append({
                "package": dependency_names[i],
                "error": str(result)
            })
        else:
            successful.append(result)

    return {"successful": successful, "failed": failed}

async def _fetch_single_dependency_docs(dep_name: str, primary_package: str) -> Dict[str, Any]:
    """Fetch documentation for a single dependency"""
    try:
        resolved_version = await version_resolver.resolve_version(dep_name)
        cache_key = version_resolver.generate_cache_key(dep_name, resolved_version)

        cached_entry = await cache_manager.get(cache_key)
        if cached_entry:
            dep_info = cached_entry.data
        else:
            async with PyPIDocumentationFetcher() as fetcher:
                dep_info = await fetcher.fetch_package_info(dep_name)
                await cache_manager.set(cache_key, dep_info)

        # Format concise documentation for context
        async with PyPIDocumentationFetcher() as fetcher:
            formatted_docs = fetcher.format_documentation(dep_info, truncate=True)

        return {
            "name": dep_info.name,
            "version": dep_info.version,
            "relationship": "runtime_dependency",
            "why_included": f"Required by {primary_package}",
            "summary": dep_info.summary,
            "documentation": formatted_docs[:1000] + "..." if len(formatted_docs) > 1000 else formatted_docs
        }

    except Exception as e:
        raise Exception(f"Failed to fetch docs for {dep_name}: {e}")

@mcp.tool
async def refresh_cache() -> Dict[str, Any]:
    """
    Refresh the local documentation cache

    Returns:
        Statistics about cache refresh operation
    """
    try:
        logger.info("Starting cache refresh")

        stats = await cache_manager.refresh_all()

        logger.info("Cache refresh completed", **stats)

        return {
            "success": True,
            "refreshed_packages": stats["refreshed_count"],
            "failed_packages": stats["failed_count"],
            "total_time_seconds": stats["duration"],
            "errors": stats["errors"]
        }

    except AutoDocsError as e:
        logger.error("Cache refresh failed", error=str(e))
        return {
            "success": False,
            "error": {
                "type": type(e).__name__,
                "message": str(e)
            }
        }

async def initialize_services():
    """Initialize global services with new components"""
    global parser, cache_manager, version_resolver, dependency_resolver

    config = get_config()
    logger.info("Initializing services", config=config.model_dump())

    parser = PyProjectParser()
    cache_manager = FileCacheManager(config.cache_dir)
    version_resolver = VersionResolver()
    dependency_resolver = DependencyResolver(cache_manager)

    await cache_manager.initialize()

def main():
    """Entry point for the MCP server"""
    try:
        # Initialize services
        asyncio.run(initialize_services())

        # Run the server
        mcp.run()

    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error("Server startup failed", error=str(e))
        raise

if __name__ == "__main__":
    main()
```

## 3. Testing Strategy Implementation

### 3.1 Unit Tests Structure
```python
# tests/unit/test_dependency_parser.py
import pytest
from pathlib import Path
from autodocs_mcp.core.dependency_parser import PyProjectParser
from autodocs_mcp.exceptions import ProjectParsingError

class TestPyProjectParser:

    @pytest.fixture
    def parser(self):
        return PyProjectParser()

    @pytest.fixture
    def sample_pyproject(self, tmp_path):
        content = '''
[project]
name = "test-project"
dependencies = [
    "requests>=2.0.0",
    "pydantic[email]>=1.8.0",
    "click"
]

[project.optional-dependencies]
dev = ["pytest>=7.0.0", "ruff"]
'''
        pyproject_path = tmp_path / "pyproject.toml"
        pyproject_path.write_text(content)
        return tmp_path

    async def test_parse_valid_project(self, parser, sample_pyproject):
        result = await parser.parse_project(sample_pyproject)

        assert result.project_name == "test-project"
        assert len(result.dependencies) == 5  # 3 main + 2 dev

        # Check main dependencies
        main_deps = [d for d in result.dependencies if d.source == "project"]
        assert len(main_deps) == 3

        requests_dep = next(d for d in main_deps if d.name == "requests")
        assert requests_dep.version_constraint == ">=2.0.0"

        pydantic_dep = next(d for d in main_deps if d.name == "pydantic")
        assert pydantic_dep.extras == ["email"]

    async def test_parse_missing_file(self, parser, tmp_path):
        with pytest.raises(ProjectParsingError, match="not found"):
            await parser.parse_project(tmp_path)

    async def test_parse_invalid_toml(self, parser, tmp_path):
        invalid_path = tmp_path / "pyproject.toml"
        invalid_path.write_text("invalid toml [content")

        with pytest.raises(ProjectParsingError, match="Invalid TOML"):
            await parser.parse_project(tmp_path)
```

### 3.2 Integration Tests
```python
# tests/integration/test_mcp_tools.py
import pytest
from unittest.mock import AsyncMock, patch
from autodocs_mcp.main import scan_dependencies, get_package_docs

class TestMCPTools:

    @pytest.fixture
    def mock_parser(self):
        with patch('autodocs_mcp.main.parser') as mock:
            yield mock

    @pytest.fixture
    def mock_cache(self):
        with patch('autodocs_mcp.main.cache_manager') as mock:
            yield mock

    async def test_scan_dependencies_success(self, mock_parser, tmp_path):
        # Setup mock response
        mock_result = Mock()
        mock_result.project_name = "test-project"
        mock_result.dependencies = []
        mock_result.scan_timestamp = datetime.now()
        mock_result.errors = []

        mock_parser.parse_project.return_value = mock_result

        # Execute
        result = await scan_dependencies(str(tmp_path))

        # Verify
        assert result["success"] is True
        assert result["project_name"] == "test-project"
        mock_parser.parse_project.assert_called_once()

    async def test_get_package_docs_cache_hit(self, mock_cache):
        # Setup cache hit
        mock_entry = Mock()
        mock_entry.is_expired = False
        mock_entry.data = Mock(name="requests", version="2.28.0")
        mock_cache.get.return_value = mock_entry

        # Execute
        with patch('autodocs_mcp.main.PyPIDocumentationFetcher'):
            result = await get_package_docs("requests")

        # Verify
        assert result["success"] is True
        assert result["cached"] is True
        assert result["package_name"] == "requests"
```

## 4. Deployment and Operations

### 4.1 Development Scripts
```python
# scripts/dev.py
#!/usr/bin/env python3
"""Development utilities for AutoDocs MCP Server"""

import asyncio
import json
from pathlib import Path
import click
from autodocs_mcp.main import scan_dependencies, get_package_docs

@click.group()
def cli():
    """Development tools for AutoDocs MCP"""
    pass

@cli.command()
@click.option('--project-path', type=click.Path(exists=True), default='.')
def test_scan(project_path):
    """Test dependency scanning locally"""
    async def run_test():
        result = await scan_dependencies(project_path)
        click.echo(json.dumps(result, indent=2))

    asyncio.run(run_test())

@cli.command()
@click.argument('package_name')
@click.option('--query', help='Filter query for documentation')
def test_docs(package_name, query):
    """Test documentation fetching locally"""
    async def run_test():
        result = await get_package_docs(package_name, query)
        click.echo(json.dumps(result, indent=2))

    asyncio.run(run_test())

if __name__ == '__main__':
    cli()
```

### 4.2 Performance Benchmarks
```python
# tests/performance/test_benchmarks.py
import pytest
import time
from autodocs_mcp.main import scan_dependencies, get_package_docs

class TestPerformance:

    @pytest.mark.asyncio
    async def test_scan_performance(self, large_project_fixture):
        """Test that scanning completes within performance target"""
        start_time = time.time()

        result = await scan_dependencies(str(large_project_fixture))

        duration = time.time() - start_time
        assert duration < 5.0  # Must complete within 5 seconds
        assert result["success"] is True
        assert result["total_dependencies"] >= 5

    @pytest.mark.asyncio
    async def test_batch_doc_fetching(self):
        """Test concurrent documentation fetching performance"""
        packages = ["requests", "pydantic", "click", "httpx", "structlog"]

        start_time = time.time()

        tasks = [get_package_docs(pkg) for pkg in packages]
        results = await asyncio.gather(*tasks)

        duration = time.time() - start_time
        assert duration < 10.0  # Batch fetch within 10 seconds
        assert all(r["success"] for r in results)
```

## 5. Deployment Checklist

### Pre-Release Validation
- [ ] All unit tests passing
- [ ] Integration tests with real PyPI API
- [ ] Performance benchmarks meet targets
- [ ] Security audit of dependencies
- [ ] Documentation completeness check
- [ ] Cursor integration testing

### Release Process
1. Version bump in pyproject.toml
2. Generate changelog
3. Create GitHub release
4. Publish to PyPI (if desired)
5. Update installation documentation

### Post-Release Monitoring
- [ ] Monitor cache performance and hit rates
- [ ] Track API usage patterns
- [ ] Collect user feedback on documentation quality
- [ ] Performance metrics in production environments

This technical plan provides a comprehensive roadmap for implementing the AutoDocs MCP Server while maintaining high code quality, testability, and adherence to SOLID principles throughout the development process.
