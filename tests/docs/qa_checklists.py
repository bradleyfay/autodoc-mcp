"""
Comprehensive Quality Assurance checklists and validation processes.

This module provides structured QA checklists and automated validation
processes for the AutoDocs documentation site, including:
- Pre-deployment validation checklists
- Content update verification procedures
- Release quality gates
- Automated quality assurance workflows
- Manual testing procedures

Used in conjunction with automated testing for comprehensive quality coverage.
"""

import json
import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import pytest


class QASeverity(Enum):
    """QA issue severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class QAStatus(Enum):
    """QA check status."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


@dataclass
class QACheckResult:
    """Result of a QA check."""

    check_name: str
    status: QAStatus
    severity: QASeverity
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: float | None = None


@dataclass
class QAChecklist:
    """A collection of QA checks."""

    name: str
    description: str
    checks: list[Callable] = field(default_factory=list)
    results: list[QACheckResult] = field(default_factory=list)
    started_at: datetime | None = None
    completed_at: datetime | None = None


class QAValidator:
    """
    Comprehensive QA validation system.

    Provides structured QA checklists, automated validation processes,
    and reporting for documentation site quality assurance.
    """

    def __init__(self, site_dir: Path, docs_dir: Path):
        self.site_dir = site_dir
        self.docs_dir = docs_dir
        self.checklists: dict[str, QAChecklist] = {}
        self.results_history: list[dict] = []
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up structured logging for QA validation."""
        logger = logging.getLogger("qa_validator")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def register_checklist(self, checklist: QAChecklist) -> None:
        """Register a QA checklist."""
        self.checklists[checklist.name] = checklist
        self.logger.info(f"Registered QA checklist: {checklist.name}")

    async def run_checklist(self, checklist_name: str) -> QAChecklist:
        """Run a specific QA checklist."""
        if checklist_name not in self.checklists:
            raise ValueError(f"Checklist '{checklist_name}' not found")

        checklist = self.checklists[checklist_name]
        checklist.started_at = datetime.now()
        checklist.results = []

        self.logger.info(f"Starting QA checklist: {checklist_name}")

        for check_func in checklist.checks:
            try:
                start_time = datetime.now()
                result = await self._run_single_check(check_func)
                end_time = datetime.now()

                result.duration_ms = (end_time - start_time).total_seconds() * 1000
                checklist.results.append(result)

                self.logger.info(
                    f"Check '{result.check_name}' completed: {result.status.value}"
                )

            except Exception as e:
                error_result = QACheckResult(
                    check_name=check_func.__name__,
                    status=QAStatus.FAILED,
                    severity=QASeverity.HIGH,
                    message=f"Check execution failed: {str(e)}",
                    details={"exception_type": type(e).__name__},
                )
                checklist.results.append(error_result)
                self.logger.error(f"Check '{check_func.__name__}' failed: {str(e)}")

        checklist.completed_at = datetime.now()
        self.logger.info(f"Completed QA checklist: {checklist_name}")

        return checklist

    async def _run_single_check(self, check_func: Callable) -> QACheckResult:
        """Run a single QA check function."""
        if callable(check_func):
            # Handle both sync and async check functions
            if hasattr(check_func, "__code__") and "async" in str(check_func.__code__):
                return await check_func(self)
            else:
                return check_func(self)
        else:
            raise ValueError(f"Invalid check function: {check_func}")

    def generate_report(self, checklist_name: str, format: str = "text") -> str:
        """Generate a QA report for a checklist."""
        if checklist_name not in self.checklists:
            raise ValueError(f"Checklist '{checklist_name}' not found")

        checklist = self.checklists[checklist_name]

        if format == "json":
            return self._generate_json_report(checklist)
        elif format == "html":
            return self._generate_html_report(checklist)
        else:
            return self._generate_text_report(checklist)

    def _generate_text_report(self, checklist: QAChecklist) -> str:
        """Generate a text-based QA report."""
        report_lines = []
        report_lines.append(f"QA Report: {checklist.name}")
        report_lines.append("=" * 50)
        report_lines.append(f"Description: {checklist.description}")

        if checklist.started_at and checklist.completed_at:
            duration = checklist.completed_at - checklist.started_at
            report_lines.append(f"Duration: {duration.total_seconds():.2f} seconds")

        # Summary statistics
        total_checks = len(checklist.results)
        passed_checks = len(
            [r for r in checklist.results if r.status == QAStatus.PASSED]
        )
        failed_checks = len(
            [r for r in checklist.results if r.status == QAStatus.FAILED]
        )

        report_lines.append("\nSummary:")
        report_lines.append(f"  Total Checks: {total_checks}")
        report_lines.append(f"  Passed: {passed_checks}")
        report_lines.append(f"  Failed: {failed_checks}")
        report_lines.append(
            f"  Success Rate: {(passed_checks / total_checks * 100):.1f}%"
            if total_checks > 0
            else "  Success Rate: N/A"
        )

        # Detailed results
        report_lines.append("\nDetailed Results:")
        report_lines.append("-" * 30)

        for result in checklist.results:
            status_symbol = {
                QAStatus.PASSED: "✓",
                QAStatus.FAILED: "✗",
                QAStatus.SKIPPED: "○",
                QAStatus.BLOCKED: "■",
            }.get(result.status, "?")

            report_lines.append(
                f"{status_symbol} [{result.severity.value.upper()}] {result.check_name}"
            )
            report_lines.append(f"    {result.message}")

            if result.duration_ms:
                report_lines.append(f"    Duration: {result.duration_ms:.0f}ms")

            if result.details:
                report_lines.append(f"    Details: {result.details}")

            report_lines.append("")

        return "\n".join(report_lines)

    def _generate_json_report(self, checklist: QAChecklist) -> str:
        """Generate a JSON-based QA report."""
        report_data = {
            "checklist_name": checklist.name,
            "description": checklist.description,
            "started_at": checklist.started_at.isoformat()
            if checklist.started_at
            else None,
            "completed_at": checklist.completed_at.isoformat()
            if checklist.completed_at
            else None,
            "results": [
                {
                    "check_name": result.check_name,
                    "status": result.status.value,
                    "severity": result.severity.value,
                    "message": result.message,
                    "details": result.details,
                    "timestamp": result.timestamp.isoformat(),
                    "duration_ms": result.duration_ms,
                }
                for result in checklist.results
            ],
            "summary": {
                "total_checks": len(checklist.results),
                "passed": len(
                    [r for r in checklist.results if r.status == QAStatus.PASSED]
                ),
                "failed": len(
                    [r for r in checklist.results if r.status == QAStatus.FAILED]
                ),
                "skipped": len(
                    [r for r in checklist.results if r.status == QAStatus.SKIPPED]
                ),
                "blocked": len(
                    [r for r in checklist.results if r.status == QAStatus.BLOCKED]
                ),
            },
        }

        return json.dumps(report_data, indent=2)

    def _generate_html_report(self, checklist: QAChecklist) -> str:
        """Generate an HTML-based QA report."""
        # Simplified HTML report - in production, use proper templating
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>QA Report: {checklist.name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .passed {{ color: green; }}
                .failed {{ color: red; }}
                .skipped {{ color: orange; }}
                .summary {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; }}
                .check {{ margin: 10px 0; padding: 10px; border-left: 3px solid #ddd; }}
            </style>
        </head>
        <body>
            <h1>QA Report: {checklist.name}</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Total Checks: {len(checklist.results)}</p>
                <p>Passed: {len([r for r in checklist.results if r.status == QAStatus.PASSED])}</p>
                <p>Failed: {len([r for r in checklist.results if r.status == QAStatus.FAILED])}</p>
            </div>
            <h2>Detailed Results</h2>
        """

        for result in checklist.results:
            status_class = result.status.value
            html_content += f"""
            <div class="check {status_class}">
                <h3>[{result.severity.value.upper()}] {result.check_name}</h3>
                <p>{result.message}</p>
                {f"<p>Duration: {result.duration_ms:.0f}ms</p>" if result.duration_ms else ""}
            </div>
            """

        html_content += """
        </body>
        </html>
        """

        return html_content


