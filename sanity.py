from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# optional: create ChromeOptions if you need headless etc.
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")    # uncomment to run headless
# options.add_argument("--disable-gpu")     # optional

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
print("Title:", driver.title)
driver.quit()
