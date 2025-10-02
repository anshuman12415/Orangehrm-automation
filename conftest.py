# conftest.py
import os
import time
import tempfile
import shutil
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Optional: pytest-html extras for embedding images
try:
    from pytest_html import extras as html_extras
except Exception:
    html_extras = None


@pytest.fixture(scope="session")
def base_url():
    return "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


@pytest.fixture(scope="function")
def driver():
    """
    Creates ChromeDriver with a unique temporary user-data-dir per test,
    and CI-safe Chrome options. Cleans up the temp directory afterwards.
    """
    tmp_profile_dir = tempfile.mkdtemp(prefix="chrome-profile-")
    options = Options()

    # Decide headless mode based on environment: run headless in CI automatically
    is_ci = bool(os.getenv("CI", "").lower() in ("1", "true", "yes"))
    if is_ci:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
    else:
        # local debugging: leave headless commented so devs can watch browser
        # options.add_argument("--headless=new")
        pass

    # Common options
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    # sometimes needed for latest Chrome
    options.add_argument("--remote-allow-origins=*")
    # IMPORTANT: unique user-data directory avoids "already in use" in CI
    options.add_argument(f"--user-data-dir={tmp_profile_dir}")

    svc = Service(ChromeDriverManager().install())
    driver = None
    try:
        driver = webdriver.Chrome(service=svc, options=options)
        driver.implicitly_wait(10)
        yield driver
    finally:
        # quit driver first
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
        # then remove temporary profile directory
        try:
            shutil.rmtree(tmp_profile_dir, ignore_errors=True)
        except Exception:
            pass


# Hook wrapper: run after each test phase to capture the test report
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    This hook runs after each test call. We capture screenshot for the 'call' phase
    regardless of pass/fail and attach to Allure and pytest-html (if available).
    """
    outcome = yield
    rep = outcome.get_result()

    # Only create screenshots for the 'call' phase (actual test body)
    if rep.when == "call":
        driver = item.funcargs.get("driver")
        if not driver:
            return

        # Build screenshots directory and file name
        screenshots_dir = os.path.join("reports", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        # Use timestamp to avoid collisions, include status in name
        status = "PASSED" if rep.passed else "FAILED" if rep.failed else str(
            rep.outcome).upper()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"{item.name}__{status}__{timestamp}.png"
        path = os.path.join(screenshots_dir, file_name)

        # Try saving screenshot (don't crash test run on error)
        try:
            driver.save_screenshot(path)
        except Exception as e:
            print(f"[conftest] Warning - could not save screenshot: {e}")
            path = None

        # Attach to Allure if available and file exists
        if path and os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    allure.attach(f.read(), name=file_name,
                                  attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(f"[conftest] Warning - could not attach to Allure: {e}")

        # Attach to pytest-html if plugin available
        if html_extras and path and os.path.exists(path):
            try:
                extra = getattr(rep, "extra", [])
                extra.append(html_extras.image(path))
                rep.extra = extra
            except Exception as e:
                print(
                    f"[conftest] Warning - could not attach to pytest-html: {e}")
