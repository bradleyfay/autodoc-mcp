# Multi-Language Support Plan

## Overview

This document outlines the comprehensive strategy for expanding AutoDocs MCP Server to support multiple programming languages beyond Python. The goal is to create a universal documentation intelligence system that works across the most popular development ecosystems.

## Language Ecosystem Analysis

### Market Share and Priority Assessment
1. **JavaScript/Node.js**: ~65% of developers (Stack Overflow 2024)
2. **Python**: ~49% of developers (current implementation)
3. **Java**: ~35% of developers (enterprise heavy)
4. **C#/.NET**: ~28% of developers (Microsoft ecosystem)
5. **Go**: ~15% of developers (growing rapidly)
6. **Rust**: ~13% of developers (systems programming, growing)

## Architecture Strategy

### Universal Design Principles
- **Language-agnostic core**: Dependency parsing and documentation fetching interfaces
- **Plugin architecture**: Language-specific parsers and fetchers as implementations
- **Unified caching**: Cross-language cache management with language prefixes
- **Consistent MCP interface**: Same tools work across all languages

### Core Abstractions
```python
class LanguageEcosystem(ABC):
    """Abstract base for language-specific implementations"""

    @abstractmethod
    def get_dependency_parser(self) -> DependencyParserInterface:
        """Return language-specific dependency parser"""

    @abstractmethod
    def get_documentation_fetchers(self) -> List[DocumentationFetcherInterface]:
        """Return available documentation sources for this language"""

    @abstractmethod
    def detect_project_language(self, project_path: Path) -> bool:
        """Detect if project uses this language"""

class UniversalMCPServer:
    """Language-agnostic MCP server that delegates to language ecosystems"""

    def __init__(self):
        self.ecosystems = [
            PythonEcosystem(),
            NodeJSEcosystem(),
            DotNetEcosystem(),
            # ... other languages
        ]
```

## Language-Specific Implementation Plans

### 1. Node.js/JavaScript Support (2-3 weeks)

#### Ecosystem Overview
- **Package Manager**: npm, yarn, pnpm
- **Dependency Files**: `package.json`, `package-lock.json`, `yarn.lock`
- **Documentation Sources**: npmjs.com, GitHub, JSDoc, TypeScript definitions

#### Implementation Plan

**Phase 1A: Dependency Parsing (1 week)**
```python
class NodeJSDependencyParser(DependencyParserInterface):
    """Parse Node.js project dependencies"""

    def parse_dependencies(self, project_path: Path) -> List[Dependency]:
        # 1. Parse package.json (dependencies, devDependencies, peerDependencies)
        # 2. Parse lock files for exact versions
        # 3. Handle scoped packages (@org/package)
        # 4. Resolve workspace dependencies (monorepos)
```

**Key Features**:
- `package.json` parsing with all dependency types
- Lock file integration for exact version resolution
- Scoped package handling (`@types/*`, `@babel/*`)
- Workspace and monorepo support
- TypeScript vs JavaScript distinction

**Technical Challenges**:
- Complex dependency trees with peer dependencies
- Monorepo workspace resolution
- Version range semantics different from Python
- TypeScript definition packages vs runtime packages

**Phase 1B: Documentation Sources (1-2 weeks)**
```python
class NPMDocumentationFetcher(DocumentationFetcherInterface):
    """Fetch documentation from npm registry and related sources"""

    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        # 1. Fetch from npm registry API
        # 2. Extract README from registry data
        # 3. Get GitHub repository information
        # 4. Parse TypeScript definition files
```

**Documentation Sources**:
- **npm Registry API**: `https://registry.npmjs.org/{package}`
- **GitHub Integration**: Same as Python (README, examples, source)
- **TypeScript Definitions**: JSDoc extraction from .d.ts files
- **npmjs.com**: Package pages with usage statistics
- **unpkg.com**: Direct source code access

**Unique Challenges**:
- TypeScript vs JavaScript documentation differences
- Complex ecosystem with many micro-packages
- Documentation quality varies significantly
- Framework-specific documentation patterns (React, Angular, Vue)

