# SkillMatch AI — Resume & Skill Gap Matcher

> **SDG 4: Quality Education** | **SDG 8: Decent Work & Economic Growth**

An AI/ML web application that parses your resume, extracts skills using NLP, compares them against a job description, and generates a personalized learning roadmap to close the skill gap.

---

## Features

| Feature | Description |
|---|---|
| **Skill Extraction** | NLP-based phrase matching across 500+ skills in 8 domains |
| **Match Scoring** | Weighted match score (0–100%) |
| **Gap Analysis** | Priority-ranked missing skills (HIGH / MEDIUM / LOW) |
| **Learning Roadmap** | Week-by-week plan with free resources (Coursera, edX, etc.) |
| **File Upload** | Drag & drop `.txt` resume upload |
| **8 Domains** | Data Science, Web Dev, DevOps, Cybersecurity, Product, UX, Mobile, Embedded |

---

## Tech Stack

- **Backend**: Python 3.13 · Flask 3.x · Regex NLP
- **Frontend**: Vanilla HTML5 · CSS3 · JavaScript (ES2022)
- **Fonts**: Inter (Google Fonts)
- **No external ML dependencies** — pure Python NLP using curated skill taxonomy

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
python app.py

# 3. Open in browser
# http://127.0.0.1:5000
```

---

## Project Structure

```
ai-resume-matcher/
├── app.py                  # Flask backend — skill extraction, gap analysis
├── requirements.txt
├── templates/
│   └── index.html          # Single-page frontend
├── static/
│   ├── css/style.css       # Full responsive UI styles
│   └── js/app.js           # Frontend logic (tabs, upload, fetch, render)
└── uploads/                # Temp upload directory
```

---

## API

### `POST /analyze`

**Request body:**
```json
{
  "resume":    "Your resume text...",
  "job_desc":  "Job description text...",
  "role":      "data_science",
  "exp_level": "mid"
}
```

**Response:**
```json
{
  "match_score": 57,
  "matched_skills": [{ "name": "python", "score": 80 }],
  "missing_skills": [{ "name": "pytorch", "importance": 70 }],
  "extra_skills":   [{ "name": "django" }],
  "skill_gaps": [{
    "skill": "pytorch", "priority": "high",
    "gap_percent": 70, "description": "..."
  }],
  "roadmap": [{
    "skill": "pytorch", "timeline": "Week 1–2",
    "description": "...",
    "resources": [{ "name": "PyTorch Tutorials", "url": "..." }]
  }]
}
```

**Available `role` values:** `data_science` · `web_dev` · `devops` · `cybersecurity` · `product` · `design` · `mobile` · `embedded`

---

## SDG Alignment

- **SDG 4 – Quality Education**: Connects learners to free courses (Coursera, edX, HuggingFace, Khan Academy) based on personalized gap analysis.
- **SDG 8 – Decent Work & Economic Growth**: Reduces skill mismatch in labor markets, improving employment outcomes and economic inclusion.
