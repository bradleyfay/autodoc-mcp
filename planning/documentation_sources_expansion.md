# Documentation Sources Expansion Plan

## Overview

This document outlines the comprehensive plan for expanding AutoDocs MCP Server beyond PyPI to support multiple documentation sources. The goal is to provide rich, contextual documentation from the most valuable sources for each package.

## Current State

**Implemented**: PyPI JSON API integration with AI-optimized formatting
**Architecture**: Clean `DocumentationFetcherInterface` ready for extension
**Coverage**: Basic package metadata and descriptions

## Documentation Source Tiers

### Tier 1: Essential Sources (High ROI)
- **GitHub README/Wiki**: Rich usage examples and getting started guides
- **Read the Docs**: Comprehensive API documentation and tutorials
- **GitHub Source Code**: Function signatures, docstrings, real examples

### Tier 2: Specialized Sources
- **GitHub Issues/Discussions**: Common problems and community solutions
- **Stack Overflow**: Real-world usage patterns and troubleshooting
- **Package Changelogs**: Version-specific changes and migration guides

### Tier 3: Advanced Sources
- **Jupyter Notebooks**: Interactive tutorial examples from repositories
- **Blog Posts/Tutorials**: Community-generated learning content
- **Package Tests**: Usage examples and comprehensive edge cases

## Implementation Phases

### Phase 1: GitHub Integration (1-2 weeks)

#### Objectives
- Extract repository URLs from PyPI metadata
- Fetch and format README files
- Scan examples directories
- Extract key source code documentation

#### Technical Implementation

**New Components**:
```python
class GitHubDocumentationFetcher(DocumentationFetcherInterface):
    """Fetch documentation from GitHub repositories"""

    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        # 1. Get repository URL from PyPI metadata
        # 2. Fetch README via GitHub API
        # 3. Scan examples/ docs/ directories
        # 4. Extract docstrings from key modules

    def format_documentation(self, package_info: PackageInfo, query: str | None = None) -> str:
        # Format with sections: README, Examples, Key APIs
```

**Key Features**:
- Repository URL extraction from PyPI `project_urls`
- README parsing (Markdown, RST, plain text)
- Examples directory scanning and filtering
- Intelligent content prioritization
- GitHub API rate limiting (5000/hour authenticated)
- Content caching with commit hash versioning

**Technical Challenges**:
- Inconsistent repository URL formats in PyPI metadata
- Large repository content filtering and selection
- Various README formats and quality levels
- GitHub API authentication and rate limiting

**Success Metrics**:
- 80%+ package coverage with discoverable repositories
- README extraction for major package formats
- Measurable improvement in AI code suggestions

#### Implementation Tasks
1. **Repository URL Resolution** (2 days)
   - Parse PyPI `project_urls` for GitHub/GitLab links
   - Handle URL variations and redirects
   - Fallback strategies for missing URLs

2. **GitHub API Integration** (3 days)
   - Implement authenticated GitHub API client
   - README file fetching with format detection
   - Directory traversal for examples/docs
   - Rate limiting and error handling

3. **Content Processing** (2 days)
   - Markdown/RST to formatted text conversion
   - Code example extraction and highlighting
   - Content length management and truncation
   - Query-based filtering integration

4. **Caching Strategy** (1 day)
   - Repository-specific cache keys with commit hashes
   - Intelligent cache invalidation
   - Performance optimization

5. **Testing & Integration** (2 days)
   - Unit tests for GitHub API integration
   - Integration tests with real repositories
   - Performance benchmarking
   - Error handling validation

---

### Phase 2: Read the Docs Integration (1 week)

#### Objectives
- Detect and access Read the Docs documentation sites
- Extract structured API documentation
- Parse tutorial and guide sections
- Handle multiple documentation formats

#### Technical Implementation

**New Components**:
```python
class ReadTheDocsFetcher(DocumentationFetcherInterface):
    """Fetch structured documentation from Read the Docs sites"""

    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        # 1. Detect RTD documentation URL
        # 2. Scrape API reference sections
        # 3. Extract tutorials and guides
        # 4. Parse code examples
```

**Key Features**:
- RTD URL detection from PyPI metadata and conventions
- Documentation site scraping with structure preservation
- API reference extraction (classes, functions, parameters)
- Tutorial and guide section identification
- Version-specific documentation routing
- Support for Sphinx, MkDocs, GitBook formats

**Technical Challenges**:
- Inconsistent documentation URL patterns across packages
- Various site structures and navigation schemes
- JavaScript-heavy documentation sites requiring rendering
- Version routing and canonical URL detection
- Content extraction from complex HTML structures

**Success Metrics**:
- Documentation found for 60%+ of major Python packages
- Successful API reference extraction
- Structured content integration with existing formatting

#### Implementation Tasks
1. **URL Detection** (1 day)
   - RTD URL pattern recognition from PyPI data
   - Convention-based URL guessing (packagename.readthedocs.io)
   - Site availability and structure validation

2. **Content Scraping** (2 days)
   - HTML parsing with BeautifulSoup/lxml
   - Navigation structure analysis
   - API reference section identification
   - Tutorial content extraction

3. **Format Support** (2 days)
   - Sphinx documentation parsing
   - MkDocs site structure handling
   - GitBook format support
   - Generic HTML documentation fallback

