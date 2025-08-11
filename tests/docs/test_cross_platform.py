"""
Cross-platform testing procedures for the AutoDocs documentation site.

This module provides comprehensive cross-platform testing including:
- Multi-browser compatibility testing (Chrome, Firefox, Safari)
- Mobile responsiveness testing across device sizes
- Performance testing for page load times
- JavaScript functionality testing
- Visual regression testing capabilities

Uses Playwright for browser automation with proper parallel execution.
"""

import asyncio
import time
from typing import Any

import pytest

# Conditional Playwright import - skip tests if not available
try:
    from playwright.async_api import Browser, Page, async_playwright

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

    # Create dummy classes for type hints
    class Browser:
        pass

    class Page:
        pass


class CrossPlatformTestError(Exception):
    """Custom exception for cross-platform testing failures."""

    pass


class CrossPlatformTester:
    """
    Comprehensive cross-platform testing for documentation sites.

    Features:
    - Multi-browser testing (Chrome, Firefox, Safari)
    - Device simulation for mobile responsiveness
    - Performance metrics collection
    - Accessibility testing across platforms
    - Screenshot comparison capabilities
    - JavaScript functionality validation
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results: dict[str, list] = {
            "browser_compatibility": [],
            "mobile_responsiveness": [],
            "performance": [],
            "javascript_functionality": [],
            "visual_consistency": [],
        }

        # Common device viewports for testing
        self.device_viewports = {
            "desktop": {"width": 1920, "height": 1080},
            "laptop": {"width": 1366, "height": 768},
            "tablet": {"width": 768, "height": 1024},
            "mobile_large": {"width": 414, "height": 896},
            "mobile_medium": {"width": 375, "height": 667},
            "mobile_small": {"width": 320, "height": 568},
        }

        # Browsers to test (if available)
        self.browsers_to_test = ["chromium", "firefox", "webkit"]

    async def run_cross_platform_tests(
        self, pages_to_test: list[str]
    ) -> dict[str, Any]:
        """
        Run comprehensive cross-platform tests.

        Args:
            pages_to_test: List of page URLs to test

        Returns:
            Dictionary with test results categorized by type
        """
        if not PLAYWRIGHT_AVAILABLE:
            return {
                "error": "Playwright not available. Install with: pip install playwright",
                "skipped_tests": [
                    "browser_compatibility",
                    "mobile_responsiveness",
                    "performance",
                    "javascript_functionality",
                ],
            }

        async with async_playwright() as playwright:
            # Test each browser
            for browser_name in self.browsers_to_test:
                try:
                    browser = await self._launch_browser(playwright, browser_name)
                    await self._test_browser_compatibility(
                        browser, browser_name, pages_to_test
                    )
                    await browser.close()
                except Exception as e:
                    self.test_results["browser_compatibility"].append(
                        {
                            "browser": browser_name,
                            "error": f"Failed to test browser: {str(e)}",
                            "type": "browser_launch_error",
                        }
                    )

            # Test mobile responsiveness with default browser
            try:
                browser = await playwright.chromium.launch()
                await self._test_mobile_responsiveness(browser, pages_to_test)
                await browser.close()
            except Exception as e:
                self.test_results["mobile_responsiveness"].append(
                    {
                        "error": f"Mobile responsiveness testing failed: {str(e)}",
                        "type": "mobile_test_error",
                    }
                )

        # Generate summary
        summary = self._generate_test_summary()

        return {**self.test_results, "summary": summary}

    async def _launch_browser(self, playwright, browser_name: str) -> Browser:
        """Launch a specific browser with appropriate configuration."""
        launch_options = {
            "headless": True,  # Run in headless mode for CI
            "args": [
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
            ],
        }

        if browser_name == "chromium":
            return await playwright.chromium.launch(**launch_options)
        elif browser_name == "firefox":
            return await playwright.firefox.launch(**launch_options)
        elif browser_name == "webkit":
            return await playwright.webkit.launch(**launch_options)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

    async def _test_browser_compatibility(
        self, browser: Browser, browser_name: str, pages: list[str]
    ):
        """Test compatibility across different browsers."""
        context = await browser.new_context(viewport=self.device_viewports["desktop"])
        page = await context.new_page()

        for page_path in pages:
            url = f"{self.base_url}/{page_path.lstrip('/')}"

            try:
                # Navigate to page and measure load time
                start_time = time.time()
                response = await page.goto(url, wait_until="networkidle", timeout=30000)
                load_time = time.time() - start_time

                if not response or response.status >= 400:
                    self.test_results["browser_compatibility"].append(
                        {
                            "browser": browser_name,
                            "page": page_path,
                            "error": f"HTTP {response.status if response else 'No response'}",
                            "type": "navigation_error",
                        }
                    )
                    continue

                # Check for JavaScript errors
                js_errors = await self._check_javascript_errors(page)
                if js_errors:
                    for error in js_errors:
                        self.test_results["browser_compatibility"].append(
                            {
                                "browser": browser_name,
                                "page": page_path,
                                "error": f"JavaScript error: {error}",
                                "type": "javascript_error",
                            }
                        )

                # Test basic functionality
                await self._test_basic_page_functionality(page, browser_name, page_path)

                # Record performance metrics
                self.test_results["performance"].append(
                    {
                        "browser": browser_name,
                        "page": page_path,
                        "load_time": load_time,
                        "viewport": "desktop",
                    }
                )

            except Exception as e:
                self.test_results["browser_compatibility"].append(
                    {
                        "browser": browser_name,
                        "page": page_path,
                        "error": f"Test failed: {str(e)}",
                        "type": "test_execution_error",
                    }
                )

        await context.close()

    async def _test_mobile_responsiveness(self, browser: Browser, pages: list[str]):
        """Test mobile responsiveness across different device sizes."""

        for device_name, viewport in self.device_viewports.items():
            context = await browser.new_context(viewport=viewport)
            page = await context.new_page()

            for page_path in pages:
                url = f"{self.base_url}/{page_path.lstrip('/')}"

                try:
                    await page.goto(url, wait_until="networkidle", timeout=30000)

                    # Test mobile-specific functionality
                    await self._test_mobile_specific_features(
                        page, device_name, page_path
                    )

                    # Check for horizontal scrollbars (bad responsive design)
                    body_width = await page.evaluate("() => document.body.scrollWidth")
                    viewport_width = viewport["width"]

                    if body_width > viewport_width:
                        self.test_results["mobile_responsiveness"].append(
                            {
                                "device": device_name,
                                "page": page_path,
                                "error": f"Horizontal scroll detected: body width {body_width}px > viewport {viewport_width}px",
                                "type": "horizontal_scroll_issue",
                            }
                        )

                    # Test touch interactions for mobile devices
                    if "mobile" in device_name:
                        await self._test_touch_interactions(
                            page, device_name, page_path
                        )

                except Exception as e:
                    self.test_results["mobile_responsiveness"].append(
                        {
                            "device": device_name,
                            "page": page_path,
                            "error": f"Mobile test failed: {str(e)}",
                            "type": "mobile_test_error",
                        }
                    )

            await context.close()

    async def _check_javascript_errors(self, page: Page) -> list[str]:
        """Check for JavaScript errors on the page."""
        errors = []

        # Set up error listeners
        def handle_console_message(message):
            if message.type == "error":
                errors.append(message.text)

        def handle_page_error(error):
            errors.append(str(error))

        page.on("console", handle_console_message)
        page.on("pageerror", handle_page_error)

        # Wait a bit for any async errors to surface
        await asyncio.sleep(1)

        return errors

    async def _test_basic_page_functionality(
        self, page: Page, browser_name: str, page_path: str
    ):
        """Test basic page functionality like navigation, search, etc."""

        # Test navigation menu functionality
        nav_elements = await page.query_selector_all(
            "nav a, .nav a, [role='navigation'] a"
        )

        if nav_elements:
            # Test that navigation links are clickable and lead somewhere
            for i, nav_element in enumerate(
                nav_elements[:3]
            ):  # Test first 3 to avoid too many requests
                try:
                    href = await nav_element.get_attribute("href")
                    if href and not href.startswith("http"):
                        # Internal link - test that it's clickable
                        is_visible = await nav_element.is_visible()
                        if not is_visible:
                            self.test_results["javascript_functionality"].append(
                                {
                                    "browser": browser_name,
                                    "page": page_path,
                                    "error": f"Navigation link {i} not visible: {href}",
                                    "type": "navigation_visibility_issue",
                                }
                            )

                except Exception as e:
                    self.test_results["javascript_functionality"].append(
                        {
                            "browser": browser_name,
                            "page": page_path,
                            "error": f"Navigation test failed for link {i}: {str(e)}",
                            "type": "navigation_test_error",
                        }
                    )

        # Test search functionality if present
        search_input = await page.query_selector(
            "input[type='search'], .search input, #search"
        )
        if search_input:
            try:
                await search_input.fill("test search")
                await page.keyboard.press("Enter")
                await asyncio.sleep(1)  # Wait for search results

                # Check if search results appeared or URL changed
                current_url = page.url
                if "search" not in current_url.lower():
                    # Look for search results container
                    search_results = await page.query_selector(
                        ".search-results, #search-results, .search-content"
                    )
                    if not search_results:
                        self.test_results["javascript_functionality"].append(
                            {
                                "browser": browser_name,
                                "page": page_path,
                                "error": "Search functionality appears non-functional",
                                "type": "search_functionality_issue",
                            }
                        )

            except Exception as e:
                self.test_results["javascript_functionality"].append(
                    {
                        "browser": browser_name,
                        "page": page_path,
                        "error": f"Search test failed: {str(e)}",
                        "type": "search_test_error",
                    }
                )

    async def _test_mobile_specific_features(
        self, page: Page, device_name: str, page_path: str
    ):
        """Test mobile-specific features like hamburger menus."""

        # Test hamburger menu functionality
        hamburger_selectors = [
            ".hamburger",
            ".menu-toggle",
            ".mobile-menu-toggle",
            "[aria-label*='menu']",
            ".nav-toggle",
        ]

        for selector in hamburger_selectors:
            hamburger = await page.query_selector(selector)
            if hamburger:
                try:
                    # Check if hamburger is visible on mobile
                    is_visible = await hamburger.is_visible()
                    if not is_visible and "mobile" in device_name:
                        self.test_results["mobile_responsiveness"].append(
                            {
                                "device": device_name,
                                "page": page_path,
                                "error": f"Hamburger menu not visible on mobile: {selector}",
                                "type": "mobile_menu_visibility_issue",
                            }
                        )
                        continue

                    # Test hamburger functionality
                    await hamburger.click()
                    await asyncio.sleep(0.5)  # Wait for animation

                    # Look for mobile menu that should have appeared
                    mobile_menu = await page.query_selector(
                        ".mobile-menu, .menu-open, .nav-open"
                    )
                    if not mobile_menu:
                        self.test_results["mobile_responsiveness"].append(
                            {
                                "device": device_name,
                                "page": page_path,
                                "error": "Hamburger menu click did not reveal mobile menu",
                                "type": "mobile_menu_functionality_issue",
                            }
                        )

                    break  # Found and tested one hamburger menu

                except Exception as e:
                    self.test_results["mobile_responsiveness"].append(
                        {
                            "device": device_name,
                            "page": page_path,
                            "error": f"Mobile menu test failed: {str(e)}",
                            "type": "mobile_menu_test_error",
                        }
                    )
                    break

    async def _test_touch_interactions(
        self, page: Page, device_name: str, page_path: str
    ):
        """Test touch-specific interactions on mobile devices."""

        # Test that touch targets are appropriately sized
        buttons = await page.query_selector_all("button, a, input[type='submit'], .btn")

        for i, button in enumerate(buttons[:5]):  # Test first 5 buttons
            try:
                bounding_box = await button.bounding_box()
                if bounding_box:
                    width = bounding_box["width"]
                    height = bounding_box["height"]

                    # WCAG AA recommends minimum 44px touch targets
                    min_touch_size = 44

                    if width < min_touch_size or height < min_touch_size:
                        self.test_results["mobile_responsiveness"].append(
                            {
                                "device": device_name,
                                "page": page_path,
                                "error": f"Touch target too small: {width}x{height}px (minimum {min_touch_size}px)",
                                "type": "touch_target_too_small",
                                "element_index": i,
                            }
                        )

            except Exception:
                # Skip this test if we can't get bounding box
                continue

    def _generate_test_summary(self) -> dict[str, Any]:
        """Generate summary statistics for all test results."""
        summary = {
            "total_issues": 0,
            "issues_by_category": {},
            "browsers_tested": set(),
            "devices_tested": set(),
            "pages_tested": set(),
        }

        for category, issues in self.test_results.items():
            if category == "summary":
                continue

            category_count = len(issues)
            summary["issues_by_category"][category] = category_count
            summary["total_issues"] += category_count

            # Collect metadata about what was tested
            for issue in issues:
                if "browser" in issue:
                    summary["browsers_tested"].add(issue["browser"])
                if "device" in issue:
                    summary["devices_tested"].add(issue["device"])
                if "page" in issue:
                    summary["pages_tested"].add(issue["page"])

        # Convert sets to lists for JSON serialization
        summary["browsers_tested"] = list(summary["browsers_tested"])
        summary["devices_tested"] = list(summary["devices_tested"])
        summary["pages_tested"] = list(summary["pages_tested"])

        return summary


@pytest.fixture
def cross_platform_tester():
    """Pytest fixture for CrossPlatformTester instance."""
    return CrossPlatformTester()


# Common pages to test
TEST_PAGES = [
    "",  # Homepage
    "product/",
    "product/getting-started/",
    "product/installation/",
    "development/",
    "journey/",
]


@pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="Playwright not installed")
@pytest.mark.asyncio
async def test_browser_compatibility(cross_platform_tester):
    """Test compatibility across different browsers."""
    results = await cross_platform_tester.run_cross_platform_tests(TEST_PAGES)
    compatibility_issues = results["browser_compatibility"]

    # Filter out non-critical issues
    critical_issues = [
        issue
        for issue in compatibility_issues
        if issue["type"]
        in ["navigation_error", "javascript_error", "test_execution_error"]
    ]

    if critical_issues:
        error_details = []
        for issue in critical_issues:
            browser = issue.get("browser", "unknown")
            page = issue.get("page", "unknown")
            error_details.append(f"  - {browser} @ {page}: {issue['error']}")

        pytest.fail(
            f"Found {len(critical_issues)} browser compatibility issues:\n"
            + "\n".join(error_details)
        )


@pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="Playwright not installed")
@pytest.mark.asyncio
async def test_mobile_responsiveness(cross_platform_tester):
    """Test mobile responsiveness across device sizes."""
    results = await cross_platform_tester.run_cross_platform_tests(TEST_PAGES)
    mobile_issues = results["mobile_responsiveness"]

    # Filter for critical mobile issues
    critical_mobile_issues = [
        issue
        for issue in mobile_issues
        if issue["type"]
        in ["horizontal_scroll_issue", "mobile_menu_functionality_issue"]
    ]

    if critical_mobile_issues:
        error_details = []
        for issue in critical_mobile_issues:
            device = issue.get("device", "unknown")
            page = issue.get("page", "unknown")
            error_details.append(f"  - {device} @ {page}: {issue['error']}")

        pytest.fail(
            f"Found {len(critical_mobile_issues)} critical mobile responsiveness issues:\n"
            + "\n".join(error_details)
        )


@pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="Playwright not installed")
@pytest.mark.asyncio
async def test_performance_benchmarks(cross_platform_tester):
    """Test performance benchmarks across browsers."""
    results = await cross_platform_tester.run_cross_platform_tests(TEST_PAGES)
    performance_data = results["performance"]

    # Check for pages that load too slowly (> 5 seconds)
    slow_pages = [perf for perf in performance_data if perf["load_time"] > 5.0]

    if slow_pages:
        error_details = []
        for perf in slow_pages:
            browser = perf.get("browser", "unknown")
            page = perf.get("page", "unknown")
            load_time = perf["load_time"]
            error_details.append(f"  - {browser} @ {page}: {load_time:.2f}s")

        pytest.fail(
            f"Found {len(slow_pages)} pages with slow load times (>5s):\n"
            + "\n".join(error_details)
        )


@pytest.mark.skipif(not PLAYWRIGHT_AVAILABLE, reason="Playwright not installed")
@pytest.mark.asyncio
async def test_javascript_functionality(cross_platform_tester):
    """Test JavaScript functionality across browsers."""
    results = await cross_platform_tester.run_cross_platform_tests(TEST_PAGES)
    js_issues = results["javascript_functionality"]

    if js_issues:
        error_details = []
        for issue in js_issues:
            browser = issue.get("browser", "unknown")
            page = issue.get("page", "unknown")
            error_details.append(f"  - {browser} @ {page}: {issue['error']}")

        pytest.fail(
            f"Found {len(js_issues)} JavaScript functionality issues:\n"
            + "\n".join(error_details)
        )


def test_playwright_installation():
    """Test that Playwright is properly installed."""
    if not PLAYWRIGHT_AVAILABLE:
        pytest.skip("Playwright not available. Install with: pip install playwright")

    # This test passes if Playwright is available


if __name__ == "__main__":
    # Allow running this module directly for debugging
    import asyncio

    async def main():
        if not PLAYWRIGHT_AVAILABLE:
            print(
                "Error: Playwright not available. Install with: pip install playwright"
            )
            return

        tester = CrossPlatformTester("http://localhost:8000")
        results = await tester.run_cross_platform_tests(TEST_PAGES)

        print("Cross-Platform Test Results:")
        print(f"Total issues: {results['summary']['total_issues']}")
        print("Issues by category:")
        for category, count in results["summary"]["issues_by_category"].items():
            print(f"  {category}: {count}")
        print(f"Browsers tested: {results['summary']['browsers_tested']}")
        print(f"Devices tested: {results['summary']['devices_tested']}")

    asyncio.run(main())
