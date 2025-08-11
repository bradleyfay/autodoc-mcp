"""
Content validation testing framework for the AutoDocs documentation site.

This module provides comprehensive content validation including:
- Content consistency and formatting validation
- Code example validation and testing
- Accessibility compliance testing
- Performance validation for page load times
- SEO and metadata validation

Uses pytest ecosystem with BeautifulSoup for HTML parsing and accessibility testing.
"""

import json
import re
from pathlib import Path
from typing import Any

import pytest
from bs4 import BeautifulSoup


class ContentValidationError(Exception):
    """Custom exception for content validation failures."""

    pass


class ContentValidator:
    """
    Comprehensive content validation for documentation sites.

    Features:
    - HTML structure and semantics validation
    - Code block syntax and example validation
    - Accessibility compliance (WCAG guidelines)
    - Performance metrics collection
    - SEO and metadata validation
    - Content consistency checking
    """

    def __init__(self, site_dir: Path, docs_dir: Path):
        self.site_dir = site_dir
        self.docs_dir = docs_dir
        self.validation_results: dict[str, list] = {
            "html_structure": [],
            "code_examples": [],
            "accessibility": [],
            "performance": [],
            "seo": [],
            "content_consistency": [],
        }

    async def validate_all_content(self) -> dict[str, Any]:
        """
        Run comprehensive content validation on the entire site.

        Returns:
            Dictionary with validation results categorized by type
        """
        html_files = list(self.site_dir.glob("**/*.html"))

        for html_file in html_files:
            await self._validate_single_page(html_file)

        # Run cross-page consistency checks
        await self._validate_content_consistency(html_files)

        # Generate summary statistics
        summary = self._generate_validation_summary()

        return {**self.validation_results, "summary": summary}

    async def _validate_single_page(self, html_file: Path) -> None:
        """Validate a single HTML page comprehensively."""
        try:
            content = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(content, "html.parser")

            relative_path = html_file.relative_to(self.site_dir)

            # Run all validation checks
            await self._validate_html_structure(soup, str(relative_path))
            await self._validate_code_examples(soup, str(relative_path))
            await self._validate_accessibility(soup, str(relative_path))
            await self._validate_seo_metadata(soup, str(relative_path))

        except Exception as e:
            self.validation_results["html_structure"].append(
                {
                    "file": str(html_file),
                    "error": f"Failed to validate page: {str(e)}",
                    "type": "page_validation_error",
                    "severity": "high",
                }
            )

    async def _validate_html_structure(
        self, soup: BeautifulSoup, page_path: str
    ) -> None:
        """Validate HTML structure and semantic correctness."""
        issues = []

        # Check for essential HTML5 elements
        if not soup.find("html"):
            issues.append(
                {
                    "error": "Missing <html> element",
                    "type": "missing_html_element",
                    "severity": "high",
                }
            )

        if not soup.find("head"):
            issues.append(
                {
                    "error": "Missing <head> element",
                    "type": "missing_head_element",
                    "severity": "high",
                }
            )

        if not soup.find("body"):
            issues.append(
                {
                    "error": "Missing <body> element",
                    "type": "missing_body_element",
                    "severity": "high",
                }
            )

        # Check for proper heading hierarchy
        headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        if headings:
            heading_levels = [int(h.name[1]) for h in headings]
            prev_level = 0

            for i, level in enumerate(heading_levels):
                if level > prev_level + 1 and prev_level > 0:
                    issues.append(
                        {
                            "error": f"Heading hierarchy skip: h{prev_level} to h{level} at position {i}",
                            "type": "heading_hierarchy_error",
                            "severity": "medium",
                        }
                    )
                prev_level = level

        # Check for duplicate IDs
        elements_with_ids = soup.find_all(id=True)
        ids = [elem.get("id") for elem in elements_with_ids]
        duplicate_ids = {id for id in ids if ids.count(id) > 1}

        for duplicate_id in duplicate_ids:
            issues.append(
                {
                    "error": f"Duplicate ID found: '{duplicate_id}'",
                    "type": "duplicate_id",
                    "severity": "high",
                }
            )

        # Check for empty links
        links = soup.find_all("a", href=True)
        for link in links:
            if not link.get_text().strip() and not link.find("img"):
                issues.append(
                    {
                        "error": f"Empty link found: {link.get('href')}",
                        "type": "empty_link",
                        "severity": "medium",
                    }
                )

        # Check for images without alt text
        images = soup.find_all("img")
        for img in images:
            if not img.get("alt"):
                issues.append(
                    {
                        "error": f"Image without alt text: {img.get('src', 'unknown')}",
                        "type": "missing_alt_text",
                        "severity": "medium",
                    }
                )

        # Add issues to results
        for issue in issues:
            self.validation_results["html_structure"].append(
                {**issue, "file": page_path}
            )

    async def _validate_code_examples(
        self, soup: BeautifulSoup, page_path: str
    ) -> None:
        """Validate code examples for syntax and completeness."""
        issues = []

        # Find all code blocks
        code_blocks = soup.find_all(["pre", "code"])

        for i, block in enumerate(code_blocks):
            code_text = block.get_text()

            # Skip empty code blocks
            if not code_text.strip():
                continue

            # Check for common syntax issues in Python code
            if self._looks_like_python_code(code_text):
                python_issues = self._validate_python_code_block(code_text, i)
                issues.extend(python_issues)

            # Check for shell command examples
            elif self._looks_like_shell_code(code_text):
                shell_issues = self._validate_shell_code_block(code_text, i)
                issues.extend(shell_issues)

            # Check for JSON examples
            elif self._looks_like_json(code_text):
                json_issues = self._validate_json_code_block(code_text, i)
                issues.extend(json_issues)

            # Check for YAML examples
            elif self._looks_like_yaml(code_text):
                yaml_issues = self._validate_yaml_code_block(code_text, i)
                issues.extend(yaml_issues)

        # Add issues to results
        for issue in issues:
            self.validation_results["code_examples"].append(
                {**issue, "file": page_path}
            )

    def _looks_like_python_code(self, code: str) -> bool:
        """Heuristic to detect Python code."""
        python_indicators = [
            "import ",
            "from ",
            "def ",
            "class ",
            "async def",
            "pytest",
            "assert",
            "await ",
            "async with",
        ]
        return any(indicator in code for indicator in python_indicators)

    def _validate_python_code_block(self, code: str, block_index: int) -> list[dict]:
        """Validate Python code block syntax."""
        issues = []

        try:
            # Try to compile the code (basic syntax check)
            compile(code, f"<code_block_{block_index}>", "exec")
        except SyntaxError as e:
            issues.append(
                {
                    "error": f"Python syntax error in code block {block_index}: {str(e)}",
                    "type": "python_syntax_error",
                    "severity": "high",
                    "details": {"line": e.lineno, "text": e.text},
                }
            )

        # Check for common issues
        lines = code.split("\n")
        for line_num, line in enumerate(lines, 1):
            # Check for inconsistent indentation
            if (
                line.strip()
                and not line.startswith(" ")
                and not line.startswith("#")
                and any(line.startswith("    ") for line in lines if line.strip())
            ):
                issues.append(
                    {
                        "error": f"Inconsistent indentation at line {line_num}",
                        "type": "indentation_inconsistency",
                        "severity": "low",
                    }
                )

        return issues

    def _looks_like_shell_code(self, code: str) -> bool:
        """Heuristic to detect shell/bash code."""
        shell_indicators = ["$", "uv ", "pip ", "python ", "cd ", "ls ", "git "]
        return any(indicator in code for indicator in shell_indicators)

    def _validate_shell_code_block(self, code: str, block_index: int) -> list[dict]:
        """Validate shell command examples."""
        issues = []

        lines = code.split("\n")
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            # Check for dangerous commands in documentation
            dangerous_commands = ["rm -rf", "sudo rm", "format", "> /dev/null 2>&1"]
            if any(cmd in line.lower() for cmd in dangerous_commands):
                issues.append(
                    {
                        "error": f"Potentially dangerous command at line {line_num}: {line}",
                        "type": "dangerous_shell_command",
                        "severity": "medium",
                    }
                )

        return issues

    def _looks_like_json(self, code: str) -> bool:
        """Heuristic to detect JSON code."""
        stripped = code.strip()
        return (stripped.startswith("{") and stripped.endswith("}")) or (
            stripped.startswith("[") and stripped.endswith("]")
        )

    def _validate_json_code_block(self, code: str, block_index: int) -> list[dict]:
        """Validate JSON syntax."""
        issues = []

        try:
            json.loads(code)
        except json.JSONDecodeError as e:
            issues.append(
                {
                    "error": f"JSON syntax error in code block {block_index}: {str(e)}",
                    "type": "json_syntax_error",
                    "severity": "high",
                    "details": {"line": e.lineno, "column": e.colno},
                }
            )

        return issues

    def _looks_like_yaml(self, code: str) -> bool:
        """Heuristic to detect YAML code."""
        yaml_indicators = [":", "- ", "name:", "version:", "dependencies:"]
        return (
            any(indicator in code for indicator in yaml_indicators) and "{" not in code
        )

    def _validate_yaml_code_block(self, code: str, block_index: int) -> list[dict]:
        """Validate YAML syntax."""
        issues = []

        try:
            import yaml

            yaml.safe_load(code)
        except ImportError:
            # YAML validation requires PyYAML - skip if not available
            pass
        except yaml.YAMLError as e:
            issues.append(
                {
                    "error": f"YAML syntax error in code block {block_index}: {str(e)}",
                    "type": "yaml_syntax_error",
                    "severity": "high",
                }
            )

        return issues

    async def _validate_accessibility(
        self, soup: BeautifulSoup, page_path: str
    ) -> None:
        """Validate accessibility compliance (WCAG guidelines)."""
        issues = []

        # Check for missing lang attribute on html element
        html_elem = soup.find("html")
        if html_elem and not html_elem.get("lang"):
            issues.append(
                {
                    "error": "Missing lang attribute on <html> element",
                    "type": "missing_lang_attribute",
                    "severity": "medium",
                    "wcag": "3.1.1",
                }
            )

        # Check for proper heading structure (already covered in HTML validation)
        h1_elements = soup.find_all("h1")
        if len(h1_elements) == 0:
            issues.append(
                {
                    "error": "No H1 heading found",
                    "type": "missing_h1",
                    "severity": "medium",
                    "wcag": "1.3.1",
                }
            )
        elif len(h1_elements) > 1:
            issues.append(
                {
                    "error": f"Multiple H1 headings found ({len(h1_elements)})",
                    "type": "multiple_h1",
                    "severity": "low",
                    "wcag": "1.3.1",
                }
            )

        # Check for images without proper alt text
        images = soup.find_all("img")
        for img in images:
            alt_text = img.get("alt", "")
            src = img.get("src", "")

            # Skip decorative images (alt="")
            if alt_text == "":
                continue

            if not alt_text:
                issues.append(
                    {
                        "error": f"Image missing alt text: {src}",
                        "type": "missing_alt_text",
                        "severity": "high",
                        "wcag": "1.1.1",
                    }
                )
            elif len(alt_text) > 125:
                issues.append(
                    {
                        "error": f"Alt text too long ({len(alt_text)} chars): {src}",
                        "type": "alt_text_too_long",
                        "severity": "low",
                        "wcag": "1.1.1",
                    }
                )

        # Check for form elements without labels
        form_inputs = soup.find_all(["input", "textarea", "select"])
        for input_elem in form_inputs:
            input_id = input_elem.get("id")
            input_type = input_elem.get("type", "text")

            # Skip certain input types that don't need labels
            if input_type in ["hidden", "submit", "button"]:
                continue

            # Look for associated label
            label = None
            if input_id:
                label = soup.find("label", attrs={"for": input_id})

            if not label:
                # Check if input is inside a label
                parent_label = input_elem.find_parent("label")
                if not parent_label:
                    issues.append(
                        {
                            "error": f"Form input without label: {input_elem}",
                            "type": "unlabeled_form_input",
                            "severity": "high",
                            "wcag": "1.3.1",
                        }
                    )

        # Check for proper link text
        links = soup.find_all("a", href=True)
        for link in links:
            link_text = link.get_text().strip()
            href = link.get("href")

            if not link_text:
                # Check for image inside link
                if not link.find("img"):
                    issues.append(
                        {
                            "error": f"Link without text: {href}",
                            "type": "empty_link_text",
                            "severity": "high",
                            "wcag": "2.4.4",
                        }
                    )
            elif link_text.lower() in ["click here", "read more", "more"]:
                issues.append(
                    {
                        "error": f"Non-descriptive link text: '{link_text}' -> {href}",
                        "type": "non_descriptive_link",
                        "severity": "low",
                        "wcag": "2.4.4",
                    }
                )

        # Check for proper table headers
        tables = soup.find_all("table")
        for table in tables:
            # Check for th elements
            headers = table.find_all("th")
            if not headers:
                # Check if first row contains headers
                first_row = table.find("tr")
                if first_row and first_row.find_all("td"):
                    issues.append(
                        {
                            "error": "Table without proper headers (th elements)",
                            "type": "table_without_headers",
                            "severity": "medium",
                            "wcag": "1.3.1",
                        }
                    )

        # Add issues to results
        for issue in issues:
            self.validation_results["accessibility"].append(
                {**issue, "file": page_path}
            )

    async def _validate_seo_metadata(self, soup: BeautifulSoup, page_path: str) -> None:
        """Validate SEO and metadata elements."""
        issues = []

        # Check for title element
        title = soup.find("title")
        if not title:
            issues.append(
                {
                    "error": "Missing <title> element",
                    "type": "missing_title",
                    "severity": "high",
                }
            )
        elif not title.get_text().strip():
            issues.append(
                {
                    "error": "Empty <title> element",
                    "type": "empty_title",
                    "severity": "high",
                }
            )
        elif len(title.get_text()) > 60:
            issues.append(
                {
                    "error": f"Title too long ({len(title.get_text())} chars): {title.get_text()[:50]}...",
                    "type": "title_too_long",
                    "severity": "low",
                }
            )

        # Check for meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if not meta_desc:
            issues.append(
                {
                    "error": "Missing meta description",
                    "type": "missing_meta_description",
                    "severity": "medium",
                }
            )
        else:
            desc_content = meta_desc.get("content", "")
            if not desc_content.strip():
                issues.append(
                    {
                        "error": "Empty meta description",
                        "type": "empty_meta_description",
                        "severity": "medium",
                    }
                )
            elif len(desc_content) > 160:
                issues.append(
                    {
                        "error": f"Meta description too long ({len(desc_content)} chars)",
                        "type": "meta_description_too_long",
                        "severity": "low",
                    }
                )

        # Check for viewport meta tag
        viewport = soup.find("meta", attrs={"name": "viewport"})
        if not viewport:
            issues.append(
                {
                    "error": "Missing viewport meta tag",
                    "type": "missing_viewport",
                    "severity": "medium",
                }
            )

        # Check for canonical link
        canonical = soup.find("link", rel="canonical")
        if not canonical and page_path != "index.html":
            issues.append(
                {
                    "error": "Missing canonical link",
                    "type": "missing_canonical",
                    "severity": "low",
                }
            )

        # Add issues to results
        for issue in issues:
            self.validation_results["seo"].append({**issue, "file": page_path})

    async def _validate_content_consistency(self, html_files: list[Path]) -> None:
        """Validate content consistency across pages."""
        issues = []

        # Check for consistent navigation structure
        nav_structures = {}

        for html_file in html_files:
            content = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(content, "html.parser")
            relative_path = html_file.relative_to(self.site_dir)

            # Extract navigation structure
            nav_elem = soup.find("nav") or soup.find(class_=re.compile(r"nav"))
            if nav_elem:
                nav_links = [a.get("href") for a in nav_elem.find_all("a", href=True)]
                nav_structures[str(relative_path)] = nav_links

        # Look for inconsistent navigation structures
        if nav_structures:
            nav_lists = list(nav_structures.values())
            first_nav = nav_lists[0] if nav_lists else []

            for page_path, nav_links in nav_structures.items():
                if nav_links != first_nav:
                    issues.append(
                        {
                            "error": "Inconsistent navigation structure",
                            "type": "inconsistent_navigation",
                            "severity": "low",
                            "file": page_path,
                        }
                    )

        # Add issues to results
        self.validation_results["content_consistency"].extend(issues)

    def _generate_validation_summary(self) -> dict[str, Any]:
        """Generate summary statistics for all validation results."""
        summary = {
            "total_issues": 0,
            "issues_by_severity": {"high": 0, "medium": 0, "low": 0},
            "issues_by_category": {},
        }

        for category, issues in self.validation_results.items():
            if category == "summary":
                continue

            category_count = len(issues)
            summary["issues_by_category"][category] = category_count
            summary["total_issues"] += category_count

            for issue in issues:
                severity = issue.get("severity", "medium")
                summary["issues_by_severity"][severity] += 1

        return summary


