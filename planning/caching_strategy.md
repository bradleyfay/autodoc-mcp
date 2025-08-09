# Version-Based Caching Strategy

## Core Concept
Cache documentation based on **resolved package versions** rather than time, ensuring we always have docs that match the actual package version while minimizing unnecessary API calls.

## Cache Key Strategy

### Cache Key Format
```
{package_name}-{resolved_version}.json
```

Examples:
- `requests-2.28.2.json`
- `pydantic-2.5.1.json`
- `fastapi-0.104.1.json`

### Version Resolution Process

1. **Dependency Scanning**: Extract version constraints from pyproject.toml
   - Input: `requests>=2.25.0,<3.0.0`
   - Store: Constraint specification

2. **Documentation Fetching**: Resolve to actual version
   - Query PyPI API: `https://pypi.org/pypi/requests/json`
   - Extract `info.version` (latest version)
   - Validate against constraint: `2.28.2 satisfies >=2.25.0,<3.0.0`
   - Cache key: `requests-2.28.2.json`

3. **Cache Lookup**: Check for exact version match
   - Look for `requests-2.28.2.json`
   - If found: Return cached docs
   - If not found: Fetch from PyPI and cache

## Implementation Details

### Enhanced Cache Manager Interface
```python
from typing import Optional, Tuple
from packaging import version
from packaging.specifiers import SpecifierSet

class VersionAwareCacheManager(CacheManagerInterface):

    async def get_for_version(self, package_name: str, version_constraint: Optional[str] = None) -> Optional[CacheEntry]:
        """
        Get cached entry for specific version constraint

        Args:
            package_name: Package name
            version_constraint: Version constraint like ">=2.0.0,<3.0.0" or None for latest

        Returns:
            CacheEntry if exact version match exists, None otherwise
        """

    async def resolve_and_cache(self, package_name: str, version_constraint: Optional[str] = None) -> Tuple[PackageInfo, bool]:
        """
        Resolve version and return cached or freshly fetched package info

        Args:
            package_name: Package name
            version_constraint: Version constraint or None for latest

        Returns:
            Tuple of (PackageInfo, was_cached: bool)
        """

    async def list_cached_versions(self, package_name: str) -> List[str]:
        """List all cached versions for a package"""

    async def cleanup_old_versions(self, package_name: str, keep_latest: int = 3) -> int:
        """Remove old cached versions, keeping N most recent"""
```

### Version Resolution Logic
```python
class VersionResolver:

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
        # Fetch package metadata from PyPI
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://pypi.org/pypi/{package_name}/json")
            data = response.json()

        latest_version = data["info"]["version"]

        if constraint is None:
            return latest_version

        # Parse and validate constraint
        specifier = SpecifierSet(constraint)

        if latest_version in specifier:
            return latest_version

        # Fallback: find highest version that matches constraint
        # This would require fetching all versions - for MVP, we'll use latest if it matches
        # or raise an error if it doesn't

        raise ValueError(f"Latest version {latest_version} doesn't satisfy constraint {constraint}")

    @staticmethod
    def generate_cache_key(package_name: str, version: str) -> str:
        """Generate cache key for specific version"""
        return f"{package_name}-{version}"
```

### Updated Get Package Docs Flow
```python
@mcp.tool
async def get_package_docs(package_name: str, version_constraint: Optional[str] = None, query: Optional[str] = None) -> Dict[str, Any]:
    """
    Args:
        package_name: Package name
        version_constraint: Optional version constraint from dependency scanning
        query: Optional query filter
    """
    try:
        # Resolve to specific version
        resolved_version = await VersionResolver.resolve_version(package_name, version_constraint)

        # Check version-specific cache
        cache_key = VersionResolver.generate_cache_key(package_name, resolved_version)
        cached_entry = await cache_manager.get(cache_key)

        if cached_entry:
            logger.info("Version-specific cache hit",
                       package=package_name,
                       version=resolved_version,
                       constraint=version_constraint)
            package_info = cached_entry.data
            from_cache = True
        else:
            logger.info("Fetching fresh package info",
                       package=package_name,
                       version=resolved_version)

            async with PyPIDocumentationFetcher() as fetcher:
                package_info = await fetcher.fetch_package_info(package_name)

                # Verify version matches what we resolved
                if package_info.version != resolved_version:
                    logger.warning("Version mismatch",
                                  expected=resolved_version,
                                  actual=package_info.version)

                await cache_manager.set(cache_key, package_info)
            from_cache = False

        # Format documentation
        async with PyPIDocumentationFetcher() as fetcher:
            formatted_docs = fetcher.format_documentation(package_info, query)

        return {
            "success": True,
            "package_name": package_info.name,
            "version": package_info.version,
            "resolved_version": resolved_version,
            "version_constraint": version_constraint,
            "documentation": formatted_docs,
            "from_cache": from_cache,
            "query_applied": query is not None
        }

    except Exception as e:
        # ... error handling
```

## Cache Management Benefits

1. **Accuracy**: Always have docs matching actual package version
2. **Efficiency**: Only fetch when version actually changes
3. **Storage**: Reasonable disk usage (docs don't change often)
4. **Performance**: Instant cache hits for repeated version requests

## Cache Cleanup Strategy

```python
# Periodic cleanup to prevent unlimited cache growth
async def periodic_cleanup():
    """Clean up old cached versions periodically"""

    # Keep 3 most recent versions per package
    for package_dir in cache_dir.iterdir():
        if package_dir.is_dir():
            await cache_manager.cleanup_old_versions(package_dir.name, keep_latest=3)

    # Remove packages not accessed in 90 days
    cutoff = datetime.now() - timedelta(days=90)
    await cache_manager.cleanup_unused_packages(cutoff)
```

## Migration from Time-Based Cache

```python
async def migrate_legacy_cache():
    """Migrate existing time-based cache to version-based"""

    for cache_file in cache_dir.glob("*.json"):
        if "-" not in cache_file.stem:  # Legacy format: package_name.json
            legacy_data = json.loads(cache_file.read_text())
            package_name = cache_file.stem
            version = legacy_data["version"]

            # Rename to version-based format
            new_name = f"{package_name}-{version}.json"
            cache_file.rename(cache_dir / new_name)
```

This approach ensures we have accurate, version-specific documentation while being much more efficient than time-based expiration.