4. **Integration** (1 day)
   - Content formatting for AI consumption
   - Merge with existing PyPI and GitHub content
   - Query filtering implementation

5. **Testing** (1 day)
   - Test with major packages (requests, pydantic, fastapi)
   - Performance optimization
   - Error handling for unreachable sites

---

### Phase 3: Multi-Source Aggregation (1 week)

#### Objectives
- Intelligently combine content from multiple sources
- Implement token budget management
- Create configurable source prioritization
- Handle source failures gracefully

#### Technical Implementation

**New Components**:
```python
class MultiSourceDocumentationFetcher:
    """Aggregate and intelligently combine multiple documentation sources"""

    def __init__(self, fetchers: List[DocumentationFetcherInterface]):
        self.fetchers = fetchers
        self.prioritization_rules = self._load_prioritization_config()

    async def fetch_comprehensive_docs(self, package_name: str, query: str | None = None) -> str:
        # 1. Fetch from all available sources concurrently
        # 2. Apply source prioritization based on package type
        # 3. Deduplicate and merge content
        # 4. Respect token budget constraints
        # 5. Format for optimal AI consumption
```

**Key Features**:
- Concurrent fetching from multiple sources with failure isolation
- Intelligent source prioritization per package type
- Content deduplication and overlap detection
- Token budget management with configurable limits
- Smart content merging with section organization
- Graceful degradation when sources fail
- Configurable source preferences and weights

**Source Prioritization Strategy**:
- **Basic Info**: PyPI (always first - fast, reliable)
- **Usage Examples**: GitHub README (high priority for examples)
- **API Reference**: Read the Docs (structured API documentation)
- **Troubleshooting**: GitHub Issues/Stack Overflow (when query suggests problems)

**Technical Challenges**:
- Content overlap detection and intelligent deduplication
- Optimal content combination within token limits
- Performance optimization with multiple concurrent requests
- Source reliability and failure handling
- Content quality assessment and prioritization

**Success Metrics**:
- Comprehensive documentation for 90%+ of packages
- Sub-5-second response times for multi-source requests
- Measurably improved AI coding assistance quality
- Graceful handling of source failures

#### Implementation Tasks
1. **Concurrent Fetching Architecture** (2 days)
   - Async source coordination with asyncio
   - Failure isolation and timeout handling
   - Progress tracking and partial results

2. **Content Merging Logic** (2 days)
   - Overlap detection algorithms
   - Section-based content organization
   - Duplicate removal while preserving context
   - Quality-based content prioritization

3. **Token Budget Management** (1 day)
   - Configurable token limits per source
   - Content truncation strategies
   - Priority-based content selection
   - Dynamic budget allocation

4. **Configuration System** (1 day)
   - Source prioritization rules by package type
   - User preference configuration
   - Package-specific override rules
   - Performance tuning parameters

5. **Testing & Optimization** (1 day)
   - Performance benchmarking with real packages
   - Content quality validation
   - Error handling comprehensive testing
   - Memory and CPU usage optimization

## Architecture Considerations

### Interface Extensions
```python
class DocumentationFetcherInterface(ABC):
    @abstractmethod
    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        """Fetch package information from external source."""

    @abstractmethod
    def format_documentation(self, package_info: PackageInfo, query: str | None = None) -> str:
        """Format package info for AI consumption."""

    @abstractmethod  # New
    def get_source_priority(self, package_type: str, query_type: str) -> int:
        """Return priority score for this source given context."""

    @abstractmethod  # New
    def estimate_token_cost(self, package_name: str) -> int:
        """Estimate token cost for this source's content."""
```

### Caching Strategy Extensions
- **Multi-source cache keys**: `{package}-{version}-{sources_hash}`
- **Incremental caching**: Cache individual sources separately, combine on demand
- **Cache warming**: Pre-populate cache for popular packages
- **Intelligent invalidation**: Source-specific cache expiration

### Error Handling Strategy
- **Graceful degradation**: Continue with available sources when others fail
- **Source health monitoring**: Track success rates and adjust priorities
- **Retry strategies**: Source-specific retry logic with backoff
- **User feedback**: Clear indication of which sources were used/failed

## Testing Strategy

### Unit Tests
- Individual fetcher testing with mocked APIs
- Content formatting and filtering validation
- Error handling and edge case coverage
- Performance benchmarking for each source

### Integration Tests
- Multi-source aggregation with real packages
- Token budget management validation
- Cache behavior across source combinations
- End-to-end MCP tool testing

### Performance Tests
- Response time benchmarks for popular packages
- Memory usage profiling with large documentation sets
- Concurrent request handling validation
- Cache performance optimization

## Deployment Considerations

### Configuration Management
- Source enable/disable toggles
- Priority weight adjustments
- Token budget configuration
- Rate limiting parameters

### Monitoring and Observability
- Source success/failure rates
- Response time tracking per source
- Token usage analytics
- Cache hit/miss ratios

### Rollout Strategy
- Feature flags for gradual source enablement
- A/B testing for content quality validation
- Performance monitoring during rollout
- User feedback collection and analysis

This expansion will transform AutoDocs from a basic PyPI lookup tool into a comprehensive documentation intelligence system, providing AI assistants with rich, contextual information from the most valuable sources for each package.
