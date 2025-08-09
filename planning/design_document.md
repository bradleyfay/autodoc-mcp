# AutoDocs MCP Server - Design Document

## 1. System Overview

### Purpose
AutoDocs MCP Server automatically provides AI assistants with contextual, version-specific documentation for Python project dependencies, eliminating manual package lookup and improving AI coding assistance accuracy.

### Core Principles
- **Single Responsibility**: Each module handles one specific aspect of functionality
- **Open/Closed**: Extensible architecture for future enhancement phases
- **Dependency Inversion**: Abstractions over concretions for testability
- **Interface Segregation**: Focused interfaces for specific use cases
- **DRY**: Shared utilities and common patterns

## 2. Architecture Overview

### High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │◄───┤   FastMCP Server │────►│  Core Services  │
│   (Cursor)      │    │   (stdio/http)   │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   MCP Tools      │    │  External APIs  │
                       │   - scan_deps    │    │  - PyPI JSON    │
                       │   - get_docs     │    │  - Cache Layer  │
                       │   - refresh      │    │                 │
                       └──────────────────┘    └─────────────────┘
```

### Component Layers
1. **Transport Layer**: FastMCP server handling MCP protocol
2. **Service Layer**: Business logic and orchestration
3. **Data Layer**: PyPI API integration and caching
4. **Utility Layer**: Common functionality and error handling

## 3. Detailed Component Design

### 3.1 Core Services

#### DependencyParser
**Responsibility**: Parse pyproject.toml files and extract dependency information

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from pathlib import Path

class DependencySpec:
    """Value object representing a dependency specification"""
    name: str
    version_constraint: Optional[str]
    extras: List[str]
    source: str  # 'project', 'dev', etc.

class DependencyParserInterface(ABC):
    @abstractmethod
    def parse_project(self, project_path: Path) -> List[DependencySpec]:
        """Parse project dependencies from pyproject.toml"""
        pass

    @abstractmethod
    def validate_file(self, file_path: Path) -> bool:
        """Validate pyproject.toml file structure"""
        pass

class PyProjectParser(DependencyParserInterface):
    """Concrete implementation for pyproject.toml parsing"""
```

#### DocumentationFetcher
**Responsibility**: Retrieve and format package documentation from PyPI

```python
class PackageInfo:
    """Value object for package information"""
    name: str
    version: str
    summary: str
    description: str
    home_page: Optional[str]
    project_urls: Dict[str, str]
    author: Optional[str]
    license: Optional[str]

class DocumentationFetcherInterface(ABC):
    @abstractmethod
    async def fetch_package_info(self, package_name: str) -> PackageInfo:
        """Fetch package information from PyPI"""
        pass

    @abstractmethod
    def format_documentation(self, package_info: PackageInfo, query: Optional[str] = None) -> str:
        """Format package info for AI consumption"""
        pass

class PyPIDocumentationFetcher(DocumentationFetcherInterface):
    """Implementation using PyPI JSON API"""
```

#### CacheManager
**Responsibility**: Handle local caching with expiration and validation

```python
class CacheEntry:
    """Value object for cache entries"""
    data: PackageInfo
    timestamp: datetime
    version: str

class CacheManagerInterface(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[CacheEntry]:
        """Retrieve cached entry if valid"""
        pass

    @abstractmethod
    async def set(self, key: str, data: PackageInfo) -> None:
        """Store entry in cache"""
        pass

    @abstractmethod
    async def invalidate(self, key: Optional[str] = None) -> None:
        """Invalidate specific key or entire cache"""
        pass

class FileCacheManager(CacheManagerInterface):
    """JSON file-based cache implementation"""
```

### 3.2 MCP Tools Layer

#### Tool Definitions
Each MCP tool is implemented as a decorated function with clear input/output contracts:

```python
@mcp.tool
async def scan_dependencies(project_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Scan project dependencies from pyproject.toml

    Args:
        project_path: Path to project directory (defaults to current)

    Returns:
        JSON with dependency specifications and metadata
    """

@mcp.tool
async def get_package_docs(package_name: str, query: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve formatted documentation for a package

    Args:
        package_name: Name of the package
        query: Optional filter for specific documentation sections

    Returns:
        Formatted documentation with metadata
    """

@mcp.tool
async def refresh_cache() -> Dict[str, Any]:
    """
    Refresh the local documentation cache

    Returns:
        Statistics about cache refresh operation
    """
```

### 3.3 Error Handling Strategy

#### Hierarchical Exception Design
```python
class AutoDocsError(Exception):
    """Base exception for all AutoDocs errors"""
    pass

class ProjectParsingError(AutoDocsError):
    """Errors related to project file parsing"""
    def __init__(self, file_path: Path, line_number: Optional[int] = None):
        self.file_path = file_path
        self.line_number = line_number

class NetworkError(AutoDocsError):
    """Network-related errors with retry information"""
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after

class CacheError(AutoDocsError):
    """Cache-related errors"""
    pass
```

