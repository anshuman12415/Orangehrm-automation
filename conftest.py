# conftest.py
import tempfile
import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    """
    Creates a Chrome WebDriver with a unique temporary user-data-dir
    so CI (and parallel tests) won't clash.

    Cleans up the temp dir at the end.
    """
    tmp_profile = tempfile.mkdtemp(prefix="chrome-profile-")
    options = Options()

    # CI-friendly options:
    options.add_argument("--headless=new")                # run headless in CI
    # required for many linux CI runners
    options.add_argument("--no-sandbox")
    # avoid /dev/shm issues
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")                 # generally safe
    options.add_argument("--disable-extensions")
    # sometimes required for newest chrome
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("--window-size=1920,1080")

    # VERY IMPORTANT: give Chrome a unique user-data-dir to avoid "already in use"
    options.add_argument(f"--user-data-dir={tmp_profile}")
    # Optional: choose a unique profile directory inside that user-data-dir
    # options.add_argument(f"--profile-directory=Profile_{os.getpid()}")

    svc = Service(ChromeDriverManager().install())

    driver = None
    try:
        driver = webdriver.Chrome(service=svc, options=options)
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
            shutil.rmtree(tmp_profile, ignore_errors=True)
        except Exception:
            pass
