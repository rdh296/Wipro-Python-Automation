# Self-Healing Selenium Automation Framework

A scalable **Selenium Python Automation Framework** built using **PyTest, Unittest, Page Object Model (POM), YAML Configuration, CSV Test Data, HTML Reporting, and Self-Healing Locators**.

This framework automates the **Login** and **Product Search** functionalities of the TutorialsNinja e-commerce application while demonstrating advanced automation concepts such as **automatic locator recovery, failure analytics, screenshots, logging, retries, and HTML reporting**.

---

# Project Overview

Traditional Selenium automation frameworks fail immediately when a web element's locator changes.

This framework introduces a **Self-Healing Locator Engine** that:

* Detects failed locators
* Tries predefined fallback locators automatically
* Continues execution when recovery succeeds
* Records locator recovery events
* Displays locator health in the HTML report

### Self-Healing Workflow

```text
Primary Locator
      │
      ▼
Element Not Found
      │
      ▼
Self-Healing Engine
      │
      ▼
Fallback Locator
      │
      ▼
Element Found
      │
      ▼
Test Continues
```

---

# Features

## Core Automation

* Selenium WebDriver
* PyTest Test Execution
* Unittest Support
* Page Object Model (POM)
* Driver Factory Pattern
* Explicit Waits

## Configuration Management

* YAML-based Configuration
* Browser Configuration
* Environment Settings

## Test Data Management

* CSV Test Data
* External Data Handling

## Reporting & Evidence

* HTML Report
* Screenshot on Failure
* Execution Logs

## Advanced Framework Features

* Self-Healing Locators
* Locator Health Tracking
* Fallback Locator Recovery
* Automatic Retry Mechanism
* Failure Intelligence Reporting

---

# Project Structure

```text
Capstone Project/
│
├── config/
│   └── config.yaml
│
├── data/
│   └── login_data.csv
│
├── framework/
│   ├── driver_factory.py
│   ├── locator_healer.py
│   └── logger.py
│
├── logs/
│   └── test.log
│
├── pages/
│   ├── base_page.py
│   ├── base_login_page.py
│   ├── base_search_page.py
│   │
│   └── tutorials_ninja/
│       ├── login_page.py
│       └── search_page.py
│
├── reports/
│   └── report.html
│
├── screenshots/
│
├── tests/
│   ├── test_login.py
│   ├── test_search.py
│   └── test_self_healing.py
│
├── utils/
│   ├── csv_reader.py
│   └── screenshot.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# Technology Stack

| Technology           | Purpose                  |
| -------------------- | ------------------------ |
| Python               | Programming Language     |
| Selenium             | Browser Automation       |
| PyTest               | Test Framework           |
| Unittest             | Additional Test Support  |
| PyYAML               | Configuration Management |
| CSV                  | Test Data Handling       |
| pytest-html          | HTML Reports             |
| pytest-rerunfailures | Retry Failed Tests       |

---

# Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
```

### Step 2: Navigate to the Project

```bash
cd "Capstone Project"
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Edit the configuration file:

```text
config/config.yaml
```

Example:

```yaml
app:
  name: tutorials_ninja
  url: https://tutorialsninja.com/demo/

browser:
  name: chrome
  headless: false
  implicit_wait: 5
  page_load_timeout: 30
```

---

# Test Data

Login credentials are stored in:

```text
data/login_data.csv
```

Example:

```csv
username,password
example@gmail.com,password123
```

---

# Running Tests

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v -s
```

Run Login test:

```bash
pytest tests/test_login.py -v -s
```

Run Product Search test:

```bash
pytest tests/test_search.py -v -s
```

Run the Self-Healing demonstration:

```bash
pytest tests/test_self_healing.py -v -s
```

---

# Self-Healing Locator Engine

The framework contains a **Locator Healer** located at:

```text
framework/locator_healer.py
```

Instead of failing immediately:

```text
ID = input-email
      │
      ▼
Element Not Found
      │
      ▼
Test Failed
```

The framework performs:

```text
Primary Locator
      │
      ▼
Failed
      │
      ▼
Fallback Locator 1
      │
      ▼
Fallback Locator 2
      │
      ▼
Element Found
      │
      ▼
Test Continues
```

### Locator States

| Status     | Meaning                                                    |
| ---------- | ---------------------------------------------------------- |
| **STABLE** | Primary locator worked successfully                        |
| **HEALED** | A fallback locator successfully recovered the element      |
| **FAILED** | Primary and fallback locators could not locate the element |

---

# HTML Reporting

After execution:

```text
reports/report.html
```

The report contains:

* Test Result
* Locator Health
* Locator Recovery Details
* Retry Count
* Screenshot on Failure
* Execution Summary

Example:

```text
Locator Health : HEALED

Original Locator:
('id','wrong-id')

Recovered Locator:
('id','input-email')

Attempts:
1
```

---

# Logging

Execution logs are stored in:

```text
logs/test.log
```

Example:

```text
2026-09-24 10:30:01 INFO Starting browser
2026-09-24 10:30:03 INFO Opening Login page
2026-09-24 10:30:05 INFO Locator STABLE
2026-09-24 10:30:09 INFO Test Passed
```

---

# Screenshots

Whenever a test fails:

```text
screenshots/
```

stores images such as:

```text
test_login_report.png
```

These screenshots are also attached to the HTML report.

---

# Retry Mechanism

Failed tests are automatically retried.

Configured inside:

```text
pytest.ini
```

Example:

```ini
addopts =
    -v
    --html=reports/report.html
    --self-contained-html
    --reruns 1
```

---

# Page Object Model

The framework follows a layered architecture.

```text
Tests
 │
 ▼
Page Objects
 │
 ▼
Base Pages
 │
 ▼
Locator Healer
 │
 ▼
Selenium WebDriver
```

### Benefits

* Reusable code
* Easy maintenance
* Separation of concerns
* Scalable framework design

---

# Framework Workflow

```text
User Starts Test
       │
       ▼
PyTest
       │
       ▼
Driver Factory
       │
       ▼
Browser Launch
       │
       ▼
Page Objects
       │
       ▼
Locator Healer
       │
       ▼
Web Application
       │
       ▼
Assertions
       │
       ▼
Logs
Screenshots
HTML Report
```

---

# Current Implemented Features

| Feature                 | Status |
| ----------------------- | ------ |
| Selenium                | ✅      |
| PyTest                  | ✅      |
| Unittest                | ✅      |
| Page Object Model       | ✅      |
| Driver Factory          | ✅      |
| YAML Configuration      | ✅      |
| CSV Test Data           | ✅      |
| Login Automation        | ✅      |
| Product Search          | ✅      |
| Self-Healing Locators   | ✅      |
| Locator Health Tracking | ✅      |
| Screenshot on Failure   | ✅      |
| HTML Report             | ✅      |
| Retry Mechanism         | ✅      |
| Logging                 | ✅      |

---

# Future Enhancements

* Multi-browser Parallel Execution
* API Testing Integration
* SQLite Execution History
* GitHub Actions CI/CD
* Slack/Email Notifications
* Visual Regression Testing
* Dashboard Analytics
* Intelligent Locator Suggestions

---

# Capstone Highlights

This project extends a traditional Selenium automation framework by introducing a **Self-Healing Locator Engine** that improves automation resilience when UI locators change.

### Key Contributions

* Self-Healing Locator Recovery
* Locator Health Monitoring
* Intelligent Failure Reporting
* Automatic Screenshot Evidence
* Retry-Based Test Recovery
* Structured Logging
* Scalable Page Object Architecture

The project demonstrates both **software testing best practices** and **maintainable automation framework design**, making it suitable as a professional capstone project.