#### Error Response Format
```json
{
  "success": false,
  "error": {
    "type": "ProjectParsingError",
    "message": "Invalid pyproject.toml at line 15: missing [project] section",
    "details": {
      "file_path": "/path/to/pyproject.toml",
      "line_number": 15,
      "suggestion": "Add [project] section with dependencies"
    }
  }
}
```

## 4. Data Flow Design

### 4.1 Dependency Scanning Flow
```
User Request → MCP Tool → DependencyParser → File Validation →
Dependency Extraction → Response Formatting → MCP Response
```

### 4.2 Documentation Retrieval Flow
```
User Request → MCP Tool → Cache Check → [Cache Miss] →
PyPI API Call → Rate Limiting → Response Processing →
Cache Storage → Documentation Formatting → MCP Response
```

### 4.3 Cache Refresh Flow
```
User Request → MCP Tool → Cache Enumeration →
Batch PyPI Requests → Progress Tracking →
Cache Updates → Statistics Collection → MCP Response
```

## 5. Performance Considerations

### 5.1 Caching Strategy
- **Cache Key Format**: `{package_name}_{version_hash}.json`
- **Expiration**: 24 hours from creation
- **Storage**: Local JSON files in configurable directory
- **Cleanup**: Automatic removal of expired entries

### 5.2 Rate Limiting
- **PyPI Requests**: Maximum 10 concurrent requests
- **Backoff Strategy**: Exponential backoff with jitter
- **Timeout Handling**: 30-second timeout with retry logic

### 5.3 Memory Management
- **Streaming Responses**: Process large documentation in chunks
- **Cache Size Limits**: Maximum 100MB cache directory
- **Resource Cleanup**: Proper async resource management

## 6. Security Considerations

### 6.1 Input Validation
- **Path Traversal**: Validate project paths against working directory
- **File Size Limits**: Maximum 10MB for pyproject.toml files
- **Content Validation**: Schema validation for TOML structures

### 6.2 Network Security
- **HTTPS Only**: All PyPI requests over HTTPS
- **Timeout Protection**: Prevent resource exhaustion
- **Content Sanitization**: Clean external content before caching

## 7. Configuration Management

### 7.1 Environment Variables
```python
AUTODOCS_CACHE_DIR: str = "~/.autodocs/cache"
AUTODOCS_CACHE_TTL: int = 86400  # 24 hours
AUTODOCS_MAX_CONCURRENT: int = 10
AUTODOCS_REQUEST_TIMEOUT: int = 30
AUTODOCS_LOG_LEVEL: str = "INFO"
```

### 7.2 Configuration Schema
```python
@dataclass
class AutoDocsConfig:
    cache_dir: Path
    cache_ttl: int
    max_concurrent: int
    request_timeout: int
    log_level: str

    @classmethod
    def from_env(cls) -> 'AutoDocsConfig':
        """Load configuration from environment variables"""
```

## 8. Testing Strategy

### 8.1 Unit Testing
- **Parser Tests**: Valid/invalid pyproject.toml files
- **Fetcher Tests**: Mock PyPI responses and error conditions
- **Cache Tests**: Storage, retrieval, and expiration logic

### 8.2 Integration Testing
- **End-to-End**: Full MCP tool execution flows
- **Network Tests**: Real PyPI API interactions with rate limiting
- **File System**: Cache operations across different environments

### 8.3 Test Package Matrix
- **Pydantic**: Clean documentation format
- **Pandas**: Large, complex documentation
- **PySpark**: Mixed documentation quality
- **FastAPI**: Rich project URLs and metadata

## 9. Monitoring and Observability

### 9.1 Logging Structure
```python
logger.info("scan_dependencies", extra={
    "project_path": str(project_path),
    "dependencies_found": len(dependencies),
    "duration_ms": duration
})
```

### 9.2 Metrics Collection
- **Request Latency**: Per-tool response times
- **Cache Hit Rate**: Percentage of cached responses
- **Error Rates**: By error type and frequency
- **PyPI API Usage**: Request patterns and rate limiting events

## 10. Future Evolution Points

### 10.1 Phase 2 Preparation
- **Semantic Search Interface**: Abstract search functionality
- **Content Ranking**: Pluggable relevance scoring
- **Embedding Storage**: Abstract vector database interface

### 10.2 Extensibility
- **Parser Registry**: Support for additional project file formats
- **Documentation Sources**: Beyond PyPI (GitHub, ReadTheDocs)
- **Content Processors**: Custom documentation formatting rules

This design provides a solid foundation for the MVP while maintaining extensibility for future phases and adhering to SOLID principles throughout the architecture.
