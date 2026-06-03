import argparse

import pytest
import allure
from pathlib import Path
from playwright.sync_api import Error as PlaywrightError, sync_playwright


DEFAULT_CONFIG = {
    "browser": "chromium",
    "headed": True,
    "base_url": "https://tutorialsninja.com/demo/",
    "video": "retain-on-failure",
    "screenshot": "only-on-failure",
    "tracing": "retain-on-failure",
}

# ========================================================================
# PYTEST + PLAYWRIGHT TEST CONFIGURATION FILE
# ========================================================================
# This file provides:
# 1. Command-line options (browser, base URL, video, screenshots, etc.)
# 2. Hooks to track test results
# 3. Fixtures for browser setup and teardown
# 4. Screenshot, video, and trace attachments to Allure reports
# ========================================================================


# ----------------------------------------------------------------------------
# STEP 1: ADD COMMAND LINE OPTIONS
# ----------------------------------------------------------------------------
def pytest_addoption(parser):
    """
    Adds command line options for test configuration.
    You can override these when running pytest or store defaults in pytest.ini.
    """



    def safe_addoption(*args, **kwargs):
        try:
            parser.addoption(*args, **kwargs)
        except (argparse.ArgumentError, ValueError):
            # pytest-playwright may already provide these command line options.
            pass

    safe_addoption("--browser", default=DEFAULT_CONFIG["browser"], help="Browser to run: chromium, firefox, webkit")
    safe_addoption("--headed", action="store_true", default=DEFAULT_CONFIG["headed"], help="Run browser in headed mode")
    safe_addoption("--headless", action="store_false", dest="headed", help="Run browser in headless mode")
    safe_addoption("--base-url", default=DEFAULT_CONFIG["base_url"], help="Application base URL")
    safe_addoption("--video", default=DEFAULT_CONFIG["video"], help="Record video: on, off, retain-on-failure")
    safe_addoption("--screenshot", default=DEFAULT_CONFIG["screenshot"], help="Take screenshot: on, off, only-on-failure")
    safe_addoption("--tracing", default=DEFAULT_CONFIG["tracing"], help="Tracing: on, off, retain-on-failure")


# ----------------------------------------------------------------------------
# STEP 2: GET CONFIGURATION VALUE (CMDLINE OR pytest.ini)
# ----------------------------------------------------------------------------
def get_config_value(config, option_name):
    """
    Helper to read configuration values.
    Tries to get from command line first, otherwise from pytest.ini.
    Supports both string and boolean options.
    """
    # Try command-line first
    cmd_value = config.getoption(option_name, default=None)
    if cmd_value is not None:
        return cmd_value

    # Fallback to pytest.ini
    try:
        ini_value = config.getini(option_name)
        if option_name == "headed":
            return ini_value.lower() == "true" if isinstance(ini_value, str) else ini_value
        return ini_value
    except ValueError:
        return DEFAULT_CONFIG[option_name]


# ----------------------------------------------------------------------------
# STEP 3: HOOK TO TRACK TEST RESULTS (PASS/FAIL)
# ----------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Captures the test result (pass/fail/skip) after each test.
    This is used later to decide whether to take screenshots or save traces.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


