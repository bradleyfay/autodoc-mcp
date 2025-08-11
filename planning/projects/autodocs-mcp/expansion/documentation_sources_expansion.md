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
- **llms.txt Files**: AI-optimized documentation following the emerging standard

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

### Phase 2.5: llms.txt Integration (3-5 days)

#### Overview
The llms.txt standard, proposed in September 2024, provides a standardized way for websites to offer LLM-friendly documentation. This emerging standard is rapidly gaining adoption across major platforms (Anthropic, Mintlify, Cursor) and represents a significant opportunity for high-quality, AI-optimized documentation.

#### Objectives
- Detect and fetch llms.txt files from project websites and documentation sites
- Parse the standardized format for structured content extraction
- Prioritize llms.txt content due to its AI-optimized nature
- Support both `/llms.txt` and `/llms-full.txt` variations

#### Technical Implementation

**New Components**:
```python
class LLMsTxtFetcher(DocumentationFetcherInterface):
    """Fetch AI-optimized documentation from llms.txt files"""

    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        # 1. Detect llms.txt URLs from project metadata
        # 2. Try standard locations: {homepage}/llms.txt, {docs_url}/llms.txt
        # 3. Fetch and parse structured markdown content
        # 4. Extract project summary, navigation, and file lists

    def format_documentation(self, package_info: PackageInfo, query: str | None = None) -> str:
        # Format prioritizing llms.txt structured content
```

**Key Features**:
- **URL Discovery**: Extract homepage/documentation URLs from PyPI metadata
- **Standard Compliance**: Support official llms.txt specification format
- **Priority Content**: Treat llms.txt as highest-quality source for AI consumption
- **Dual File Support**: Handle both `/llms.txt` (navigation) and `/llms-full.txt` (comprehensive)
- **Validation**: Verify proper markdown structure and required H1 header
- **Caching**: Version-aware caching with content hash validation

**llms.txt Format Specification**:
- **Location**: Root path `/llms.txt` of website
- **Required**: H1 header with project/site name
- **Optional**: Blockquote with project summary
- **Structure**: Markdown with H2 sections containing file lists
- **Links**: `[Title](URL): Optional description` format
- **Sections**: Organized by topic/category with clear hierarchy

**URL Discovery Strategy**:
1. **Primary Sources**: `homepage_url` and `documentation_url` from PyPI metadata
2. **Common Patterns**: GitHub Pages, Read the Docs, custom documentation sites
3. **Fallback Discovery**: Repository root README links to documentation sites
4. **Standard Locations**: Try `{base_url}/llms.txt` and `{base_url}/llms-full.txt`

**Content Processing**:
- **Header Extraction**: Project name from required H1
- **Summary Parsing**: Optional blockquote project description
- **Navigation Structure**: H2 sections with organized link lists
- **Link Processing**: Extract titles, URLs, and optional descriptions
- **Content Validation**: Verify markdown structure and required elements

#### Implementation Priority Rationale
- **Highest Quality**: Content specifically optimized for AI consumption
- **Emerging Standard**: Early adoption provides competitive advantage
- **Rapid Adoption**: Major platforms already implementing (first-mover advantage)
- **Perfect Fit**: Directly addresses AutoDocs' use case for AI documentation
- **Low Complexity**: Simple format reduces implementation overhead
- **High Value**: Pre-structured content reduces processing complexity

#### Implementation Tasks
1. **URL Discovery** (1 day)
   - Extract documentation URLs from PyPI project metadata
   - Implement standard location checking logic
   - Handle URL variations and redirects
   - Add fallback discovery strategies

2. **Format Parser** (1 day)
   - Implement llms.txt markdown specification parser
   - Extract required H1 and optional blockquote
   - Parse H2 sections and structured link lists
   - Validate format compliance and handle variations

3. **Content Integration** (1 day)
   - Priority scoring for llms.txt content (highest available)
   - Content formatting for AI consumption
   - Integration with existing multi-source architecture
   - Query filtering implementation

