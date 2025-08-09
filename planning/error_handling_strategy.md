# Error Handling Strategy: Graceful Degradation

## Philosophy: Maximize Useful Context

For the AutoDocs MCP MVP, we prioritize **providing maximum useful context** over strict validation. Real-world Python projects often have edge cases, malformed dependencies, or temporary network issues that shouldn't prevent the tool from being helpful.

## Graceful Degradation Approach

### Core Principle
**Collect and return as much valid information as possible, while clearly documenting what failed and why.**

### Implementation Strategy

#### 1. Dependency Scanning with Partial Success
```python
class ScanResult(BaseModel):
    """Enhanced result model supporting partial success"""
    project_path: Path
    dependencies: List[DependencySpec]
    project_name: Optional[str] = None
    scan_timestamp: datetime

    # Graceful degradation fields
    successful_deps: int = 0
    failed_deps: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    partial_success: bool = False

async def parse_project(self, project_path: Path) -> ScanResult:
    """Parse with graceful degradation"""
    dependencies = []
    failed_deps = []
    warnings = []

    try:
        # Main parsing logic
        for dep_str in dependency_strings:
            try:
                spec = self._parse_dependency_string(dep_str, source)
                dependencies.append(spec)
            except ValueError as e:
                failed_deps.append({
                    "dependency_string": dep_str,
                    "error": str(e),
                    "source": source
                })
                warnings.append(f"Skipped malformed dependency: {dep_str}")
                continue  # Keep processing other deps

    except Exception as e:
        # Even if parsing fails, return what we have
        warnings.append(f"Partial parsing failure: {e}")

    return ScanResult(
        project_path=project_path,
        dependencies=dependencies,
        successful_deps=len(dependencies),
        failed_deps=failed_deps,
        warnings=warnings,
        partial_success=len(failed_deps) > 0 or len(warnings) > 0,
        scan_timestamp=datetime.now()
    )
```

#### 2. Documentation Fetching with Fallbacks
```python
@mcp.tool
async def get_package_docs(package_name: str, version_constraint: Optional[str] = None, include_dependencies: bool = True) -> Dict[str, Any]:
    """Fetch docs with graceful handling of failures"""

    main_package_info = None
    dependency_docs = []
    errors = []
    warnings = []

    try:
        # Primary package documentation
        main_package_info, from_cache = await cache_manager.resolve_and_cache(
            package_name, version_constraint
        )

        # Fetch dependency documentation if requested
        if include_dependencies and main_package_info:
            dependency_docs, dep_errors = await self._fetch_dependency_docs(
                package_name, main_package_info.version
            )
            errors.extend(dep_errors)

    except PackageNotFoundError:
        errors.append({
            "type": "PackageNotFoundError",
            "package": package_name,
            "message": f"Package '{package_name}' not found on PyPI",
            "suggestions": await self._suggest_similar_packages(package_name)
        })

    except NetworkError as e:
        errors.append({
            "type": "NetworkError",
            "package": package_name,
            "message": str(e),
            "retry_suggested": True
        })

    # Return partial results even with errors
    return {
        "success": main_package_info is not None,
        "partial_success": len(errors) > 0 or len(warnings) > 0,

        # Main package info (may be None if failed)
        "package_name": main_package_info.name if main_package_info else package_name,
        "version": main_package_info.version if main_package_info else None,
        "documentation": formatted_docs if main_package_info else None,

        # Dependency documentation (best effort)
        "dependencies": dependency_docs,
        "dependency_count": len(dependency_docs),

        # Error/warning information
        "errors": errors,
        "warnings": warnings,
        "from_cache": from_cache if main_package_info else False
    }

async def _fetch_dependency_docs(self, package_name: str, version: str) -> Tuple[List[Dict], List[Dict]]:
    """Fetch dependency docs with error collection"""
    dependency_docs = []
    errors = []

    try:
        # Get package dependencies from PyPI metadata
        deps = await self._get_package_dependencies(package_name, version)

        # Limit to top 5 direct dependencies to avoid explosion
        for dep_name in deps[:5]:
            try:
                dep_info, _ = await cache_manager.resolve_and_cache(dep_name)

                async with PyPIDocumentationFetcher() as fetcher:
                    formatted = fetcher.format_documentation(dep_info, truncate=True)

                dependency_docs.append({
                    "name": dep_info.name,
                    "version": dep_info.version,
                    "documentation": formatted,
                    "relationship": "dependency"
                })

            except Exception as e:
                errors.append({
                    "type": type(e).__name__,
                    "package": dep_name,
                    "message": f"Failed to fetch dependency docs: {e}"
                })
                continue  # Keep trying other dependencies

    except Exception as e:
        errors.append({
            "type": type(e).__name__,
            "message": f"Failed to resolve dependencies for {package_name}: {e}"
        })

    return dependency_docs, errors
```

