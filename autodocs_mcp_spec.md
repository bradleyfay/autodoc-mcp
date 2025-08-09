# AutoDocs MCP Server - Complete Product Specification

## Problem Statement
Software developers frequently context-switch to browse package documentation while coding, breaking flow. Current AI assistants lack contextual awareness of project-specific dependencies and their documentation, leading to generic suggestions that may not match the exact versions being used.

## Core Value Proposition
Automatically parse Python project dependency files and provide AI assistants with contextual, version-specific documentation and source code for all project dependencies, eliminating manual package lookup and providing more accurate coding assistance.

## Market Opportunity
- Existing MCP servers provide general package documentation lookup but don't automatically parse project dependencies
- No solution bridges the gap between dependency management and AI-assisted coding
- Growing market of AI-powered development tools (Cursor, GitHub Copilot, etc.)

## Critical Assumptions to Validate
1. **Developer Pain Point**: Developers actually struggle with frequent documentation lookup
2. **AI Context Value**: AI assistants perform significantly better with package-specific context
3. **Documentation Quality**: Well-structured documentation will improve AI suggestions more than source code alone
4. **Integration Workflow**: Developers prefer automatic context provision vs. explicit requests
5. **Performance**: Documentation fetching overhead won't slow AI interactions unacceptably
6. **Version Accuracy**: Providing exact version context is more valuable than general package knowledge

## MVP Specification

### Core Features
- **Single File Parser**: pyproject.toml parsing only (skip requirements.txt, poetry, pipenv)
- **Basic Documentation Source**: PyPI JSON API for package metadata
- **Simple Caching**: Local JSON file storage (no database)
- **Three MCP Tools**: scan_dependencies, get_package_docs, refresh_cache
- **Cursor Integration**: stdio transport for immediate testing

### Technical Requirements

#### Project Structure
```
autodocs-mcp/
├── pyproject.toml          # Project config with FastMCP, TOML, requests deps
├── main.py                 # FastMCP server entry point
├── dependency_parser.py    # pyproject.toml parsing logic
├── doc_fetcher.py         # PyPI API calls and caching
├── cache_manager.py       # Local JSON cache operations
└── README.md              # Setup and integration instructions
```

#### MCP Tool Specifications

**scan_dependencies**
- Parameters: `project_path` (optional, defaults to current directory)
- Functionality: Parse pyproject.toml, extract dependencies from [project] table
- Returns: JSON with package names and version constraints

**get_package_docs**
- Parameters: `package_name` (required), `query` (optional for filtering)
- Functionality: Check cache, fetch from PyPI if needed, return relevant documentation
- Returns: Formatted documentation with description, URLs, examples

**refresh_cache**
- Parameters: None
- Functionality: Clear local cache, re-fetch all previously cached packages
- Returns: Success confirmation and statistics

#### API Integration
- **PyPI Endpoint**: `https://pypi.org/pypi/{package_name}/json`
- **Extract Fields**: info.summary, info.home_page, info.project_urls, info.author
- **Rate Limiting**: Simple retry logic with exponential backoff
- **Cache**: 24-hour expiration, {package_name}.json files

#### Error Handling
- Network timeouts: Graceful error messages with retry suggestions
- Invalid pyproject files: Specific parsing errors with line numbers
- Missing packages: "Package not found" with similar package suggestions
- Cache corruption: Automatic refresh trigger

### Test Package Selection
**High-quality docs**: Pydantic (clean, well-structured)
**Overwhelming docs**: pandas (comprehensive but verbose)
**Poor docs**: PySpark (Java-heavy, confusing structure)
**Additional test cases**: Dask, Plotly, MLflow

### Success Metrics
- Parse real Python projects with 5+ dependencies in <5 seconds
- Provide useful documentation for 80%+ of common packages
- Measurable developer time savings vs manual lookup
- A/B test: documentation vs source code vs hybrid approach

## Product Evolution Strategy

### Phase 1: MVP Validation
- Basic text search within documentation
- Validate core assumption about AI performance improvement
- Test with 3 contrasting packages (Pydantic, pandas, PySpark)

### Phase 2: Smart Context Selection
- Add query parameter for targeted documentation sections
- Implement semantic search using local embeddings (Sentence Transformers)
- Use models like "all-MiniLM-L6-v2" (90MB, runs locally)
- Store embeddings in ChromaDB or numpy arrays

### Phase 3: Project Intelligence
- Learn user coding patterns and preferences
- Build semantic profile of architectural choices
- Track which documentation sections lead to successful code
- Prioritize documentation based on project context

### Architecture Considerations

#### Documentation vs Source Code
**Hypothesis**: Source code + minimal docs outperforms verbose documentation
**Rationale**:
- LLMs excel at reading source code directly
- Source code is unambiguous about parameters, returns, edge cases
- Version-specific source solves training data staleness problem

**Testing Strategy**: A/B test three approaches:
1. Documentation only
2. Source code only
3. Smart hybrid (source + targeted docs)

#### Context Window Management
**Current Limits**: Claude 3.5 Sonnet (200K tokens), GPT-4 (128K tokens)
**Token Budget**: Reserve ~20% (40K tokens) for injected context
**Selection Strategy**:
- Typical function: 10-50 tokens
- Class definition: 100-500 tokens
- Complete module: 1,000-10,000 tokens
- Prioritize by relevance score, truncate gracefully

## Competitive Positioning
**vs. Cursor's codebase awareness**: Extends AI context to entire dependency ecosystem
**vs. GitHub Copilot**: Version-specific accuracy prevents outdated suggestions
**vs. Manual documentation lookup**: Automatic, contextual, integrated workflow

## Technical Implementation Strategy
Use **prompt engineering with context injection** rather than fine-tuning:
- Keep using foundation models (Claude, GPT-4)
- Competitive advantage in intelligent context selection
- Benefit from automatic model improvements
- More scalable than maintaining custom models

## Integration Requirements
**Cursor Desktop Configuration**:
```json
{
  "mcpServers": {
    "autodocs-mcp": {
      "command": "uv",
      "args": ["run", "main.py"],
      "env": {
        "CACHE_DIR": "/path/to/cache"
      }
    }
  }
}
```

**Server Configuration**:
- Transport: stdio (for Cursor compatibility)
- Logging: stderr only (never stdout for MCP compliance)
- Server name: "autodocs-mcp"
- Tool descriptions: Clear explanations for AI understanding

## Next Steps
1. Build MVP with FastMCP framework
2. Test with selected packages on real Python projects
3. Measure AI coding performance improvement
4. Validate critical assumptions through user testing
5. Plan Phase 2 semantic search implementation