#### Testing Strategy
- **Test Packages**: express, react, lodash, axios, typescript
- **Monorepo Testing**: Lerna/Rush/Nx based projects
- **TypeScript Integration**: @types/* packages and inline definitions

---

### 2. .NET Support (2-3 weeks)

#### Ecosystem Overview
- **Package Manager**: NuGet
- **Dependency Files**: `.csproj`, `packages.config`, `Directory.Build.props`
- **Documentation Sources**: nuget.org, docs.microsoft.com, GitHub, XML docs

#### Implementation Plan

**Phase 2A: Dependency Parsing (1 week)**
```python
class DotNetDependencyParser(DependencyParserInterface):
    """Parse .NET project dependencies"""

    def parse_dependencies(self, project_path: Path) -> List[Dependency]:
        # 1. Parse .csproj files (PackageReference elements)
        # 2. Handle packages.config (legacy format)
        # 3. Parse Directory.Build.props for centralized management
        # 4. Resolve target framework dependencies
```

**Key Features**:
- `.csproj` XML parsing for PackageReference elements
- Legacy `packages.config` support
- Centralized package management with `Directory.Build.props`
- Target framework specific dependencies
- Version constraint resolution
- Multi-targeting project support

**Technical Challenges**:
- Multiple project file formats (.csproj, .vbproj, .fsproj)
- Complex target framework matrix
- Legacy vs modern .NET differences
- Enterprise package sources (private NuGet feeds)

**Phase 2B: Documentation Sources (1-2 weeks)**
```python
class NuGetDocumentationFetcher(DocumentationFetcherInterface):
    """Fetch documentation from NuGet and Microsoft ecosystem"""

    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        # 1. Fetch from NuGet API
        # 2. Get Microsoft Docs integration
        # 3. Parse XML documentation comments
        # 4. Extract GitHub repository information
```

**Documentation Sources**:
- **NuGet API**: `https://api.nuget.org/v3-flatcontainer/{package}`
- **Microsoft Docs**: docs.microsoft.com integration for official packages
- **GitHub Integration**: Repository documentation
- **XML Documentation**: Compiled XML doc files
- **Source Code**: Reference source and GitHub repositories

**Unique Challenges**:
- Microsoft-centric documentation ecosystem
- XML documentation file parsing
- .NET Framework vs .NET Core documentation differences
- Enterprise and private package repository integration

#### Testing Strategy
- **Test Packages**: Newtonsoft.Json, Entity Framework, ASP.NET Core
- **Framework Variations**: .NET Framework, .NET Core, .NET 5+
- **Enterprise Scenarios**: Private NuGet feeds and packages

---

### 3. Java Support (3-4 weeks)

#### Ecosystem Overview
- **Build Systems**: Maven, Gradle, SBT (Scala), Apache Ivy
- **Dependency Files**: `pom.xml`, `build.gradle`, `ivy.xml`
- **Documentation Sources**: Maven Central, Javadoc, GitHub

#### Implementation Plan

**Phase 3A: Dependency Parsing (2 weeks)**
```python
class JavaDependencyParser(DependencyParserInterface):
    """Parse Java project dependencies from multiple build systems"""

    def parse_dependencies(self, project_path: Path) -> List[Dependency]:
        # 1. Detect build system (Maven vs Gradle vs SBT)
        # 2. Parse appropriate configuration files
        # 3. Handle dependency scopes and exclusions
        # 4. Resolve multi-module projects
```

**Key Features**:
- Multi-build system support (Maven, Gradle, SBT)
- Complex dependency scope handling (compile, test, runtime, provided)
- Dependency exclusion and version conflict resolution
- Multi-module project support
- Parent POM inheritance
- Gradle variant-aware dependency resolution

**Technical Challenges**:
- Multiple build systems with different syntax and semantics
- Complex dependency scopes and exclusions
- Version conflict resolution strategies
- Enterprise repository and mirror configuration
- Gradle's complex dependency model

**Phase 3B: Documentation Sources (1-2 weeks)**
```python
class MavenCentralDocumentationFetcher(DocumentationFetcherInterface):
    """Fetch documentation from Maven ecosystem"""

    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        # 1. Query Maven Central API
        # 2. Download and parse Javadoc
        # 3. Extract source code documentation
        # 4. Get GitHub repository information
```

**Documentation Sources**:
- **Maven Central**: search.maven.org API
- **Javadoc**: Generated API documentation
- **GitHub Integration**: Repository documentation
- **Oracle Docs**: Official Java API documentation
- **Spring Docs**: Framework-specific documentation for Spring ecosystem

**Unique Challenges**:
- GroupId/ArtifactId coordinate system vs simple package names
- Javadoc HTML parsing and extraction
- Enterprise repository integration
- Framework-specific documentation patterns (Spring, Android)

#### Testing Strategy
- **Test Packages**: Spring Framework, Apache Commons, Jackson, Hibernate
- **Build Systems**: Maven and Gradle projects
- **Enterprise Scenarios**: Private repositories and corporate proxies

---

### 4. Go Support (1-2 weeks)

#### Ecosystem Overview
- **Package Manager**: Go modules (built-in)
- **Dependency Files**: `go.mod`, `go.sum`
- **Documentation Sources**: pkg.go.dev, GitHub

#### Implementation Plan

**Phase 4A: Dependency Parsing (3-4 days)**
```python
class GoDependencyParser(DependencyParserInterface):
    """Parse Go module dependencies"""

    def parse_dependencies(self, project_path: Path) -> List[Dependency]:
        # 1. Parse go.mod for require statements
        # 2. Handle replace and exclude directives
        # 3. Parse go.sum for version verification
        # 4. Handle major version suffixes (v2, v3, etc.)
```

**Key Features**:
- `go.mod` parsing for require statements
- Replace and exclude directive handling
- Version checksum verification from `go.sum`
- Major version suffix handling in import paths
- Workspace mode support (Go 1.18+)

**Technical Challenges**:
- Major version semantics with URL path changes
- Replace directive complexity for local/fork dependencies
- Minimal version selection algorithm understanding

**Phase 4B: Documentation Sources (3-4 days)**
```python
class GoDocumentationFetcher(DocumentationFetcherInterface):
    """Fetch documentation from Go ecosystem"""

    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        # 1. Query pkg.go.dev API
        # 2. Extract package documentation
        # 3. Get GitHub repository information
        # 4. Parse inline Go documentation
```

**Documentation Sources**:
- **pkg.go.dev**: Official Go package documentation
- **GitHub Integration**: Repository documentation and examples
- **Inline Documentation**: Go doc comments and examples
- **Go Blog**: Official Go team blog posts and tutorials

**Unique Challenges**:
- Module path vs package import path confusion
- Major version URL routing on pkg.go.dev
- Minimal external documentation culture (relies heavily on inline docs)

#### Testing Strategy
- **Test Packages**: gorilla/mux, gin-gonic/gin, kubernetes/client-go
- **Version Scenarios**: v0, v1, v2+ major versions
- **Module Features**: Replace directives, workspace mode

---

### 5. Rust Support (2 weeks)

#### Ecosystem Overview
- **Package Manager**: Cargo
- **Dependency Files**: `Cargo.toml`, `Cargo.lock`
- **Documentation Sources**: docs.rs, crates.io, GitHub

#### Implementation Plan

**Phase 5A: Dependency Parsing (1 week)**
```python
class RustDependencyParser(DependencyParserInterface):
    """Parse Rust project dependencies"""

    def parse_dependencies(self, project_path: Path) -> List[Dependency]:
        # 1. Parse Cargo.toml dependencies sections
        # 2. Handle feature flags and optional dependencies
        # 3. Parse workspace configurations
        # 4. Handle build dependencies and dev dependencies
```

**Key Features**:
- `Cargo.toml` parsing for multiple dependency sections
- Feature flag resolution and optional dependencies
- Workspace member dependency management
- Build-time vs runtime dependency distinction
- Version requirement syntax (semantic versioning with extensions)

**Technical Challenges**:
- Feature-based conditional compilation
- Workspace dependency management complexity
- Optional dependency resolution
- Platform-specific dependencies

**Phase 5B: Documentation Sources (1 week)**
```python
class DocsRsDocumentationFetcher(DocumentationFetcherInterface):
    """Fetch documentation from Rust ecosystem"""

    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        # 1. Query crates.io API
        # 2. Fetch docs.rs documentation
        # 3. Extract README and repository information
        # 4. Parse feature flag documentation
```

**Documentation Sources**:
- **docs.rs**: Automatically generated documentation
- **crates.io**: Package registry with metadata
- **GitHub Integration**: Repository documentation and examples
- **The Rust Book**: Official language documentation integration

**Unique Challenges**:
- Feature flag documentation and examples
- Workspace vs single-crate documentation
- docs.rs build failures and fallback strategies

#### Testing Strategy
- **Test Packages**: serde, tokio, clap, reqwest
- **Feature Scenarios**: Default features, optional features, feature combinations
- **Workspace Testing**: Multi-crate workspace projects

## Universal Implementation Strategy

### Phase-by-Phase Rollout

**Phase 1: Foundation + Node.js (3-4 weeks)**
- Implement universal architecture
- Complete Node.js ecosystem support
- Multi-language MCP tool interface

**Phase 2: Rapid Expansion (4-5 weeks)**
- Go support (simple, validates architecture)
- .NET support (enterprise validation)

**Phase 3: Complex Ecosystems (6-8 weeks)**
- Java support (most complex dependency resolution)
- Rust support (feature flag complexity)

**Phase 4: Polish & Integration (2-3 weeks)**
- Cross-language dependency analysis
- Universal documentation aggregation
- Performance optimization

### Universal MCP Tools

```python
# Enhanced tools that work across all languages
class UniversalMCPTools:

    @mcp_tool
    async def scan_project_dependencies(self, project_path: str = ".") -> dict:
        """Scan project for dependencies across all supported languages"""
        # Auto-detect language(s) and parse dependencies

    @mcp_tool
    async def get_package_docs(self, package_name: str, language: str = None, query: str = None) -> str:
        """Get documentation for package in specified or detected language"""
        # Route to appropriate language ecosystem

    @mcp_tool
    async def analyze_cross_language_project(self, project_path: str = ".") -> dict:
        """Analyze multi-language projects (e.g., Python backend + Node.js frontend)"""
        # Detect and analyze multiple ecosystems in single project
```

### Language Detection Strategy
```python
class ProjectLanguageDetector:
    """Auto-detect programming languages used in a project"""

    DETECTION_RULES = {
        "python": ["pyproject.toml", "requirements.txt", "setup.py", "Pipfile"],
        "node": ["package.json", "yarn.lock", "package-lock.json"],
        "dotnet": ["*.csproj", "*.sln", "packages.config"],
        "java": ["pom.xml", "build.gradle", "ivy.xml"],
        "go": ["go.mod", "go.sum"],
        "rust": ["Cargo.toml", "Cargo.lock"],
    }

    def detect_languages(self, project_path: Path) -> List[str]:
        """Return list of detected languages in priority order"""
```

## Cross-Language Features

### Multi-Language Projects
- **Frontend + Backend**: Node.js + Python/Java/.NET
- **Microservices**: Multiple languages in single repository
- **Build Tools**: Language-agnostic tools (Docker, Make, etc.)

### Universal Documentation Aggregation
- Cross-reference related packages across languages
- Language ecosystem comparison and migration guides
- Universal dependency vulnerability scanning

### Performance Considerations
- Language-specific caching strategies
- Concurrent multi-language analysis
- Incremental parsing for large multi-language projects

## Testing Strategy

### Unit Tests
- Language-specific parser testing with real projects
- Documentation fetcher validation
- Cross-language project detection

### Integration Tests
- Multi-language project analysis
- Performance benchmarking across ecosystems
- Cache behavior with multiple languages

### Real-World Validation
- Popular open-source projects in each language
- Enterprise project scenarios
- Performance at scale testing

## Deployment and Rollout

### Feature Flags
- Per-language ecosystem enable/disable
- Gradual rollout to prevent system overload
- A/B testing for language-specific features

### Monitoring
- Language-specific success rates and performance
- Cross-language usage analytics
- Error tracking per ecosystem

### Documentation
- Language-specific setup guides
- Cross-language project examples
- Migration guides from language-specific tools

This multi-language expansion will position AutoDocs as the universal documentation intelligence platform for modern development teams working across diverse technology stacks.
