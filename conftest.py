# conftest.py
import os
import shutil
import tempfile
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the AUT."""
    return "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


@pytest.fixture(scope="session")
def login_data():
    """
    Reads resources/login_data.xlsx and returns list of dicts:
    [{'username': 'Admin', 'password': 'admin123', 'expected': 'success'}, ...]
    """
    path = os.path.join(os.path.dirname(__file__),
                        "resources", "login_data.xlsx")
    if not os.path.exists(path):
        # fallback inline data to avoid failing if Excel not present
        return [
            {"username": "Admin", "password": "admin123", "expected": "success"},
            {"username": "Admin", "password": "wrongpass", "expected": "failure"},
        ]
    df = pd.read_excel(path)
    return df.to_dict(orient="records")


@pytest.fixture(scope="function")
def driver():
    """
    Creates a Chrome WebDriver with a unique temporary user-data-dir
    so CI (and parallel tests) won't clash. Cleans up after use.
    """
    tmp_profile = tempfile.mkdtemp(prefix="chrome-profile-")
    options = Options()
    # CI/local friendly options:
    # comment-out for visual debugging locally
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("--window-size=1920,1080")
    # unique user-data-dir avoids "already in use" error
    options.add_argument(f"--user-data-dir={tmp_profile}")

    svc = Service(ChromeDriverManager().install())

    driver = None
    try:
        driver = webdriver.Chrome(service=svc, options=options)
        yield driver
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
        try:
            shutil.rmtree(tmp_profile, ignore_errors=True)
        except Exception:
            pass
