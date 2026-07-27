# FastAPI Security Service & Ansible Deployment Pipeline

An automated, security-first deployment pipeline for a Python FastAPI web service. Built using Ansible to automate virtual environment configuration, static security scanning, unit testing, and background service execution.

## 🚀 Features
* **FastAPI Service:** Lightweight Python web framework.
* **Automated Security Scanning:** Runs `bandit` to check for security vulnerabilities prior to launch.
* **Unit Testing:** Runs test suites with `pytest` to prevent regressions.
* **Infrastructure Automation:** Ansible playbook (`deploy.yml`) handles setup, test execution, process lifecycle, and live endpoint verification.

## 🛠️ Requirements
* Python 3.10+
* Ansible

## 💻 Quick Start
To trigger the automated deployment pipeline:

```bash
ansible-playbook deploy.yml