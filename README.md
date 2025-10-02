# Orangehrm-automation
Automating orangeHRM using python-POM&amp;Data driven(Hybrid framework)
# OrangeHRM Automation Framework 🚀

Hybrid automation framework for [OrangeHRM Demo](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login)  
Built with **Python + Selenium + Pytest + POM + Data-Driven (Excel)**  
Reports: **Allure** + **pytest-html**  
CI/CD: **GitHub Actions**

---

## 📌 Features
- **Selenium + Python** for web UI automation
- **Hybrid Framework**: Page Object Model (POM) + Data Driven (Excel)
- **Pytest Fixtures**: driver setup, base URL, Excel data reader
- **Reporting**:
  - Self-contained HTML report (pytest-html)
  - Allure advanced reporting with screenshots
- **CI/CD Integration**:
  - GitHub Actions workflow on every push/PR
  - Reports uploaded as artifacts
- **Cross-platform**: Works on Mac (M1), Linux, CI runners

---
## 📂 Folder Structure
orangehrm-automation/
│
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions workflow
│
├── requirements.txt               # Project dependencies
├── pytest.ini                     # Pytest configuration
├── conftest.py                    # Fixtures + reporting hooks
│
├── pages/
│   ├── base_page.py               # BasePage abstraction
│   └── login_page.py              # Page Object
│
├── tests/
│   └── test_login.py              # Login test (valid/invalid)
│
├── testdata/
│   └── login_data.xlsx            # Excel test data
│
├── utilities/
│   ├── excel_reader.py            # Excel utility
│   └── driver_factory.py          # Driver management
│
├── reports/
│   ├── allure-results/            # Raw Allure results
│   └── report.html                # pytest-html report
│
└── README.md

## ⚙️ Setup (Local)

### 1️⃣ Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Run Tests (with Reports)

pytest --alluredir=reports/allure-results --html=reports/report.html --self-contained-html -q

4️⃣ Generate Allure Report (HTML)

# Requires Allure CLI installed (brew install allure / scoop install allure)
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

📊 Reports
	•	pytest-html → reports/report.html (open directly in browser)
	•	Allure Report → Rich report with steps, screenshots, logs

Screenshots are captured automatically on each test (pass/fail) and attached to reports.

⸻

🤖 CI/CD with GitHub Actions
	•	Workflow: .github/workflows/ci.yml
	•	Triggers: On push, pull_request, or manual dispatch
	•	Runs on: ubuntu-latest
	•	Steps:
	1.	Checkout repo
	2.	Setup Python 3.11
	3.	Install dependencies
	4.	Install Chromium + Chromedriver
	5.	Run pytest with Allure + HTML reports
	6.	Upload artifacts (pytest-html, allure-results, screenshots)

⸻

📥 Fetch CI Reports
	1.	Go to your repo → Actions tab
	2.	Click latest workflow run → scroll down to Artifacts
	3.	Download:
	•	pytest-html-report → contains report.html (open directly in browser)
	•	allure-results → raw data (use allure generate locally)
	•	screenshots → captured test screenshots

Optional: Auto-generate Allure HTML in CI

Add this snippet to your workflow (ci.yml) after tests:
yaml

- name: Install Allure CLI
  run: |
    sudo apt-get update
    sudo apt-get install -y unzip default-jre
    wget -qO /tmp/allure.zip https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.21.0/allure-commandline-2.21.0.zip
    sudo unzip -o /tmp/allure.zip -d /opt/
    sudo ln -s /opt/allure-2.21.0/bin/allure /usr/local/bin/allure

- name: Generate Allure HTML
  if: always()
  run: |
    allure generate reports/allure-results -o reports/allure-report --clean

- name: Upload Allure HTML
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: allure-html
    path: reports/allure-report

    
    
🛠 Troubleshooting

❌ Error: fixture 'base_url' not found

➡ Add this in conftest.py:
@pytest.fixture(scope="session")
def base_url():
    return "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


❌ Error: SessionNotCreatedException: user data dir already in use

➡ In CI, always use headless Chrome with unique profile:
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

❌ Reports not opening in CI
➡ Download from Actions → Artifacts and open locally.


(Quick Highlights)
	•	Framework Type: Hybrid (POM + Data-driven + Pytest)
	•	Data Handling: Excel (openpyxl) + parametrize
	•	Reporting: Allure (detailed), pytest-html (quick view)
	•	CI: GitHub Actions (pytest → artifacts → download)
	•	Design Pattern: Page Object Model for maintainability
	•	Parallel Runs: pytest-xdist with isolated drivers
	•	Evidence: Screenshots captured via pytest hook, attached to reports


✅ Quick Commands

# Run tests + reports
pytest --alluredir=reports/allure-results --html=reports/report.html --self-contained-html -q

# Generate Allure HTML
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

# Trigger CI manually (no code change)
git commit --allow-empty -m "ci: trigger workflow"
git push origin main


👨‍💻 Author: Anshuman Kumar Ray
📌 Role: SDET | Automation Engineer
📍 Tech: Python · Selenium · Pytest · POM · Allure · GitHub Actions