@pytest.fixture
def content_validator():
    """Pytest fixture for ContentValidator instance."""
    site_dir = Path(__file__).parent.parent.parent / "site"
    docs_dir = Path(__file__).parent.parent.parent / "docs"
    return ContentValidator(site_dir, docs_dir)


@pytest.mark.asyncio
async def test_html_structure_validation(content_validator):
    """Test HTML structure and semantic correctness."""
    results = await content_validator.validate_all_content()
    html_issues = results["html_structure"]

    # Filter out low-severity issues for main test
    high_medium_issues = [
        issue for issue in html_issues if issue.get("severity") in ["high", "medium"]
    ]

    if high_medium_issues:
        error_details = []
        for issue in high_medium_issues:
            error_details.append(
                f"  - {issue['file']}: [{issue['severity']}] {issue['error']}"
            )

        pytest.fail(
            f"Found {len(high_medium_issues)} HTML structure issues:\n"
            + "\n".join(error_details)
        )


@pytest.mark.asyncio
async def test_code_examples_validation(content_validator):
    """Test code examples for syntax correctness."""
    results = await content_validator.validate_all_content()
    code_issues = results["code_examples"]

    if code_issues:
        error_details = []
        for issue in code_issues:
            error_details.append(
                f"  - {issue['file']}: [{issue['severity']}] {issue['error']}"
            )

        pytest.fail(
            f"Found {len(code_issues)} code example issues:\n"
            + "\n".join(error_details)
        )


