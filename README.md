# SkillReady AI — Job Readiness & Skill Gap Analyzer

A student project prototype for **AI-Based Dynamic Skill Relevance and Job Readiness Prediction**. It lets a candidate select skills or upload a text-based PDF resume, compares those skills with a small role-requirement dataset, calculates skill-match scores, highlights gaps, and suggests learning priorities.

## Features

- Responsive dashboard UI
- PDF resume text extraction with PyMuPDF
- Keyword-based skill detection
- Role matching for Data Analyst, Python Developer, Web Developer, Machine Learning Engineer, and Backend Developer
- Missing-skill and learning-priority recommendations
- Chart.js role comparison chart
- Flask backend and local role dataset

## Important project scope

This is a **working prototype**, not a trained machine-learning model. The readiness score is a transparent skill coverage percentage calculated as:

`matched required skills / total required skills × 100`

The included role requirements are sample data, not live job-market data. Resume extraction works best with text-based PDFs; scanned image PDFs need OCR, which is not included. Do not use this prototype as the sole basis for hiring decisions.

## Run locally in VS Code

### 1. Install prerequisites
- Python 3.10 or newer
- Git
- Visual Studio Code (Python extension recommended)

Check Python and Git:
```bash
python --version
git --version
```

### 2. Open the project
Extract the ZIP, then open the `skillreadiness_ai` folder in VS Code.

### 3. Create and activate a virtual environment

**Windows PowerShell**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Start the website
```bash
python app.py
```

Open the local URL shown in the terminal, usually http://127.0.0.1:5000.

Press `Ctrl+C` in the terminal to stop the server.

## Push the project to GitHub

Create a **new empty repository** on GitHub (do not initialize it with a README if you plan to use the commands below). In the VS Code terminal, from the project folder:

```bash
git init
git add .
git commit -m "Build SkillReady AI job readiness prototype"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the example repository URL with your actual GitHub repository URL. GitHub may ask you to sign in through your browser.

For later updates:
```bash
git add .
git commit -m "Describe your update"
git push
```

## Suggested next improvements

1. Replace sample job requirements with a maintained dataset or a real job API.
2. Add OCR support for scanned resumes.
3. Train and evaluate a real ML model using a documented dataset.
4. Add user accounts and a database only if needed.
5. Add tests, input validation, and privacy controls before public deployment.
