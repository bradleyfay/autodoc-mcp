#!/usr/bin/env python3
"""Development utilities for AutoDocs MCP Server."""

import asyncio
import json
from pathlib import Path

import click

from autodocs_mcp.config import get_config
from autodocs_mcp.core.cache_manager import FileCacheManager
from autodocs_mcp.core.dependency_parser import PyProjectParser
from autodocs_mcp.core.doc_fetcher import PyPIDocumentationFetcher
from autodocs_mcp.core.version_resolver import VersionResolver


@click.group()
def cli():
    """Development tools for AutoDocs MCP."""
    pass


@cli.command()
@click.option('--project-path', type=click.Path(exists=True), default='.')
def test_scan(project_path):
    """Test dependency scanning locally."""
    async def run_test():
        parser = PyProjectParser()
        project_dir = Path(project_path)
        
        try:
            result = await parser.parse_project(project_dir)
            
            # Convert to MCP tool response format
            mcp_result = {
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
            
            click.echo(json.dumps(mcp_result, indent=2, default=str))
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": {
                    "type": type(e).__name__,
                    "message": str(e)
                }
            }
            click.echo(json.dumps(error_result, indent=2, default=str))
    
    asyncio.run(run_test())


@cli.command()
@click.option('--project-path', type=click.Path(exists=True), default='.')
def validate_project(project_path):
    """Validate that a project can be scanned."""
    from autodocs_mcp.core.dependency_parser import PyProjectParser
    
    parser = PyProjectParser()
    project_dir = Path(project_path)
    pyproject_file = project_dir / "pyproject.toml"
    
    if not pyproject_file.exists():
        click.echo(f"❌ No pyproject.toml found in {project_dir}")
        return
    
    is_valid = parser.validate_file(pyproject_file)
    if is_valid:
        click.echo(f"✅ Valid pyproject.toml found in {project_dir}")
    else:
        click.echo(f"⚠️  pyproject.toml exists but appears invalid in {project_dir}")


@cli.command()
@click.argument('package_name')
@click.option('--version-constraint', help='Version constraint like ">=2.0.0"')
@click.option('--query', help='Filter query for documentation')
def test_docs(package_name, version_constraint, query):
    """Test documentation fetching locally."""
    async def run_test():
        config = get_config()
        cache_manager = FileCacheManager(config.cache_dir)
        version_resolver = VersionResolver()
        
        await cache_manager.initialize()
        
        try:
            click.echo(f"🔍 Resolving version for {package_name}...")
            resolved_version = await version_resolver.resolve_version(package_name, version_constraint)
            cache_key = version_resolver.generate_cache_key(package_name, resolved_version)
            
            click.echo(f"📦 Resolved: {package_name} -> v{resolved_version}")
            click.echo(f"🔑 Cache key: {cache_key}")
            
            # Check cache first
            cached_entry = await cache_manager.get(cache_key)
            if cached_entry:
                click.echo("✅ Found in cache!")
                package_info = cached_entry.data
                from_cache = True
            else:
                click.echo("🌐 Fetching from PyPI...")
                async with PyPIDocumentationFetcher() as fetcher:
                    package_info = await fetcher.fetch_package_info(package_name)
                    await cache_manager.set(cache_key, package_info)
                from_cache = False
            
            # Format documentation
            async with PyPIDocumentationFetcher() as fetcher:
                docs = fetcher.format_documentation(package_info, query)
            
            result = {
                "success": True,
                "package_name": package_info.name,
                "version": package_info.version,
                "resolved_version": resolved_version,
                "version_constraint": version_constraint,
                "from_cache": from_cache,
                "cache_key": cache_key,
                "documentation": docs
            }
            
            click.echo(json.dumps(result, indent=2, default=str))
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": {
                    "type": type(e).__name__,
                    "message": str(e)
                }
            }
            click.echo(json.dumps(error_result, indent=2, default=str))
    
    asyncio.run(run_test())


@cli.command()
def cache_stats():
    """Show cache statistics."""
    async def run_test():
        config = get_config()
        cache_manager = FileCacheManager(config.cache_dir)
        await cache_manager.initialize()
        
        stats = await cache_manager.get_cache_stats()
        packages = await cache_manager.list_cached_packages()
        
        result = {
            "cache_stats": stats,
            "cached_packages": packages,
            "total_packages": len(packages)
        }
        
        click.echo(json.dumps(result, indent=2, default=str))
    
    asyncio.run(run_test())


@cli.command()
def clear_cache():
    """Clear the documentation cache."""
    async def run_test():
        config = get_config()
        cache_manager = FileCacheManager(config.cache_dir)
        await cache_manager.initialize()
        
        initial_stats = await cache_manager.get_cache_stats()
        await cache_manager.invalidate()
        final_stats = await cache_manager.get_cache_stats()
        
        click.echo(f"✅ Cleared {initial_stats.get('total_entries', 0)} cache entries")
        click.echo(f"💾 Freed {initial_stats.get('total_size_bytes', 0)} bytes")
    
    asyncio.run(run_test())


if __name__ == '__main__':
    cli()