# Pre-defined QA Check Functions
def check_site_build_exists(qa_validator: QAValidator) -> QACheckResult:
    """Check that the site has been built successfully."""
    if not qa_validator.site_dir.exists():
        return QACheckResult(
            check_name="site_build_exists",
            status=QAStatus.FAILED,
            severity=QASeverity.CRITICAL,
            message="Site directory does not exist. Run 'mkdocs build' first.",
        )

    index_file = qa_validator.site_dir / "index.html"
    if not index_file.exists():
        return QACheckResult(
            check_name="site_build_exists",
            status=QAStatus.FAILED,
            severity=QASeverity.CRITICAL,
            message="Main index.html not found. Site build may have failed.",
        )

    return QACheckResult(
        check_name="site_build_exists",
        status=QAStatus.PASSED,
        severity=QASeverity.INFO,
        message="Site build verification passed.",
    )


def check_essential_pages_exist(qa_validator: QAValidator) -> QACheckResult:
    """Check that essential pages exist."""
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
        page_path = qa_validator.site_dir / page
        if not page_path.exists():
            missing_pages.append(page)

    if missing_pages:
        return QACheckResult(
            check_name="essential_pages_exist",
            status=QAStatus.FAILED,
            severity=QASeverity.HIGH,
            message=f"Missing essential pages: {missing_pages}",
            details={"missing_pages": missing_pages},
        )

    return QACheckResult(
        check_name="essential_pages_exist",
        status=QAStatus.PASSED,
        severity=QASeverity.INFO,
        message=f"All {len(required_pages)} essential pages exist.",
    )


