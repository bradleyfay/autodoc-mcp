# System Architecture

This document explains the architectural design of AutoDocs MCP Server, covering the layered architecture, component responsibilities, and design principles that guide the implementation.

## Architectural Overview

AutoDocs MCP Server follows a **modular, layered architecture** with comprehensive separation of concerns. The system is designed for production reliability, maintainability, and extensibility.

### Architecture Principles

1. **Layered Design**: Clear separation between infrastructure, core services, and application layers
2. **Dependency Inversion**: Higher layers depend on abstractions, not concrete implementations
3. **Single Responsibility**: Each module has a focused, well-defined purpose
4. **Graceful Degradation**: System continues operating with partial failures
5. **Async-First**: Full asynchronous support for optimal performance

## System Layers

### 1. Infrastructure Layer (`src/autodocs_mcp/`)

The infrastructure layer provides foundational services and system-level functionality.

#### Main Application (`main.py`)
- **FastMCP Server**: MCP protocol compliance with 8 exposed tools
- **Lifecycle Management**: Graceful startup, shutdown, and async resource management
- **Service Integration**: Coordinates all core services and manages their lifecycles

#### Configuration Management (`config.py`)
- **Environment-Aware**: Supports development, testing, and production configurations
- **Validation**: Comprehensive Pydantic-based validation with clear error messages
- **Defaults**: Sensible defaults for all configuration parameters

#### Security Layer (`security.py`)
- **Input Validation**: Sanitization of all user inputs and parameters
- **Path Security**: Secure handling of file paths and cache keys
- **URL Validation**: Validation of external URLs and endpoints

#### Observability (`observability.py`)
- **Metrics Collection**: Performance tracking and system monitoring
- **Structured Logging**: Production-ready logging with context preservation
- **Performance Monitoring**: Request timing, cache hit rates, and error tracking

#### Health Management (`health.py`)
- **Health Checks**: Comprehensive system health status for load balancers
- **Readiness Checks**: Kubernetes-style readiness probe for deployment orchestration
- **Dependency Monitoring**: Validation of external service availability

#### Data Models (`models.py`)
- **Type Safety**: Pydantic v2 models for all data structures
- **Serialization**: JSON serialization with proper error handling
- **Validation**: Runtime validation of all data structures

#### Exception Handling (`exceptions.py`)
- **Custom Hierarchy**: Structured exception types with context information
- **Error Context**: Detailed error information for debugging and user feedback
- **Recovery Guidance**: Actionable error messages with suggested solutions

### 2. Core Services Layer (`src/autodocs_mcp/core/`)

The core services layer implements business logic and domain-specific functionality.

#### Dependency Management

**Dependency Parser (`dependency_parser.py`)**
- **PyProject.toml Parsing**: Robust parsing with graceful degradation for malformed files
- **Dependency Extraction**: Parsing of [project] dependencies with version constraints
- **Error Recovery**: Continues processing with partial parsing failures

**Dependency Resolver (`dependency_resolver.py`)**
- **Enhanced Resolution**: Dependency resolution with conflict detection
- **Version Constraint Handling**: Complex version constraint parsing and validation
- **Transitive Dependencies**: Future support for dependency tree analysis

**Version Resolver (`version_resolver.py`)**
- **PyPI Integration**: Version constraint resolution using PyPI API
- **Caching**: Efficient caching of version resolution results
- **Fallback Strategies**: Graceful handling of version resolution failures

#### Documentation Services

**Documentation Fetcher (`doc_fetcher.py`)**
- **PyPI API Integration**: Fetching package metadata and documentation from PyPI
- **Concurrent Processing**: Parallel fetching of multiple packages with rate limiting
- **Content Processing**: Extraction and formatting of relevant documentation sections

**Context Fetcher (`context_fetcher.py`)**
- **Phase 4 Feature**: Comprehensive context fetching with dependency analysis
- **Smart Scoping**: Intelligent selection of relevant dependencies for AI context
- **Token Management**: Budget-aware context assembly for AI model limits

**Context Formatter (`context_formatter.py`)**
- **AI Optimization**: Documentation formatting optimized for AI consumption
- **Token Budget Management**: Automatic context truncation and prioritization
- **Query Filtering**: Targeted documentation section selection

#### Infrastructure Services

**Cache Manager (`cache_manager.py`)**
- **High-Performance Caching**: JSON file-based caching with version-specific keys
- **Immutable Keys**: Version-based cache keys (`{package_name}-{version}`) with no expiration
- **Corruption Recovery**: Automatic detection and recovery from corrupted cache entries

