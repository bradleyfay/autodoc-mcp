#!/usr/bin/env python3
"""
Link Validation Script for AutoDocs Documentation

Validates all internal and external links in the documentation.
Provides detailed reporting and suggestions for fixing broken links.
"""

import concurrent.futures
import re
import time
from pathlib import Path

import requests


class LinkValidator:
    def __init__(self, docs_path: str = "docs", base_url: str = ""):
        self.docs_path = Path(docs_path)
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "AutoDocs Link Validator 1.0"})

        # Results storage
        self.internal_links = set()
        self.external_links = set()
        self.broken_links = []
        self.warnings = []

    def validate_all_links(self) -> dict:
        """Validate all links in documentation."""
        print("🔍 Scanning documentation for links...")

        # Extract all links from markdown files
        self._extract_links_from_docs()

        print(f"Found {len(self.internal_links)} internal links")
        print(f"Found {len(self.external_links)} external links")

        # Validate internal links
        print("\n📋 Validating internal links...")
        internal_results = self._validate_internal_links()

        # Validate external links
        print("\n🌐 Validating external links...")
        external_results = self._validate_external_links()

        return {
            "internal_links": {
                "total": len(self.internal_links),
                "broken": len([r for r in internal_results if not r["valid"]]),
                "results": internal_results,
            },
            "external_links": {
                "total": len(self.external_links),
                "broken": len([r for r in external_results if not r["valid"]]),
                "results": external_results,
            },
            "warnings": self.warnings,
        }

    def _extract_links_from_docs(self):
        """Extract all links from markdown files."""
        for md_file in self.docs_path.rglob("*.md"):
            if "assets" in str(md_file):  # Skip asset documentation
                continue

            with open(md_file, encoding="utf-8") as f:
                content = f.read()

            # Find markdown links [text](url)
            markdown_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)

            for _text, url in markdown_links:
                # Clean URL (remove anchors for validation)
                clean_url = url.split("#")[0]

                if clean_url.startswith(("http://", "https://")):
                    self.external_links.add(clean_url)
                elif clean_url and not clean_url.startswith(("mailto:", "tel:")):
                    # Internal link - convert relative to absolute path
                    if clean_url.startswith("/"):
                        self.internal_links.add(clean_url)
                    else:
                        # Relative link - convert to absolute
                        try:
                            base_dir = md_file.parent
                            abs_path = (base_dir / clean_url).resolve()
                            rel_path = abs_path.relative_to(self.docs_path.resolve())
                            self.internal_links.add(
                                "/" + str(rel_path).replace("\\", "/")
                            )
                        except ValueError:
                            # Link points outside docs directory, treat as external or add warning
                            self.warnings.append(
                                f"Link '{clean_url}' in {md_file} points outside docs directory"
                            )
                            self.internal_links.add(
                                clean_url
                            )  # Still validate as internal

    def _validate_internal_links(self) -> list[dict]:
        """Validate internal documentation links."""
        results = []

        for link in sorted(self.internal_links):
            result = self._check_internal_link(link)
            results.append(result)

            status = "✅" if result["valid"] else "❌"
            print(f"  {status} {link}")

            if not result["valid"]:
                self.broken_links.append(result)

        return results

    def _check_internal_link(self, link: str) -> dict:
        """Check if internal link is valid."""
        # Remove leading slash and convert to file path
        file_path = link.lstrip("/")

        # Try different file extensions and index files
        possible_paths = [
            self.docs_path / file_path,
            self.docs_path / file_path / "index.md",
            self.docs_path / f"{file_path}.md",
        ]

        for path in possible_paths:
            if path.exists() and path.is_file():
                return {
                    "url": link,
                    "valid": True,
                    "resolved_path": str(path),
                    "type": "internal",
                }

        return {
            "url": link,
            "valid": False,
            "error": "File not found",
            "suggested_paths": [str(p) for p in possible_paths],
            "type": "internal",
        }

    def _validate_external_links(self) -> list[dict]:
        """Validate external links with concurrent requests."""
        results = []

        # Use thread pool for concurrent validation
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {
                executor.submit(self._check_external_link, url): url
                for url in sorted(self.external_links)
            }

            for future in concurrent.futures.as_completed(future_to_url):
                result = future.result()
                results.append(result)

                status = "✅" if result["valid"] else "❌"
                print(f"  {status} {result['url']}")

                if not result["valid"]:
                    self.broken_links.append(result)

        return results

    def _check_external_link(self, url: str) -> dict:
        """Check if external link is accessible."""
        try:
            # Some sites block HEAD requests, so try GET with timeout
            response = self.session.get(url, timeout=10, allow_redirects=True)

            return {
                "url": url,
                "valid": response.status_code < 400,
                "status_code": response.status_code,
                "final_url": response.url,
                "type": "external",
            }

        except requests.exceptions.RequestException as e:
            return {"url": url, "valid": False, "error": str(e), "type": "external"}

    def generate_report(self, results: dict) -> str:
        """Generate a comprehensive link validation report."""
        report = []
        report.append("# Link Validation Report")
        report.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Summary
        total_links = (
            results["internal_links"]["total"] + results["external_links"]["total"]
        )
        total_broken = (
            results["internal_links"]["broken"] + results["external_links"]["broken"]
        )

        report.append("## Summary")
        report.append(f"- **Total Links**: {total_links}")
        report.append(f"- **Broken Links**: {total_broken}")
        report.append(
            f"- **Success Rate**: {((total_links - total_broken) / total_links * 100):.1f}%"
        )
        report.append("")

        # Internal Links
        report.append("## Internal Links")
        report.append(f"- **Total**: {results['internal_links']['total']}")
        report.append(f"- **Broken**: {results['internal_links']['broken']}")

        if results["internal_links"]["broken"] > 0:
            report.append("\n### Broken Internal Links")
            for result in results["internal_links"]["results"]:
                if not result["valid"]:
                    report.append(f"- ❌ `{result['url']}`")
                    report.append(f"  - Error: {result.get('error', 'Unknown error')}")
                    if "suggested_paths" in result:
                        report.append("  - Suggested fixes:")
                        for path in result["suggested_paths"]:
                            report.append(f"    - `{path}`")
        else:
            report.append("- ✅ All internal links are valid")

        report.append("")

        # External Links
        report.append("## External Links")
        report.append(f"- **Total**: {results['external_links']['total']}")
        report.append(f"- **Broken**: {results['external_links']['broken']}")

        if results["external_links"]["broken"] > 0:
            report.append("\n### Broken External Links")
            for result in results["external_links"]["results"]:
                if not result["valid"]:
                    report.append(f"- ❌ `{result['url']}`")
                    if "status_code" in result:
                        report.append(f"  - Status Code: {result['status_code']}")
                    if "error" in result:
                        report.append(f"  - Error: {result['error']}")
        else:
            report.append("- ✅ All external links are valid")

        # Warnings
        if results["warnings"]:
            report.append("\n## Warnings")
            for warning in results["warnings"]:
                report.append(f"- ⚠️ {warning}")

        report.append("")

        # Recommendations
        report.append("## Recommendations")
        if total_broken == 0:
            report.append("- ✅ All links are valid! No action required.")
        else:
            report.append("- Fix broken internal links by checking file paths")
            report.append("- Update or remove broken external links")
            report.append("- Consider implementing link checking in CI/CD pipeline")
            report.append("- Set up monitoring for external link health")

        return "\n".join(report)


def main():
    """Main function to run link validation."""
    print("🔗 AutoDocs Link Validation")
    print("=" * 40)

    validator = LinkValidator()
    results = validator.validate_all_links()

    # Generate and display report
    report = validator.generate_report(results)
    print("\n" + "=" * 40)
    print(report)

    # Save report to file
    report_path = Path("link_validation_report.md")
    with open(report_path, "w") as f:
        f.write(report)

    print(f"\n📄 Full report saved to: {report_path}")

    # Exit with error code if links are broken
    total_broken = (
        results["internal_links"]["broken"] + results["external_links"]["broken"]
    )
    if total_broken > 0:
        print(f"\n❌ {total_broken} broken links found!")
        exit(1)
    else:
        print("\n✅ All links are valid!")


if __name__ == "__main__":
    main()
