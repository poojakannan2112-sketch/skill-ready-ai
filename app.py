from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import re

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Starter dataset for the project demo. Add or update skills/roles as needed.
ROLE_REQUIREMENTS = {
    "Data Analyst": {
        "skills": ["Python", "SQL", "Excel", "Statistics", "Power BI", "Data Visualization"],
        "description": "Turn raw data into reports, dashboards, and business insights.",
        "learning": ["SQL joins and window functions", "Power BI dashboards", "Statistics and hypothesis testing"]
    },
    "Python Developer": {
        "skills": ["Python", "Git", "REST APIs", "SQL", "OOP", "Testing"],
        "description": "Build backend services, automation scripts, and Python applications.",
        "learning": ["Object-oriented Python", "Flask REST APIs", "Unit testing with pytest"]
    },
    "Web Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "Git", "REST APIs", "SQL"],
        "description": "Build responsive web experiences and connect them to backend services.",
        "learning": ["JavaScript DOM and async programming", "Responsive CSS", "REST API integration"]
    },
    "Machine Learning Engineer": {
        "skills": ["Python", "Statistics", "Machine Learning", "SQL", "Data Visualization", "Git"],
        "description": "Prepare data, train models, and evaluate predictive systems.",
        "learning": ["Pandas and NumPy", "Model evaluation", "Scikit-learn pipelines"]
    },
    "Backend Developer": {
        "skills": ["Python", "SQL", "REST APIs", "Git", "OOP", "Testing"],
        "description": "Develop server-side logic, APIs, and database-backed applications.",
        "learning": ["Flask architecture", "Database design", "Authentication and API testing"]
    }
}

SKILL_ALIASES = {
    "python": "Python", "py": "Python",
    "sql": "SQL", "mysql": "SQL", "postgresql": "SQL", "sqlite": "SQL",
    "excel": "Excel", "ms excel": "Excel",
    "statistics": "Statistics", "statistical analysis": "Statistics",
    "power bi": "Power BI", "powerbi": "Power BI",
    "data visualization": "Data Visualization", "visualization": "Data Visualization",
    "html": "HTML", "html5": "HTML",
    "css": "CSS", "css3": "CSS",
    "javascript": "JavaScript", "js": "JavaScript",
    "git": "Git", "github": "Git",
    "rest api": "REST APIs", "rest apis": "REST APIs", "api development": "REST APIs",
    "oop": "OOP", "object oriented programming": "OOP",
    "testing": "Testing", "unit testing": "Testing", "pytest": "Testing",
    "machine learning": "Machine Learning", "ml": "Machine Learning",
    "pandas": "Python", "numpy": "Python", "flask": "REST APIs",
}

ALL_SKILLS = sorted({skill for role in ROLE_REQUIREMENTS.values() for skill in role["skills"]})

def extract_pdf_text(file_storage):
    """Extract text from a PDF resume. Returns an empty string if extraction is unavailable."""
    if not file_storage or not file_storage.filename:
        return ""
    if not file_storage.filename.lower().endswith(".pdf"):
        raise ValueError("Please upload a PDF resume.")
    if fitz is None:
        raise RuntimeError("PDF extraction is unavailable. Install dependencies with: pip install -r requirements.txt")
    safe_name = secure_filename(file_storage.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
    file_storage.save(path)
    try:
        doc = fitz.open(path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

def detect_skills(text):
    """Simple keyword-based extraction suitable for a transparent starter demo."""
    lower = re.sub(r"\s+", " ", text.lower())
    found = set()
    for alias, canonical in SKILL_ALIASES.items():
        # Word boundaries reduce accidental matches inside unrelated words.
        if re.search(r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])", lower):
            found.add(canonical)
    return found

def evaluate_roles(candidate_skills, experience_years=0):
    results = []
    for role, info in ROLE_REQUIREMENTS.items():
        required = info["skills"]
        matched = [skill for skill in required if skill in candidate_skills]
        missing = [skill for skill in required if skill not in candidate_skills]
        score = round((len(matched) / len(required)) * 100) if required else 0
        # Experience is displayed as context, not used to inflate the skill-match score.
        results.append({
            "name": role,
            "description": info["description"],
            "score": score,
            "matched": matched,
            "missing": missing,
            "learning": info["learning"],
            "required_count": len(required)
        })
    return sorted(results, key=lambda item: (-item["score"], item["name"]))

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        try:
            uploaded_file = request.files.get("resume")
            resume_text = extract_pdf_text(uploaded_file) if uploaded_file and uploaded_file.filename else ""
            selected = set(request.form.getlist("skills"))
            typed_skills = request.form.get("extra_skills", "")
            typed = detect_skills(typed_skills)
            extracted = detect_skills(resume_text)
            candidate_skills = selected | typed | extracted
            if not candidate_skills:
                error = "Select at least one skill, enter skills, or upload a text-based PDF resume."
            else:
                try:
                    experience = max(0, min(50, int(request.form.get("experience", "0"))))
                except ValueError:
                    experience = 0
                roles = evaluate_roles(candidate_skills, experience)
                top = roles[0]
                all_required = sorted({s for r in ROLE_REQUIREMENTS.values() for s in r["skills"]})
                result = {
                    "skills": sorted(candidate_skills),
                    "extracted": sorted(extracted),
                    "experience": experience,
                    "roles": roles,
                    "top_role": top,
                    "overall": round(sum(r["score"] for r in roles) / len(roles)),
                    "all_required": all_required,
                    "skill_labels": [r["name"] for r in roles],
                    "skill_scores": [r["score"] for r in roles]
                }
        except (ValueError, RuntimeError) as exc:
            error = str(exc)
    return render_template("index.html", all_skills=ALL_SKILLS, result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