**Network Client (`network_client.py`)**
- **HTTP Abstraction**: Clean HTTP client interface with retry logic
- **Connection Pooling**: Efficient connection reuse with automatic cleanup
- **Request Management**: Timeout handling, request queuing, and resource limits

**Network Resilience (`network_resilience.py`)**
- **Circuit Breakers**: Advanced network reliability with failure detection
- **Exponential Backoff**: Smart retry strategies for transient failures
- **Connection Pool Management**: Automatic resource cleanup and health monitoring

**Error Formatter (`error_formatter.py`)**
- **User-Friendly Messages**: Structured error handling with clear, actionable messages
- **Error Context**: Detailed error information for debugging and troubleshooting
- **Recovery Suggestions**: Guidance for resolving common error conditions

## Component Interactions

### Request Flow Architecture

```
MCP Client Request
       ↓
FastMCP Server (main.py)
       ↓
Security Validation (security.py)
       ↓
Core Service Layer
   ├── Dependency Parser → Version Resolver
   ├── Context Fetcher → Doc Fetcher
   └── Cache Manager ← Network Client
       ↓
Network Resilience Layer
       ↓
External APIs (PyPI)
```

### Data Flow Patterns

1. **Dependency Scanning Flow**:
   - pyproject.toml → Dependency Parser → Dependency Resolver → Structured Response

2. **Documentation Fetching Flow**:
   - Package Request → Cache Check → Network Fetch → Format → Cache Store → Response

3. **Context Assembly Flow**:
   - Dependencies → Context Fetcher → Smart Scoping → Token Budget → Formatted Context

## Architectural Decisions

### Async-First Design

**Decision**: Full asynchronous architecture throughout the system
**Rationale**:
- I/O-bound operations (network requests, file operations) benefit significantly from async
- Better resource utilization for concurrent operations
- Scalability for handling multiple simultaneous requests

**Implementation**:
- All service methods are async
- Proper async context managers for resources
- AsyncIO-compatible libraries (httpx, aiofiles where applicable)

### Layered Architecture

**Decision**: Strict separation between infrastructure, core services, and application layers
**Rationale**:
- Clear separation of concerns improves maintainability
- Dependency inversion enables better testing and mocking
- Modular design supports future architectural evolution

**Implementation**:
- Infrastructure layer handles system concerns (config, logging, health)
- Core services implement business logic without infrastructure knowledge
- Clear interfaces between layers

### Version-Based Caching

**Decision**: Use immutable cache keys based on package name and version
**Rationale**:
- Package versions are immutable - documentation won't change for a given version
- Eliminates cache invalidation complexity
- Optimal performance for repeated requests

**Implementation**:
- Cache keys: `{package_name}-{version}.json`
- No time-based expiration
- Automatic cache validation and corruption recovery

### Circuit Breaker Pattern

**Decision**: Implement circuit breakers for external API calls
**Rationale**:
- Prevents cascading failures when PyPI or other services are unavailable
- Improves system resilience and user experience
- Enables graceful degradation

**Implementation**:
- Configurable failure thresholds
- Exponential backoff with jitter
- Automatic circuit recovery

## Performance Considerations

### Concurrent Processing
- Parallel dependency fetching with configurable limits
- Connection pooling with automatic cleanup
- Request queuing and rate limiting

### Memory Management
- Streaming JSON processing for large responses
- Bounded cache sizes with LRU eviction
- Efficient string handling and memory cleanup

### Resource Limits
- Configurable timeouts for all external requests
- Maximum context size limits for AI compatibility
- Connection pool size management

## Security Architecture

### Input Validation
- All user inputs validated and sanitized
- Path traversal prevention for cache operations
- URL validation for external requests

### Resource Protection
- Rate limiting for external API calls
- Memory usage monitoring and limits
- Secure temporary file handling

### Error Information Security
- Sanitized error messages to prevent information disclosure
- Secure logging practices (no sensitive data in logs)
- Controlled error context in responses

## Evolution and Extensibility

### Plugin Architecture Readiness
The current architecture supports future plugin-based extensions:
- Clear service interfaces suitable for plugin implementation
- Configuration system designed for plugin parameters
- Event system foundation for plugin lifecycle management

### Service Container Pattern
The infrastructure supports evolution toward a service container:
- Dependency injection patterns already established
- Service lifecycle management in place
- Configuration-driven service instantiation

### Microservice Decomposition
The layered architecture supports future microservice extraction:
- Clear service boundaries
- Network-aware interfaces
- Independent service configuration

This architectural foundation provides a solid base for current requirements while enabling future evolution and scaling needs.