#### 3. User-Friendly Error Messages
```python
class ErrorResponseFormatter:
    """Format errors for user consumption"""

    @staticmethod
    def format_parsing_errors(failed_deps: List[Dict]) -> List[str]:
        """Convert parsing errors to helpful messages"""
        suggestions = []

        for failure in failed_deps:
            dep_str = failure["dependency_string"]
            error = failure["error"]

            if "version" in error.lower():
                suggestions.append(
                    f"'{dep_str}' has an invalid version specifier. "
                    f"Try formats like: {dep_str.split()[0]}>=1.0.0"
                )
            elif "bracket" in error.lower():
                suggestions.append(
                    f"'{dep_str}' has malformed extras. "
                    f"Use square brackets like: {dep_str.split()[0]}[extra1,extra2]"
                )
            else:
                suggestions.append(
                    f"'{dep_str}' couldn't be parsed. Check the dependency format."
                )

        return suggestions

    @staticmethod
    def format_network_errors(errors: List[Dict]) -> List[str]:
        """Convert network errors to actionable messages"""
        suggestions = []

        for error in errors:
            if error["type"] == "PackageNotFoundError":
                msg = f"Package '{error['package']}' not found."
                if "suggestions" in error:
                    msg += f" Did you mean: {', '.join(error['suggestions'])}"
                suggestions.append(msg)

            elif error["type"] == "NetworkError":
                suggestions.append(
                    f"Network issue fetching '{error['package']}'. "
                    f"Check internet connection and try again."
                )

        return suggestions
```

## Benefits of Graceful Degradation

1. **Real-World Usability**: Works with imperfect project configurations
2. **Partial Value**: Users get help for packages that do work
3. **Clear Feedback**: Users understand exactly what failed and why
4. **Development Friendly**: Doesn't break workflows due to single dependency issues
5. **Debugging Support**: Detailed error information helps users fix issues

## When to Fail Fast

Reserve fail-fast behavior for:
- **Critical Configuration Issues**: Missing pyproject.toml entirely
- **Security Concerns**: Path traversal attempts, suspicious file access
- **System Resource Issues**: Out of disk space, permission denied
- **Invalid MCP Parameters**: Malformed tool inputs

## Example Response with Graceful Degradation

```json
{
    "success": true,
    "partial_success": true,
    "package_name": "fastapi",
    "version": "0.104.1",
    "documentation": "# FastAPI Documentation...",
    "dependencies": [
        {
            "name": "pydantic",
            "version": "2.5.1",
            "documentation": "# Pydantic Documentation...",
            "relationship": "dependency"
        },
        {
            "name": "starlette",
            "version": "0.27.0",
            "documentation": "# Starlette Documentation...",
            "relationship": "dependency"
        }
    ],
    "dependency_count": 2,
    "warnings": [
        "Skipped malformed dependency: 'invalid-package-name=='",
        "Limited to 5 dependencies for performance"
    ],
    "errors": [
        {
            "type": "PackageNotFoundError",
            "package": "nonexistent-package",
            "message": "Package 'nonexistent-package' not found on PyPI",
            "suggestions": ["nonexistent", "non-existent-pkg"]
        }
    ],
    "suggestions": [
        "'invalid-package-name==' has an invalid version specifier. Try formats like: invalid-package-name>=1.0.0",
        "Package 'nonexistent-package' not found. Did you mean: nonexistent, non-existent-pkg"
    ]
}
```

This approach maximizes the tool's utility while providing clear guidance for resolving issues.