4. **Caching & Performance** (1 day)
   - Content-hash based cache keys
   - HTTP caching header respect
   - Performance optimization for batch requests
   - Error handling for unreachable files

5. **Testing & Validation** (1 day)
   - Test with existing llms.txt implementations
   - Content quality validation
   - Integration testing with real projects
   - Error handling for malformed files

#### Success Metrics
- **Discovery Rate**: Successfully locate llms.txt files for packages with documentation sites
- **Content Quality**: Measurably improved AI assistance quality from structured content
- **Performance**: Sub-second response times for llms.txt content
- **Adoption Tracking**: Monitor ecosystem adoption and adjust discovery strategies
- **Standard Compliance**: 100% compatibility with official llms.txt specification

#### Future Enhancements
- **Auto-generation**: Generate llms.txt files for projects that don't have them
- **Quality Assessment**: Score llms.txt content quality and completeness
- **Standard Evolution**: Track and implement specification updates
- **Community Contribution**: Contribute improvements back to llms.txt standard

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
- **AI-Optimized Content**: llms.txt files (highest priority - purpose-built for LLMs)
- **Basic Info**: PyPI (always first - fast, reliable baseline)
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

---

## Development Setup Documentation

### Claude Code Integration Setup
The AutoDocs MCP Server includes comprehensive Claude Code integration through the `CLAUDE.md` file in the project root. This file serves as the complete project context and development guide for Claude Code sessions.

#### CLAUDE.md Contents
- **Project Overview**: Complete technical architecture and implementation status
- **MCP Tools Available**: All 8 MCP tools with usage recommendations
- **Development Workflow**: Git branching strategy, commit standards, and semantic versioning
- **Technical Standards**: Testing patterns, dependency management, and code quality requirements
- **Configuration**: Environment variables, cache management, and deployment settings

#### Agent Architecture
The project employs a specialized agent architecture for different development concerns:

1. **core-services** (Orange) - Core business logic and performance optimization
2. **docs-integration** (Purple) - Technical documentation and API integration guides
3. **mcp-protocol** (Green) - MCP protocol implementation and client integration
4. **testing-specialist** (Blue) - Comprehensive testing strategies and pytest ecosystem
5. **production-ops** (Red) - Deployment, monitoring, and release management
6. **technical-writer** (Teal) - User-centered documentation using Diátaxis framework
7. **product-manager** (Indigo) - Roadmap prioritization and product specification evolution

Each agent has specialized knowledge and tools for their domain, enabling focused expertise while maintaining clear collaboration patterns.

#### Development Environment Setup
```bash
# Complete project setup for Claude Code sessions
uv sync  # Install all dependencies including dev tools
uv run python scripts/dev.py test-scan  # Validate dependency scanning
uv run python scripts/dev.py test-docs requests ">=2.28.0"  # Test documentation fetching

# Start MCP server for integration testing
uv run python -m autodocs_mcp.main
```

#### Agent Collaboration Patterns
- **Strategic Alignment**: product-manager ensures all development aligns with user value and roadmap priorities
- **Cross-Agent Communication**: Agents coordinate through shared understanding of project structure
- **Feature Development Pipeline**: product-manager defines requirements → core-services implements → testing-specialist validates → docs-integration/technical-writer document
- **Quality Assurance**: Multiple agents validate different aspects (product fit, technical accuracy, user experience, test coverage)
- **User Feedback Integration**: product-manager synthesizes feedback → collaborates with relevant agents for implementation

#### Product Management Integration
The **product-manager** agent serves as the strategic coordinator, ensuring all development efforts align with user needs and product vision:

- **Feature Prioritization**: Uses RICE framework to prioritize GitHub issues, user feedback, and agent-identified improvements
- **Product Spec Evolution**: Maintains living documentation that evolves based on user feedback and technical learnings
- **Cross-Functional Coordination**: Ensures technical decisions support user value and strategic objectives
- **Roadmap Management**: Balances immediate user needs with long-term product vision and technical debt

This agent-based approach ensures comprehensive coverage while maintaining specialized expertise in each domain, with clear strategic oversight from the product management perspective.