def check_navigation_consistency(qa_validator: QAValidator) -> QACheckResult:
    """Check that navigation is consistent across pages."""
    try:
        from bs4 import BeautifulSoup

        html_files = list(qa_validator.site_dir.glob("**/*.html"))[:5]  # Sample 5 pages
        nav_structures = []

        for html_file in html_files:
            content = html_file.read_text(encoding="utf-8")
            soup = BeautifulSoup(content, "html.parser")

            # Extract navigation links
            nav_elem = soup.find("nav") or soup.find(
                class_=lambda x: x and "nav" in x.lower()
            )
            if nav_elem:
                nav_links = [a.get("href") for a in nav_elem.find_all("a", href=True)]
                nav_structures.append(nav_links)

        # Check consistency
        if len(nav_structures) > 1:
            first_nav = nav_structures[0]
            inconsistent = any(nav != first_nav for nav in nav_structures[1:])

            if inconsistent:
                return QACheckResult(
                    check_name="navigation_consistency",
                    status=QAStatus.FAILED,
                    severity=QASeverity.MEDIUM,
                    message="Navigation structure is inconsistent across pages.",
                )

        return QACheckResult(
            check_name="navigation_consistency",
            status=QAStatus.PASSED,
            severity=QASeverity.INFO,
            message="Navigation structure is consistent.",
        )

    except ImportError:
        return QACheckResult(
            check_name="navigation_consistency",
            status=QAStatus.SKIPPED,
            severity=QASeverity.LOW,
            message="BeautifulSoup not available for navigation check.",
        )


def check_asset_integrity(qa_validator: QAValidator) -> QACheckResult:
    """Check that essential assets exist."""
    essential_assets = [
        "assets/stylesheets",
        "assets/javascripts",
        "search/search_index.json",
    ]

    missing_assets = []
    for asset in essential_assets:
        asset_path = qa_validator.site_dir / asset
        if not asset_path.exists():
            missing_assets.append(asset)

    if missing_assets:
        return QACheckResult(
            check_name="asset_integrity",
            status=QAStatus.FAILED,
            severity=QASeverity.MEDIUM,
            message=f"Missing essential assets: {missing_assets}",
            details={"missing_assets": missing_assets},
        )

    return QACheckResult(
        check_name="asset_integrity",
        status=QAStatus.PASSED,
        severity=QASeverity.INFO,
        message="All essential assets are present.",
    )


def check_search_functionality(qa_validator: QAValidator) -> QACheckResult:
    """Check that search functionality is properly configured."""
    search_index = qa_validator.site_dir / "search" / "search_index.json"

    if not search_index.exists():
        return QACheckResult(
            check_name="search_functionality",
            status=QAStatus.FAILED,
            severity=QASeverity.MEDIUM,
            message="Search index file not found.",
        )

    try:
        with open(search_index) as f:
            search_data = json.load(f)

        if not search_data.get("docs"):
            return QACheckResult(
                check_name="search_functionality",
                status=QAStatus.FAILED,
                severity=QASeverity.MEDIUM,
                message="Search index is empty or malformed.",
            )

        return QACheckResult(
            check_name="search_functionality",
            status=QAStatus.PASSED,
            severity=QASeverity.INFO,
            message=f"Search index contains {len(search_data['docs'])} documents.",
        )

    except json.JSONDecodeError:
        return QACheckResult(
            check_name="search_functionality",
            status=QAStatus.FAILED,
            severity=QASeverity.MEDIUM,
            message="Search index file is not valid JSON.",
        )


def check_sitemap_generation(qa_validator: QAValidator) -> QACheckResult:
    """Check that sitemap has been generated."""
    sitemap_xml = qa_validator.site_dir / "sitemap.xml"

    if not sitemap_xml.exists():
        return QACheckResult(
            check_name="sitemap_generation",
            status=QAStatus.FAILED,
            severity=QASeverity.LOW,
            message="Sitemap.xml not found.",
        )

    try:
        sitemap_content = sitemap_xml.read_text(encoding="utf-8")
        if "<url>" not in sitemap_content:
            return QACheckResult(
                check_name="sitemap_generation",
                status=QAStatus.FAILED,
                severity=QASeverity.LOW,
                message="Sitemap appears to be empty or malformed.",
            )

        url_count = sitemap_content.count("<url>")
        return QACheckResult(
            check_name="sitemap_generation",
            status=QAStatus.PASSED,
            severity=QASeverity.INFO,
            message=f"Sitemap contains {url_count} URLs.",
        )

    except Exception as e:
        return QACheckResult(
            check_name="sitemap_generation",
            status=QAStatus.FAILED,
            severity=QASeverity.LOW,
            message=f"Error reading sitemap: {str(e)}",
        )


