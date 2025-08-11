#!/usr/bin/env python3
"""
Documentation testing script for AutoDocs.

This script provides a convenient interface for running documentation tests
locally and in CI environments. It supports different test levels and
provides comprehensive reporting.

Usage:
    python scripts/test_docs.py --help
    python scripts/test_docs.py quick
    python scripts/test_docs.py full
    python scripts/test_docs.py external-links
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


class DocumentationTester:
    """
    Documentation testing coordinator.

    Manages test execution, reporting, and CI integration.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.site_dir = project_root / "site"
        self.tests_dir = project_root / "tests" / "docs"
        self.reports_dir = project_root / "reports"

        # Ensure reports directory exists
        self.reports_dir.mkdir(exist_ok=True)

    def check_prerequisites(self) -> bool:
        """Check that all prerequisites are met."""
        print("🔍 Checking prerequisites...")

        # Check that site is built
        if not self.site_dir.exists():
            print("❌ Site directory not found. Building documentation...")
            if not self.build_documentation():
                return False

        # Check required dependencies
        missing_deps = []

        try:
            import importlib.util

            if importlib.util.find_spec("bs4") is None:
                missing_deps.append("beautifulsoup4")
        except ImportError:
            missing_deps.append("beautifulsoup4")

        try:
            import importlib.util

            if importlib.util.find_spec("httpx") is None:
                missing_deps.append("httpx")
        except ImportError:
            missing_deps.append("httpx")

        if missing_deps:
            print(f"❌ Missing required dependencies: {missing_deps}")
            print("Install with: uv pip install " + " ".join(missing_deps))
            return False

        print("✅ Prerequisites check passed")
        return True

    def build_documentation(self) -> bool:
        """Build the documentation site."""
        print("📖 Building documentation...")

        try:
            result = subprocess.run(
                [sys.executable, "-m", "mkdocs", "build", "--strict"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode == 0:
                print("✅ Documentation built successfully")
                return True
            else:
                print(f"❌ Documentation build failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("❌ Documentation build timed out")
            return False
        except Exception as e:
            print(f"❌ Documentation build error: {e}")
            return False

    def run_quick_tests(self) -> bool:
        """Run quick validation tests."""
        print("\n🚀 Running quick validation tests...")

        test_commands = [
            # QA checklist validation
            [
                "pytest",
                "tests/docs/qa_checklists.py::test_pre_deployment_checklist",
                "-v",
                "--tb=short",
            ],
            # Basic content validation
            [
                "pytest",
                "tests/docs/test_content_validation.py::test_site_build_exists",
                "tests/docs/test_content_validation.py::test_html_structure_validation",
                "-v",
                "--tb=short",
            ],
        ]

        all_passed = True
        for cmd in test_commands:
            result = subprocess.run(cmd, cwd=self.project_root)
            if result.returncode != 0:
                all_passed = False

        return all_passed

    def run_comprehensive_tests(self) -> bool:
        """Run comprehensive test suite."""
        print("\n🔄 Running comprehensive tests...")

        test_suites = [
            {
                "name": "Link Validation",
                "command": ["pytest", "tests/docs/test_link_validation.py", "-v"],
                "report": "link-validation",
            },
            {
                "name": "Content Validation",
                "command": ["pytest", "tests/docs/test_content_validation.py", "-v"],
                "report": "content-validation",
            },
            {
                "name": "QA Checklists",
                "command": ["pytest", "tests/docs/qa_checklists.py", "-v"],
                "report": "qa-checklists",
            },
        ]

        all_passed = True

        for suite in test_suites:
            print(f"\n📋 Running {suite['name']}...")

            cmd = suite["command"] + [
                f"--html={self.reports_dir}/{suite['report']}-report.html",
                "--json-report",
                f"--json-report-file={self.reports_dir}/{suite['report']}.json",
            ]

            result = subprocess.run(cmd, cwd=self.project_root)
            if result.returncode != 0:
                print(f"❌ {suite['name']} failed")
                all_passed = False
            else:
                print(f"✅ {suite['name']} passed")

        return all_passed

    def run_cross_platform_tests(self) -> bool:
        """Run cross-platform tests with Playwright."""
        print("\n🌐 Running cross-platform tests...")

        # Check if Playwright is available
        try:
            import importlib.util

            if importlib.util.find_spec("playwright") is None:
                print(
                    "⚠️ Playwright not available. Install with: uv pip install playwright"
                )
                print("Then run: playwright install")
                return True  # Don't fail if optional dependency is missing
        except ImportError:
            print("⚠️ Playwright not available. Install with: uv pip install playwright")
            print("Then run: playwright install")
            return True  # Don't fail if optional dependency is missing

        # Start local server for testing
        print("🚀 Starting local server...")
        import http.server
        import os
        import socketserver
        import threading

        server_thread = None
        try:
            # Start server in background
            os.chdir(self.site_dir)
            httpd = socketserver.TCPServer(
                ("", 8000), http.server.SimpleHTTPRequestHandler
            )
            server_thread = threading.Thread(target=httpd.serve_forever)
            server_thread.daemon = True
            server_thread.start()

            # Wait for server to start
            time.sleep(2)

            # Run cross-platform tests
            cmd = [
                "pytest",
                "tests/docs/test_cross_platform.py",
                "-v",
                f"--html={self.reports_dir}/cross-platform-report.html",
                "--json-report",
                f"--json-report-file={self.reports_dir}/cross-platform.json",
            ]

            result = subprocess.run(cmd, cwd=self.project_root)

            httpd.shutdown()

            if result.returncode != 0:
                print("❌ Cross-platform tests failed")
                return False
            else:
                print("✅ Cross-platform tests passed")
                return True

        except Exception as e:
            print(f"❌ Cross-platform test error: {e}")
            if server_thread:
                import contextlib

                with contextlib.suppress(Exception):
                    httpd.shutdown()
            return False

    def run_external_link_tests(self) -> bool:
        """Run external link validation tests."""
        print("\n🔗 Running external link validation...")

        cmd = [
            "pytest",
            "tests/docs/test_link_validation.py::test_external_links_validation",
            "-v",
            "--tb=short",
            f"--html={self.reports_dir}/external-links-report.html",
            "--json-report",
            f"--json-report-file={self.reports_dir}/external-links.json",
        ]

        result = subprocess.run(cmd, cwd=self.project_root)

        if result.returncode != 0:
            print("❌ External link validation failed")
            return False
        else:
            print("✅ External link validation passed")
            return True

    def generate_summary_report(self) -> None:
        """Generate a summary report of all test results."""
        print("\n📊 Generating summary report...")

        report_files = list(self.reports_dir.glob("*.json"))
        if not report_files:
            print("⚠️ No test reports found to summarize")
            return

        summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "total_test_suites": len(report_files),
            "test_results": {},
            "overall_status": "passed",
        }

        for report_file in report_files:
            try:
                with open(report_file) as f:
                    report_data = json.load(f)

                suite_name = report_file.stem
                summary["test_results"][suite_name] = {
                    "total": report_data.get("summary", {}).get("total", 0),
                    "passed": report_data.get("summary", {}).get("passed", 0),
                    "failed": report_data.get("summary", {}).get("failed", 0),
                    "duration": report_data.get("duration", 0),
                }

                if report_data.get("summary", {}).get("failed", 0) > 0:
                    summary["overall_status"] = "failed"

            except Exception as e:
                print(f"⚠️ Could not read report {report_file}: {e}")

        # Write summary report
        summary_file = self.reports_dir / "test-summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        # Print summary
        print("\n📋 Test Summary:")
        print(
            f"Overall Status: {'✅ PASSED' if summary['overall_status'] == 'passed' else '❌ FAILED'}"
        )
        print(f"Test Suites: {summary['total_test_suites']}")

        for suite_name, results in summary["test_results"].items():
            status = "✅" if results["failed"] == 0 else "❌"
            print(
                f"  {status} {suite_name}: {results['passed']}/{results['total']} passed"
            )

        print(f"\nDetailed reports available in: {self.reports_dir}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AutoDocs documentation testing")
    subparsers = parser.add_subparsers(dest="command", help="Test command to run")

    # Quick tests
    subparsers.add_parser("quick", help="Run quick validation tests")

    # Full tests
    full_parser = subparsers.add_parser("full", help="Run comprehensive test suite")
    full_parser.add_argument(
        "--skip-cross-platform", action="store_true", help="Skip cross-platform tests"
    )

    # External link tests
    subparsers.add_parser("external-links", help="Run external link validation")

    # Cross-platform tests only
    subparsers.add_parser("cross-platform", help="Run cross-platform tests only")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Initialize tester
    project_root = Path(__file__).parent.parent
    tester = DocumentationTester(project_root)

    # Check prerequisites
    if not tester.check_prerequisites():
        return 1

    success = True

    if args.command == "quick":
        success = tester.run_quick_tests()

    elif args.command == "full":
        success = tester.run_comprehensive_tests()

        if success and not args.skip_cross_platform:
            cross_platform_success = tester.run_cross_platform_tests()
            success = success and cross_platform_success

    elif args.command == "external-links":
        success = tester.run_external_link_tests()

    elif args.command == "cross-platform":
        success = tester.run_cross_platform_tests()

    # Generate summary report
    tester.generate_summary_report()

    if success:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed. Check the reports for details.")
        return 1


if __name__ == "__main__":
    exit(main())
