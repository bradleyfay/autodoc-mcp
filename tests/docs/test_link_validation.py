"""
Automated link validation test suite for the AutoDocs documentation site.

This module provides comprehensive link validation testing including:
- Internal link validation
- External link validation with retries
- Navigation structure testing
- Asset link validation
- Cross-reference validation

Uses pytest ecosystem with proper error handling and parallel execution support.
"""

import asyncio
import re
from pathlib import Path
from urllib.parse import urlparse

import httpx
import pytest
from bs4 import BeautifulSoup


class LinkValidationError(Exception):
    """Custom exception for link validation failures."""

    pass


class LinkValidator:
    """
    Comprehensive link validation for documentation sites.

    Features:
    - Internal link validation against actual file system
    - External link validation with retry logic
    - Asset validation (images, CSS, JS)
    - Fragment identifier validation
    - Parallel processing for performance
    """

    def __init__(self, site_dir: Path, base_url: str = "https://localhost"):
        self.site_dir = site_dir
        self.base_url = base_url
        self.internal_links: dict[str, set[str]] = {}
        self.external_links: dict[str, set[str]] = {}
        self.asset_links: dict[str, set[str]] = {}
        self.broken_links: list[dict[str, str]] = []

    async def validate_all_links(self) -> dict[str, list]:
        """
        Run comprehensive link validation on the entire site.

        Returns:
            Dictionary with validation results categorized by type
        """
        html_files = list(self.site_dir.glob("**/*.html"))

        # Parse all HTML files and extract links
        for html_file in html_files:
            await self._parse_html_file(html_file)

        # Validate different types of links
        internal_results = await self._validate_internal_links()
        external_results = await self._validate_external_links()
        asset_results = await self._validate_asset_links()

        return {
            "internal_validation": internal_results,
            "external_validation": external_results,
            "asset_validation": asset_results,
            "summary": {
                "total_files_processed": len(html_files),
                "internal_links_found": sum(
                    len(links) for links in self.internal_links.values()
                ),
                "external_links_found": sum(
                    len(links) for links in self.external_links.values()
                ),
                "asset_links_found": sum(
                    len(links) for links in self.asset_links.values()
                ),
                "broken_links_total": len(self.broken_links),
            },
        }

    async def _parse_html_file(self, html_file: Path) -> None:
        """Parse HTML file and extract all links."""
        try:
            content = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(content, "html.parser")

            relative_path = html_file.relative_to(self.site_dir)
            page_key = str(relative_path)

            # Initialize link sets for this page
            self.internal_links[page_key] = set()
            self.external_links[page_key] = set()
            self.asset_links[page_key] = set()

            # Extract different types of links
            self._extract_href_links(soup, page_key)
            self._extract_src_links(soup, page_key)
            self._extract_css_links(soup, page_key)

        except Exception as e:
            self.broken_links.append(
                {
                    "file": str(html_file),
                    "error": f"Failed to parse HTML: {str(e)}",
                    "type": "parse_error",
                }
            )

    def _extract_href_links(self, soup: BeautifulSoup, page_key: str) -> None:
        """Extract all href links from HTML."""
        for element in soup.find_all(["a", "link"], href=True):
            href = element["href"].strip()
            if not href:
                continue

            if self._is_external_link(href):
                self.external_links[page_key].add(href)
            elif href.startswith("#"):
                # Fragment-only links are internal to the page
                self.internal_links[page_key].add(f"{page_key}{href}")
            else:
                # Internal link
                self.internal_links[page_key].add(href)

    def _extract_src_links(self, soup: BeautifulSoup, page_key: str) -> None:
        """Extract all src links from HTML (images, scripts, etc.)."""
        for element in soup.find_all(["img", "script", "iframe", "embed"], src=True):
            src = element["src"].strip()
            if not src:
                continue

            if self._is_external_link(src):
                self.external_links[page_key].add(src)
            else:
                self.asset_links[page_key].add(src)

    def _extract_css_links(self, soup: BeautifulSoup, page_key: str) -> None:
        """Extract CSS links and analyze for additional resources."""
        for element in soup.find_all("link", rel="stylesheet"):
            href = element.get("href", "").strip()
            if href and not self._is_external_link(href):
                self.asset_links[page_key].add(href)

    def _is_external_link(self, url: str) -> bool:
        """Check if a URL is external."""
        parsed = urlparse(url)
        return bool(parsed.netloc) and not url.startswith(self.base_url)

    async def _validate_internal_links(self) -> list[dict[str, str]]:
        """Validate all internal links against the file system."""
        validation_results = []

        for page_key, links in self.internal_links.items():
            for link in links:
                result = await self._validate_single_internal_link(page_key, link)
                if result:
                    validation_results.append(result)

        return validation_results

    async def _validate_single_internal_link(
        self, page_key: str, link: str
    ) -> dict[str, str] | None:
        """Validate a single internal link."""
        try:
            # Handle fragment identifiers
            if "#" in link:
                file_part, fragment = link.split("#", 1)
                if not file_part:
                    # Fragment-only link - validate fragment exists in current page
                    return await self._validate_fragment(page_key, fragment)
            else:
                file_part = link
                fragment = None

            # Resolve relative paths
            if file_part.startswith("./") or not file_part.startswith("/"):
                base_dir = (self.site_dir / page_key).parent
                target_path = (base_dir / file_part).resolve()
            else:
                target_path = (self.site_dir / file_part.lstrip("/")).resolve()

            # Check if target exists
            if not target_path.exists():
                # Try common variations
                variations = [
                    target_path.with_suffix(".html"),
                    target_path / "index.html",
                ]

                found = False
                for variation in variations:
                    if variation.exists():
                        target_path = variation
                        found = True
                        break

                if not found:
                    return {
                        "source_file": page_key,
                        "target_link": link,
                        "error": f"Target file not found: {target_path}",
                        "type": "broken_internal_link",
                    }

            # Validate fragment if present
            if fragment:
                fragment_result = await self._validate_fragment(
                    str(target_path), fragment
                )
                if fragment_result:
                    return fragment_result

        except Exception as e:
            return {
                "source_file": page_key,
                "target_link": link,
                "error": f"Validation error: {str(e)}",
                "type": "validation_error",
            }

        return None

    async def _validate_fragment(
        self, file_path: str, fragment: str
    ) -> dict[str, str] | None:
        """Validate that a fragment identifier exists in the target file."""
        try:
            if file_path.startswith("site/"):
                target_file = self.site_dir / file_path.replace("site/", "")
            else:
                target_file = self.site_dir / file_path

            if not target_file.exists():
                return {
                    "source_file": file_path,
                    "target_link": f"#{fragment}",
                    "error": f"Target file for fragment validation not found: {target_file}",
                    "type": "fragment_validation_error",
                }

            content = target_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(content, "html.parser")

            # Look for element with matching id
            target_element = soup.find(id=fragment)
            if not target_element:
                # Also check for heading elements that might generate IDs
                headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
                heading_ids = [
                    self._generate_heading_id(h.get_text()) for h in headings
                ]
                if fragment not in heading_ids:
                    return {
                        "source_file": file_path,
                        "target_link": f"#{fragment}",
                        "error": f"Fragment '{fragment}' not found in target file",
                        "type": "missing_fragment",
                    }

        except Exception as e:
            return {
                "source_file": file_path,
                "target_link": f"#{fragment}",
                "error": f"Fragment validation error: {str(e)}",
                "type": "fragment_validation_error",
            }

        return None

    def _generate_heading_id(self, text: str) -> str:
        """Generate heading ID the way MkDocs does."""
        # Simplified version - real MkDocs ID generation is more complex
        return re.sub(r"[^\w\s-]", "", text.lower()).replace(" ", "-")

    async def _validate_external_links(self) -> list[dict[str, str]]:
        """Validate external links with retry logic."""
        validation_results = []
        unique_external_links = set()

        # Collect all unique external links
        for links in self.external_links.values():
            unique_external_links.update(links)

        # Validate each unique external link
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            tasks = [
                self._validate_single_external_link(client, link)
                for link in unique_external_links
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for link, result in zip(unique_external_links, results, strict=False):
                if isinstance(result, Exception):
                    validation_results.append(
                        {
                            "target_link": link,
                            "error": f"Validation exception: {str(result)}",
                            "type": "external_validation_exception",
                        }
                    )
                elif result:
                    validation_results.append(result)

        return validation_results

    async def _validate_single_external_link(
        self, client: httpx.AsyncClient, url: str
    ) -> dict[str, str] | None:
        """Validate a single external link with retries."""
        max_retries = 3
        retry_delay = 1.0

        for attempt in range(max_retries):
            try:
                response = await client.head(url, timeout=30.0)
                if response.status_code >= 400:
                    # Try GET request for servers that don't support HEAD
                    response = await client.get(url, timeout=30.0)

                if response.status_code >= 400:
                    return {
                        "target_link": url,
                        "error": f"HTTP {response.status_code}: {response.reason_phrase}",
                        "type": "external_link_error",
                    }

                # Success
                return None

            except httpx.TimeoutException:
                if attempt == max_retries - 1:
                    return {
                        "target_link": url,
                        "error": "Connection timeout",
                        "type": "external_link_timeout",
                    }
                await asyncio.sleep(retry_delay * (2**attempt))

            except httpx.RequestError as e:
                if attempt == max_retries - 1:
                    return {
                        "target_link": url,
                        "error": f"Request error: {str(e)}",
                        "type": "external_link_error",
                    }
                await asyncio.sleep(retry_delay * (2**attempt))

        return None

    async def _validate_asset_links(self) -> list[dict[str, str]]:
        """Validate asset links (CSS, JS, images, etc.)."""
        validation_results = []

        for page_key, links in self.asset_links.items():
            for link in links:
                result = await self._validate_single_asset_link(page_key, link)
                if result:
                    validation_results.append(result)

        return validation_results

    async def _validate_single_asset_link(
        self, page_key: str, link: str
    ) -> dict[str, str] | None:
        """Validate a single asset link."""
        try:
            # Resolve asset path
            if link.startswith("./") or not link.startswith("/"):
                base_dir = (self.site_dir / page_key).parent
                asset_path = (base_dir / link).resolve()
            else:
                asset_path = (self.site_dir / link.lstrip("/")).resolve()

            if not asset_path.exists():
                return {
                    "source_file": page_key,
                    "target_link": link,
                    "error": f"Asset file not found: {asset_path}",
                    "type": "missing_asset",
                }

        except Exception as e:
            return {
                "source_file": page_key,
                "target_link": link,
                "error": f"Asset validation error: {str(e)}",
                "type": "asset_validation_error",
            }

        return None


@pytest.fixture
def link_validator():
    """Pytest fixture for LinkValidator instance."""
    site_dir = Path(__file__).parent.parent.parent / "site"
    return LinkValidator(site_dir)


@pytest.mark.asyncio
async def test_internal_links_validation(link_validator):
    """Test that all internal links are valid."""
    results = await link_validator.validate_all_links()
    internal_issues = results["internal_validation"]

    if internal_issues:
        # Create detailed error message
        error_details = []
        for issue in internal_issues:
            error_details.append(
                f"  - {issue['source_file']}: {issue['target_link']} -> {issue['error']}"
            )

        pytest.fail(
            f"Found {len(internal_issues)} internal link issues:\n"
            + "\n".join(error_details)
        )


@pytest.mark.asyncio
async def test_asset_links_validation(link_validator):
    """Test that all asset links (CSS, JS, images) are valid."""
    results = await link_validator.validate_all_links()
    asset_issues = results["asset_validation"]

    if asset_issues:
        error_details = []
        for issue in asset_issues:
            error_details.append(
                f"  - {issue['source_file']}: {issue['target_link']} -> {issue['error']}"
            )

        pytest.fail(
            f"Found {len(asset_issues)} asset link issues:\n" + "\n".join(error_details)
        )


@pytest.mark.asyncio
async def test_external_links_validation(link_validator):
    """Test that critical external links are valid."""
    results = await link_validator.validate_all_links()
    external_issues = results["external_validation"]

    # Filter out non-critical external link issues (like social media, etc.)
    critical_issues = [
        issue
        for issue in external_issues
        if any(
            domain in issue["target_link"]
            for domain in ["github.com", "pypi.org", "python.org", "docs.python.org"]
        )
    ]

    if critical_issues:
        error_details = []
        for issue in critical_issues:
            error_details.append(f"  - {issue['target_link']}: {issue['error']}")

        pytest.fail(
            f"Found {len(critical_issues)} critical external link issues:\n"
            + "\n".join(error_details)
        )


@pytest.mark.asyncio
async def test_navigation_structure_completeness(link_validator):
    """Test that navigation structure is complete and consistent."""
    site_dir = link_validator.site_dir

    # Check that key pages exist
    required_pages = [
        "index.html",
        "product/index.html",
        "product/getting-started/index.html",
        "product/installation/index.html",
        "development/index.html",
        "journey/index.html",
    ]

    missing_pages = []
    for page in required_pages:
        page_path = site_dir / page
        if not page_path.exists():
            missing_pages.append(page)

    if missing_pages:
        pytest.fail(f"Missing required pages: {missing_pages}")


def test_site_structure_consistency():
    """Test that the site directory structure is consistent."""
    site_dir = Path(__file__).parent.parent.parent / "site"

    if not site_dir.exists():
        pytest.fail("Site directory does not exist. Run 'mkdocs build' first.")

    # Check for essential directories
    required_dirs = ["assets", "product", "development", "journey"]

    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = site_dir / dir_name
        if not dir_path.exists():
            missing_dirs.append(dir_name)

    if missing_dirs:
        pytest.fail(f"Missing required directories: {missing_dirs}")


@pytest.mark.asyncio
async def test_fragment_links_validation(link_validator):
    """Test that all fragment links (#anchors) are valid."""
    results = await link_validator.validate_all_links()

    # Fragment issues are included in internal validation
    fragment_issues = [
        issue
        for issue in results["internal_validation"]
        if issue["type"] in ["missing_fragment", "fragment_validation_error"]
    ]

    if fragment_issues:
        error_details = []
        for issue in fragment_issues:
            error_details.append(
                f"  - {issue['source_file']}: {issue['target_link']} -> {issue['error']}"
            )

        pytest.fail(
            f"Found {len(fragment_issues)} fragment link issues:\n"
            + "\n".join(error_details)
        )


if __name__ == "__main__":
    # Allow running this module directly for debugging
    import sys

    async def main():
        validator = LinkValidator(Path("site"))
        results = await validator.validate_all_links()

        print("Link Validation Results:")
        print(f"Files processed: {results['summary']['total_files_processed']}")
        print(f"Internal links: {results['summary']['internal_links_found']}")
        print(f"External links: {results['summary']['external_links_found']}")
        print(f"Asset links: {results['summary']['asset_links_found']}")
        print(f"Broken links: {results['summary']['broken_links_total']}")

        if results["summary"]["broken_links_total"] > 0:
            sys.exit(1)

    asyncio.run(main())
