import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def base_url():
    return "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


@pytest.fixture(scope="function")
def driver():
    options = Options()
    # options.add_argument("--headless=new")   # uncomment if you want headless
    options.add_argument("--window-size=1920,1080")
    svc = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=svc, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # hook to take screenshot on failure and attach to allure
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshots_dir = os.path.join("reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            file_name = f"{item.name}.png"
            path = os.path.join(screenshots_dir, file_name)
            driver.save_screenshot(path)
            with open(path, "rb") as f:
                allure.attach(f.read(), name=file_name,
                              attachment_type=allure.attachment_type.PNG)
