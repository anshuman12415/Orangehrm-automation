# 🟠 OrangeHRM Automation Framework 🚀

Automating [OrangeHRM Demo](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login)  
Built with **Python + Selenium + Pytest + POM + Data-Driven (Hybrid Framework)**  
Reports: **Allure** + **pytest-html**  
CI/CD: **GitHub Actions**

---

## 📌 Features
- 🖥️ **Selenium + Python** for Web UI automation  
- 🏗 **Hybrid Framework**: Page Object Model (POM) + Data Driven (Excel)  
- ⚡ **Pytest Fixtures** for driver setup, base URL, and test data  
- 📊 **Reporting**:
  - Self-contained HTML report (**pytest-html**)  
  - Advanced reports with screenshots (**Allure**)  
- 🔄 **CI/CD Integration**:
  - GitHub Actions workflow (runs on push/PR)  
  - Test reports uploaded as artifacts  
- 🌍 **Cross-platform**: Mac (M1), Linux, Windows, CI runners  

---

## 📂 Folder Structure

```bash
orangehrm-automation/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions workflow
│
├── requirements.txt             # Dependencies
├── pytest.ini                   # Pytest config
├── conftest.py                  # Fixtures + reporting hooks
│
├── pages/
│   ├── base_page.py             # BasePage abstraction
│   └── login_page.py            # Page Object
│
├── tests/
│   └── test_login.py            # Login tests
│
├── testdata/
│   └── login_data.xlsx          # Excel test data
│
├── utilities/
│   ├── excel_reader.py          # Excel utility
│   └── driver_factory.py        # Driver manager
│
├── reports/
│   ├── allure-results/          # Raw Allure results
│   └── report.html              # pytest-html report
│
└── README.md

⚙️ Local Setup
1️⃣ Create Virtual Environment
python3 -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run Tests (with Reports)
pytest --alluredir=reports/allure-results --html=reports/report.html --self-contained-html -q
4️⃣ Generate Allure Report
# Install Allure CLI first
brew install allure      # Mac
scoop install allure     # Windows

# Generate + open report
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

📊 Reports
	•	📝 pytest-html → reports/report.html (open in browser)
	•	📸 Allure Report → Interactive UI with steps, logs, screenshots
	•	✅ Screenshots automatically captured and attached to reports

🤖 CI/CD with GitHub Actions
	•	Workflow: .github/workflows/ci.yml
	•	Triggers: on push, pull_request, or manual run
	•	Runs on: ubuntu-latest

Steps executed in CI:
	1.	Checkout repo
	2.	Setup Python 3.11
	3.	Install dependencies
	4.	Install Chromium + Chromedriver
	5.	Run pytest (Allure + HTML reports)
	6.	Upload artifacts (reports, screenshots)

📥 Download Test Reports from GitHub Actions
	1.	Go to Actions tab in GitHub repo
	2.	Select a workflow run
	3.	Scroll to Artifacts section
	4.	Download:
	•	pytest-html-report → open report.html
	•	allure-results → generate locally with:
												allure serve allure-results
	•	screenshots → test evidence

🛠 Troubleshooting

❌ fixture ‘base_url’ not found
➡ Add this in conftest.py:
@pytest.fixture(scope="session")
def base_url():
    return "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
❌ SessionNotCreatedException: user data dir already in use
➡ Use these Chrome options in CI:
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

❌ Reports not opening in CI
➡ Download artifacts → open locally

🛑 Git Ignore Rules
# Python cache
__pycache__/
*.pyc

# Virtual environments
.venv/
env/

# Reports and test outputs
reports/
*.html
*.xml

# IDE / Editor files
.vscode/
.idea/

✅ Quick Commands
# Run tests + reports
pytest --alluredir=reports/allure-results --html=reports/report.html --self-contained-html -q

# Generate Allure HTML
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

# Trigger CI manually
git commit --allow-empty -m "ci: trigger workflow"
git push origin main



👨‍💻 Author

Anshuman
📌 Role: SDET | Automation Engineer
📍 Tech: Python · Selenium · Pytest · POM · Allure · GitHub Actions
