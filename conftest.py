import os
import time
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
    options = Options()
    # options.add_argument("--headless=new")    # uncomment for headless runs
    options.add_argument("--window-size=1920,1080")
    # optional: avoid GPU sandbox issues on some Mac setups
    # options.add_argument("--disable-gpu")
    svc = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=svc, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

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
        status = "PASSED" if rep.passed else "FAILED" if rep.failed else rep.outcome.upper()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"{item.name}__{status}__{timestamp}.png"
        path = os.path.join(screenshots_dir, file_name)

        # Try saving screenshot (don't crash test run on error)
        try:
            driver.save_screenshot(path)
        except Exception as e:
            # If screenshot fails, log but continue
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