# Pre-defined QA Checklists
def create_pre_deployment_checklist() -> QAChecklist:
    """Create the pre-deployment QA checklist."""
    return QAChecklist(
        name="pre_deployment",
        description="Essential checks before deploying documentation site",
        checks=[
            check_site_build_exists,
            check_essential_pages_exist,
            check_asset_integrity,
            check_search_functionality,
            check_sitemap_generation,
            check_navigation_consistency,
        ],
    )


def create_content_update_checklist() -> QAChecklist:
    """Create the content update QA checklist."""
    return QAChecklist(
        name="content_update",
        description="Checks to run after content updates",
        checks=[
            check_site_build_exists,
            check_essential_pages_exist,
            check_search_functionality,
            check_navigation_consistency,
        ],
    )


def create_release_checklist() -> QAChecklist:
    """Create the release QA checklist."""
    return QAChecklist(
        name="release",
        description="Comprehensive checks for major releases",
        checks=[
            check_site_build_exists,
            check_essential_pages_exist,
            check_navigation_consistency,
            check_asset_integrity,
            check_search_functionality,
            check_sitemap_generation,
        ],
    )


@pytest.fixture
def qa_validator():
    """Pytest fixture for QAValidator instance."""
    site_dir = Path(__file__).parent.parent.parent / "site"
    docs_dir = Path(__file__).parent.parent.parent / "docs"
    return QAValidator(site_dir, docs_dir)


@pytest.mark.asyncio
async def test_pre_deployment_checklist(qa_validator):
    """Test the pre-deployment QA checklist."""
    checklist = create_pre_deployment_checklist()
    qa_validator.register_checklist(checklist)

    result = await qa_validator.run_checklist("pre_deployment")

    # Check for critical failures
    critical_failures = [
        r
        for r in result.results
        if r.status == QAStatus.FAILED and r.severity == QASeverity.CRITICAL
    ]

    if critical_failures:
        error_details = []
        for failure in critical_failures:
            error_details.append(f"  - {failure.check_name}: {failure.message}")

        pytest.fail(
            "Critical pre-deployment failures found:\n" + "\n".join(error_details)
        )


@pytest.mark.asyncio
async def test_content_update_checklist(qa_validator):
    """Test the content update QA checklist."""
    checklist = create_content_update_checklist()
    qa_validator.register_checklist(checklist)

    result = await qa_validator.run_checklist("content_update")

    # Check for high-severity failures
    high_severity_failures = [
        r
        for r in result.results
        if r.status == QAStatus.FAILED
        and r.severity in [QASeverity.CRITICAL, QASeverity.HIGH]
    ]

    if high_severity_failures:
        error_details = []
        for failure in high_severity_failures:
            error_details.append(f"  - {failure.check_name}: {failure.message}")

        pytest.fail(
            "High-severity content update failures found:\n" + "\n".join(error_details)
        )


def test_qa_checklist_registration(qa_validator):
    """Test QA checklist registration and management."""
    checklist = create_pre_deployment_checklist()
    qa_validator.register_checklist(checklist)

    assert "pre_deployment" in qa_validator.checklists
    assert qa_validator.checklists["pre_deployment"].name == "pre_deployment"


if __name__ == "__main__":
    # Allow running this module directly for manual QA validation
    import asyncio

    async def main():
        site_dir = Path("site")
        docs_dir = Path("docs")

        if not site_dir.exists():
            print("Error: Site directory not found. Run 'mkdocs build' first.")
            return

        validator = QAValidator(site_dir, docs_dir)

        # Run pre-deployment checklist
        checklist = create_pre_deployment_checklist()
        validator.register_checklist(checklist)

        print("Running pre-deployment QA checklist...")
        result = await validator.run_checklist("pre_deployment")

        print("\n" + validator.generate_report("pre_deployment"))

        # Check for failures
        failures = [r for r in result.results if r.status == QAStatus.FAILED]
        if failures:
            print(f"\n❌ {len(failures)} checks failed!")
            exit(1)
        else:
            print("\n✅ All QA checks passed!")

    asyncio.run(main())