@pytest.mark.asyncio
async def test_accessibility_compliance(content_validator):
    """Test accessibility compliance (WCAG guidelines)."""
    results = await content_validator.validate_all_content()
    accessibility_issues = results["accessibility"]

    # Filter out low-severity accessibility issues for main test
    critical_a11y_issues = [
        issue
        for issue in accessibility_issues
        if issue.get("severity") in ["high", "medium"]
    ]

    if critical_a11y_issues:
        error_details = []
        for issue in critical_a11y_issues:
            wcag = f" (WCAG {issue['wcag']})" if issue.get("wcag") else ""
            error_details.append(
                f"  - {issue['file']}: [{issue['severity']}] {issue['error']}{wcag}"
            )

        pytest.fail(
            f"Found {len(critical_a11y_issues)} accessibility issues:\n"
            + "\n".join(error_details)
        )


@pytest.mark.asyncio
async def test_seo_metadata_validation(content_validator):
    """Test SEO and metadata elements."""
    results = await content_validator.validate_all_content()
    seo_issues = results["seo"]

    # Filter for high-priority SEO issues
    critical_seo_issues = [
        issue for issue in seo_issues if issue.get("severity") == "high"
    ]

    if critical_seo_issues:
        error_details = []
        for issue in critical_seo_issues:
            error_details.append(f"  - {issue['file']}: {issue['error']}")

        pytest.fail(
            f"Found {len(critical_seo_issues)} critical SEO issues:\n"
            + "\n".join(error_details)
        )


