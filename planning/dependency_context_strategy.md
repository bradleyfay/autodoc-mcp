# Dependency Context Strategy

## Goal: Rich AI Context with Performance Balance

Provide comprehensive documentation context by including both the requested package and its key dependencies, giving AI assistants the full picture needed for accurate suggestions.

## Context Architecture

### 1. Layered Documentation Context

```python
class DocumentationContext(BaseModel):
    """Complete documentation context for AI consumption"""
    
    # Primary package (the one explicitly requested)
    primary_package: PackageDocumentation
    
    # Direct dependencies (runtime dependencies) 
    runtime_dependencies: List[PackageDocumentation] = Field(default_factory=list)
    
    # Development dependencies (if relevant to query)
    dev_dependencies: List[PackageDocumentation] = Field(default_factory=list)
    
    # Context metadata
    context_scope: str  # "primary_only", "with_runtime", "with_dev"
    total_packages: int
    truncated_packages: List[str] = Field(default_factory=list)  # Packages skipped due to limits
    
    @property
    def token_estimate(self) -> int:
        """Rough token count estimate for context window management"""
        return sum(doc.token_estimate for doc in self.all_packages)
    
    @property 
    def all_packages(self) -> List[PackageDocumentation]:
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
        return len(content.split()) * 1.3  # Rough tokens per word
```

### 2. Dependency Resolution Strategy

#### Phase 1: Identify Dependencies
```python
class DependencyResolver:
    """Resolve package dependencies with intelligent scoping"""
    
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
        
        # Get dependency metadata from PyPI
        deps_metadata = await self._get_dependency_metadata(package_name, version)
        
        # Score dependencies by relevance
        scored_deps = []
        for dep in deps_metadata.runtime_requires:
            score = self._calculate_dependency_relevance(dep, package_name)
            scored_deps.append((score, dep))
        
        # Sort by relevance and apply limits
        scored_deps.sort(reverse=True)  # Highest score first
        
        selected_deps = []
        estimated_tokens = 0
        
        for score, dep in scored_deps:
            if len(selected_deps) >= max_dependencies:
                break
            
            # Rough token estimate for this dependency
            dep_tokens = await self._estimate_dependency_tokens(dep.name)
            if estimated_tokens + dep_tokens > max_tokens:
                break
                
            selected_deps.append(dep.name)
            estimated_tokens += dep_tokens
        
        return selected_deps
    
    def _calculate_dependency_relevance(self, dep: DependencySpec, primary_package: str) -> float:
        """Score dependency relevance for context inclusion"""
        score = 0.0
        
        # Core framework dependencies get high priority
        if dep.name in CORE_FRAMEWORKS:  # requests, httpx, pydantic, etc.
            score += 10.0
        
        # Common utility libraries
        if dep.name in COMMON_UTILITIES:  # click, typer, rich, etc.
            score += 5.0
        
        # Package-specific boost for known important relationships
        package_boosts = {
            "fastapi": {"pydantic": 8.0, "starlette": 8.0, "uvicorn": 6.0},
            "django": {"django-rest-framework": 7.0, "psycopg2": 6.0},
            "flask": {"jinja2": 7.0, "werkzeug": 7.0},
            "requests": {"urllib3": 8.0, "certifi": 6.0}
        }
        
        if primary_package in package_boosts:
            score += package_boosts[primary_package].get(dep.name, 0.0)
        
        # Penalty for very low-level or build dependencies
        if dep.name in LOW_PRIORITY_DEPS:  # setuptools, wheel, etc.
            score -= 5.0
        
        # Boost for packages with good documentation
        if dep.name in WELL_DOCUMENTED:  # pandas, numpy, requests, etc.
            score += 2.0
            
        return max(0.0, score)  # Don't go negative

# Pre-defined package categories
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
```