# ----------------------------------------------------------------------------
# STEP 4: FIXTURE 1 - BROWSER CONTEXT SETUP
# ----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def browser_context(request):
    """
    Creates and manages the Playwright browser context.
    - Reads configuration (browser, headed mode, video settings)
    - Starts the Playwright browser
    - Enables video recording if configured
    - Cleans up automatically after each test
    """
    # Read configuration values
    browser_name = get_config_value(request.config, "browser")
    headed_flag = get_config_value(request.config, "headed")
    video_option = get_config_value(request.config, "video")
    reports_dir = Path(request.config.rootpath) / "reports"
    videos_dir = reports_dir / "videos"
    if isinstance(browser_name, list):
        browser_name = browser_name[0]

    print(f"[OK] Starting browser: {browser_name}")
    print(f"[OK] Headless mode: {not headed_flag} (headed={headed_flag})")

    # Start Playwright
    playwright = sync_playwright().start()

    # Launch the specified browser
    if browser_name.lower() == "chromium":
        browser = playwright.chromium.launch(headless=not headed_flag)
    elif browser_name.lower() == "firefox":
        browser = playwright.firefox.launch(headless=not headed_flag)
    elif browser_name.lower() == "webkit":
        browser = playwright.webkit.launch(headless=not headed_flag)
    else:
        raise ValueError(f"[FAIL] Unsupported browser: {browser_name}")

    # Create a browser context (optionally with video recording)
    if video_option in ["on", "retain-on-failure"]:
        videos_dir.mkdir(parents=True, exist_ok=True)
        context = browser.new_context(record_video_dir=str(videos_dir))
    else:
        context = browser.new_context()

    # Yield the context for use in tests
    yield context

    # Clean up after the test
    print("[CLEANUP] Closing browser context and stopping Playwright...")
    context.close()
    browser.close()
    playwright.stop()


# ----------------------------------------------------------------------------
# STEP 5: FIXTURE 2 - PAGE CREATION AND TEST ARTIFACT MANAGEMENT
# ----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def page(request, browser_context):
    """
    Creates a new browser page for each test.
    - Navigates to the base URL
    - Starts tracing (if enabled)
    - Captures screenshots, traces, and videos for failed tests
    - Attaches all artifacts to Allure report
    """
    # Read test configuration
    base_url = get_config_value(request.config, "base_url")
    screenshot_option = get_config_value(request.config, "screenshot")
    tracing_option = get_config_value(request.config, "tracing")
    video_option = get_config_value(request.config, "video")
    reports_dir = Path(request.config.rootpath) / "reports"
    screenshots_dir = reports_dir / "screenshots"
    traces_dir = reports_dir / "traces"

    print(f"[INFO] Navigating to: {base_url}")

    # Start tracing if enabled
    if tracing_option in ["on", "retain-on-failure"]:
        print("[TRACE] Tracing enabled - capturing screenshots and actions")
        browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    # Create and navigate to base URL
    page = browser_context.new_page()
    page.goto(base_url)

    # Yield the page to the test
    yield page

    # ------------------------------------------------------------------------
    # After the test: manage artifacts (screenshots, videos, traces)
    # ------------------------------------------------------------------------
    test_name = request.node.name
    test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    print(f"[RESULT] Test '{test_name}' result: {'[FAIL]' if test_failed else '[PASS]'}")

    # Save and attach trace
    if tracing_option in ["on", "retain-on-failure"]:
        traces_dir.mkdir(parents=True, exist_ok=True)
        trace_path = traces_dir / f"{test_name}_trace.zip"
        browser_context.tracing.stop(path=str(trace_path))
        print(f"[SAVE] Trace saved: {trace_path}")

        # Attach trace to Allure report if test failed
        # Currently ZIP file is not supported to attach in Allure reports
        # if test_failed:
        #     allure.attach.file(
        #         trace_path,
        #         name=f"{test_name}_trace",
        #         attachment_type=allure.attachment_type.ZIP
        #     )
        #     print("[ATTACH] Trace attached to Allure report")

    # Take screenshot if test failed
    if test_failed and screenshot_option in ["on", "only-on-failure"]:
        screenshot_path = screenshots_dir / f"{test_name}.png"
        try:
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path))
            print(f"[SAVE] Screenshot saved: {screenshot_path}")

            # Attach to Allure report
            allure.attach.file(
                str(screenshot_path),
                name=f"{test_name}_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            print("[ATTACH] Screenshot attached to Allure report")
        except PlaywrightError as e:
            print(f"[WARN] Screenshot skipped: {e}")

    # Attach video if available and test failed
    if test_failed and video_option in ["on", "retain-on-failure"]:
        video_path = page.video.path() if page.video else None
        if video_path and Path(video_path).exists():
            allure.attach.file(
                video_path,
                name=f"{test_name}_video",
                attachment_type=allure.attachment_type.WEBM
            )
            print("[ATTACH] Video attached to Allure report")