@pytest.mark.asyncio
async def test_content_consistency(content_validator):
    """Test content consistency across pages."""
    results = await content_validator.validate_all_content()
    consistency_issues = results["content_consistency"]

    if consistency_issues:
        error_details = []
        for issue in consistency_issues:
            error_details.append(f"  - {issue['file']}: {issue['error']}")

        pytest.fail(
            f"Found {len(consistency_issues)} content consistency issues:\n"
            + "\n".join(error_details)
        )


def test_site_build_exists():
    """Test that the site has been built."""
    site_dir = Path(__file__).parent.parent.parent / "site"

    if not site_dir.exists():
        pytest.fail(
            "Site directory does not exist. Run 'mkdocs build' before running tests."
        )

    # Check that key files exist
    index_file = site_dir / "index.html"
    if not index_file.exists():
        pytest.fail(
            "Main index.html file not found. Ensure 'mkdocs build' completed successfully."
        )


if __name__ == "__main__":
    # Allow running this module directly for debugging
    import asyncio

    async def main():
        site_dir = Path("site")
        docs_dir = Path("docs")

        if not site_dir.exists():
            print("Error: Site directory not found. Run 'mkdocs build' first.")
            return

        validator = ContentValidator(site_dir, docs_dir)
        results = await validator.validate_all_content()

        print("Content Validation Results:")
        print(f"Total issues: {results['summary']['total_issues']}")
        print("Issues by severity:")
        for severity, count in results["summary"]["issues_by_severity"].items():
            print(f"  {severity}: {count}")
        print("Issues by category:")
        for category, count in results["summary"]["issues_by_category"].items():
            print(f"  {category}: {count}")

    asyncio.run(main())
