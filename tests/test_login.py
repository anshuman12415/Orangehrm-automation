import pytest
import allure
from pages.login_page import LoginPage
from utilities.excel_utils import get_data
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DATA = get_data(os.path.join("testdata", "login_data.xlsx"), "Sheet1")


@pytest.mark.parametrize("username,password,expected", DATA)
def test_login(driver, base_url, username, password, expected):
    with allure.step("Open login page"):
        driver.get(base_url)

    login = LoginPage(driver)
    with allure.step("Enter credentials"):
        login.enter_username(username)
        login.enter_password(password)
        login.click_login()

    if expected == "success":
        with allure.step("Verify successful login (dashboard URL)"):
            WebDriverWait(driver, 10).until(
                EC.url_contains("dashboard")
            )
            assert "dashboard" in driver.current_url.lower()
    else:
        with allure.step("Verify error shown"):
            err = login.get_error_message()
            assert "invalid" in err.lower() or err != ""