#### Phase 2: Fetch and Format Context
```python
@mcp.tool
async def get_package_docs_with_context(
    package_name: str, 
    version_constraint: Optional[str] = None,
    include_dependencies: bool = True,
    context_scope: str = "smart"  # "primary_only", "runtime", "smart"
) -> Dict[str, Any]:
    """
    Fetch comprehensive documentation context
    
    Args:
        package_name: Primary package to document
        version_constraint: Version constraint from dependency scanning  
        include_dependencies: Whether to include dependency context
        context_scope: How much context to include
    """
    
    # Step 1: Get primary package documentation
    primary_info, from_cache = await cache_manager.resolve_and_cache(
        package_name, version_constraint
    )
    
    primary_docs = await _format_primary_documentation(primary_info)
    
    context = DocumentationContext(
        primary_package=primary_docs,
        context_scope="primary_only"
    )
    
    if not include_dependencies:
        return _format_context_response(context)
    
    # Step 2: Resolve relevant dependencies 
    try:
        dependency_names = await dependency_resolver.resolve_context_dependencies(
            package_name=primary_info.name,
            version=primary_info.version,
            max_dependencies=8 if context_scope == "smart" else 5
        )
        
        # Step 3: Fetch dependency documentation concurrently
        dependency_tasks = []
        for dep_name in dependency_names:
            task = _fetch_dependency_documentation(dep_name, primary_info.name)
            dependency_tasks.append(task)
        
        # Wait for all dependency fetches (with timeout)
        dependency_results = await asyncio.gather(
            *dependency_tasks, 
            return_exceptions=True,
            timeout=15.0  # Don't wait too long for dependencies
        )
        
        # Step 4: Process results with graceful degradation
        successful_deps = []
        failed_deps = []
        
        for i, result in enumerate(dependency_results):
            if isinstance(result, Exception):
                failed_deps.append({
                    "package": dependency_names[i],
                    "error": str(result)
                })
            else:
                successful_deps.append(result)
        
        context.runtime_dependencies = successful_deps
        context.context_scope = f"with_runtime ({len(successful_deps)} deps)"
        context.total_packages = 1 + len(successful_deps)
        
        if failed_deps:
            context.truncated_packages = [f["package"] for f in failed_deps]
        
    except Exception as e:
        # If dependency resolution fails, still return primary package docs
        logger.warning("Dependency context failed", error=str(e))
        context.context_scope = "primary_only (deps_failed)"
    
    return _format_context_response(context)

async def _fetch_dependency_documentation(dep_name: str, primary_package: str) -> PackageDocumentation:
    """Fetch concise documentation for a dependency"""
    
    try:
        dep_info, _ = await cache_manager.resolve_and_cache(dep_name)
        
        # Create concise documentation focused on key information
        return PackageDocumentation(
            name=dep_info.name,
            version=dep_info.version, 
            relationship="runtime_dependency",
            why_included=f"Required by {primary_package}",
            dependency_level=1,
            summary=dep_info.summary,
            key_features=_extract_key_features(dep_info.description),
            main_classes=_extract_main_classes(dep_info), 
            main_functions=_extract_main_functions(dep_info),
            usage_examples=_extract_concise_examples(dep_info.description)
        )
        
    except Exception as e:
        # Return minimal documentation for failed fetches
        return PackageDocumentation(
            name=dep_name,
            version="unknown",
            relationship="runtime_dependency", 
            why_included=f"Required by {primary_package} (fetch failed)",
            dependency_level=1,
            summary=f"Documentation fetch failed: {e}"
        )
```

### 3. Context Response Format

```json
{
    "success": true,
    "context": {
        "primary_package": {
            "name": "fastapi",
            "version": "0.104.1",
            "relationship": "primary",
            "summary": "FastAPI framework, high performance, easy to learn...",
            "key_features": ["Automatic API documentation", "Type hints", "Async support"],
            "main_classes": ["FastAPI", "APIRouter", "Depends"],
            "usage_examples": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/')\ndef read_root()..."
        },
        "runtime_dependencies": [
            {
                "name": "pydantic", 
                "version": "2.5.1",
                "relationship": "runtime_dependency",
                "why_included": "Required by fastapi",
                "summary": "Data validation using Python type hints",
                "key_features": ["Data validation", "Serialization", "Type safety"],
                "main_classes": ["BaseModel", "Field", "validator"],
                "usage_examples": "from pydantic import BaseModel\nclass User(BaseModel)..."
            },
            {
                "name": "starlette",
                "version": "0.27.0", 
                "relationship": "runtime_dependency",
                "why_included": "Required by fastapi",
                "summary": "Lightweight ASGI framework/toolkit",
                "key_features": ["ASGI support", "WebSocket support", "Middleware"],
                "main_classes": ["Request", "Response", "WebSocket"]
            }
        ],
        "context_scope": "with_runtime (2 deps)",
        "total_packages": 3,
        "token_estimate": 15420
    },
    "performance": {
        "primary_fetch_time": 0.12,
        "dependency_fetch_time": 0.89,
        "cache_hits": 1,
        "cache_misses": 2
    }
}
```

## Performance Optimizations

1. **Concurrent Fetching**: Fetch all dependencies in parallel
2. **Smart Caching**: Version-based caching for all packages
3. **Token Management**: Respect context window limits
4. **Timeout Protection**: Don't wait indefinitely for slow dependencies
5. **Relevance Scoring**: Prioritize most important dependencies

## Context Window Management

```python
class ContextWindowManager:
    """Manage AI context window efficiently"""
    
    @staticmethod
    def fit_to_window(context: DocumentationContext, max_tokens: int = 30000) -> DocumentationContext:
        """Trim context to fit within token limits"""
        
        if context.token_estimate <= max_tokens:
            return context
        
        # Start by truncating dependency documentation
        truncated_deps = []
        remaining_tokens = max_tokens - context.primary_package.token_estimate
        
        for dep in context.runtime_dependencies:
            if remaining_tokens >= dep.token_estimate:
                truncated_deps.append(dep)
                remaining_tokens -= dep.token_estimate
            else:
                context.truncated_packages.append(dep.name)
        
        context.runtime_dependencies = truncated_deps
        return context
```

This strategy provides rich, contextual documentation while maintaining good performance and respecting token limits. The AI assistant will have comprehensive information about the primary package plus its key dependencies, enabling much more accurate and helpful suggestions.