from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.username = (By.NAME, "username")
        self.password = (By.NAME, "password")
        self.login_btn = (By.XPATH, "//button[@type='submit']")
        self.error_msg = (By.XPATH, "//p[contains(@class,'oxd-alert')]")

    def enter_username(self, uname):
        el = self.wait.until(EC.visibility_of_element_located(self.username))
        el.clear()
        el.send_keys(uname)

    def enter_password(self, pwd):
        el = self.wait.until(EC.visibility_of_element_located(self.password))
        el.clear()
        el.send_keys(pwd)

    def click_login(self):
        self.driver.find_element(*self.login_btn).click()

    def get_error_message(self):
        try:
            return self.wait.until(EC.visibility_of_element_located(self.error_msg)).text
        except:
            return ""  # No error message found
