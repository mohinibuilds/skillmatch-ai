"""
SkillMatch AI – Flask Backend
AI Resume & Skill Gap Matcher
SDG 4: Quality Education | SDG 8: Decent Work & Economic Growth
"""

import re
import json
import os
from flask import Flask, render_template, request, jsonify

import sys
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB


# ─────────────────────────────────────────────────────────
# SKILL TAXONOMY
# A curated, domain-mapped skill library used for matching.
# ─────────────────────────────────────────────────────────
SKILL_TAXONOMY = {
    # ── Data Science / ML ────────────────────────────────
    "data_science": [
        "python", "r", "sql", "pandas", "numpy", "matplotlib", "seaborn",
        "scikit-learn", "sklearn", "machine learning", "deep learning",
        "tensorflow", "keras", "pytorch", "xgboost", "lightgbm",
        "natural language processing", "nlp", "bert", "gpt", "transformers",
        "computer vision", "opencv", "statistics", "probability",
        "data analysis", "data visualization", "tableau", "power bi",
        "feature engineering", "model deployment", "mlops", "airflow",
        "spark", "hadoop", "data wrangling", "etl", "a/b testing",
        "regression", "classification", "clustering", "neural networks",
        "aws sagemaker", "gcp vertex ai", "azure ml", "jupyter", "colab",
        "data pipeline", "recommendation systems", "time series",
    ],
    # ── Web Development ──────────────────────────────────
    "web_dev": [
        "html", "css", "javascript", "typescript", "react", "vue", "angular",
        "node.js", "nodejs", "express", "django", "flask", "fastapi",
        "rest api", "graphql", "websocket", "next.js", "nuxt", "redux",
        "git", "github", "docker", "ci/cd", "webpack", "vite",
        "tailwind css", "bootstrap", "sass", "postgresql", "mysql",
        "mongodb", "redis", "nginx", "linux", "aws", "gcp", "azure",
        "microservices", "oauth", "jwt", "testing", "jest", "pytest",
        "responsive design", "ux", "accessibility",
    ],
    # ── DevOps / Cloud ───────────────────────────────────
    "devops": [
        "docker", "kubernetes", "k8s", "terraform", "ansible", "jenkins",
        "github actions", "ci/cd", "aws", "gcp", "azure", "linux", "bash",
        "shell scripting", "python", "monitoring", "prometheus", "grafana",
        "nginx", "helm", "argocd", "vault", "networking", "vpc",
        "load balancing", "auto scaling", "elasticsearch", "logstash",
        "kibana", "elk", "cloudformation", "infrastructure as code",
        "site reliability", "sre", "on-call", "incident management",
    ],
    # ── Cybersecurity ────────────────────────────────────
    "cybersecurity": [
        "network security", "penetration testing", "ethical hacking",
        "siem", "soc", "firewalls", "ids/ips", "vulnerability assessment",
        "cryptography", "ssl/tls", "zero trust", "iam", "sso", "oauth",
        "python", "linux", "bash", "wireshark", "metasploit", "burp suite",
        "owasp", "iso 27001", "nist", "gdpr", "compliance", "incident response",
        "threat intelligence", "reverse engineering", "malware analysis",
    ],
    # ── Product Management ───────────────────────────────
    "product": [
        "product roadmap", "agile", "scrum", "kanban", "jira",
        "user research", "ux", "a/b testing", "data analysis",
        "market research", "competitive analysis", "kpis", "okrs",
        "stakeholder management", "communication", "prioritization",
        "wireframing", "figma", "go-to-market", "sql", "tableau",
        "product strategy", "mvp", "user stories", "backlog",
    ],
    # ── UI/UX Design ─────────────────────────────────────
    "design": [
        "figma", "sketch", "adobe xd", "photoshop", "illustrator",
        "user research", "wireframing", "prototyping", "usability testing",
        "design systems", "typography", "color theory", "accessibility",
        "responsive design", "interaction design", "ux writing",
        "html", "css", "javascript", "animation", "after effects",
    ],
    # ── Mobile Development ───────────────────────────────
    "mobile": [
        "swift", "objective-c", "kotlin", "java", "flutter", "dart",
        "react native", "android", "ios", "xcode", "android studio",
        "firebase", "rest api", "sqlite", "realm", "jetpack compose",
        "swiftui", "mobile testing", "app store", "play store", "ci/cd",
    ],
    # ── Embedded / IoT ───────────────────────────────────
    "embedded": [
        "c", "c++", "embedded c", "assembly", "rtos", "freertos",
        "arduino", "raspberry pi", "stm32", "esp32", "arm cortex",
        "uart", "spi", "i2c", "can bus", "modbus", "mqtt", "coap",
        "linux", "device drivers", "firmware", "iot", "pcb design",
        "kicad", "soldering", "debugging", "gdb", "openocd",
    ],
}

# Cross-domain soft/common skills
COMMON_SKILLS = [
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "project management", "time management",
    "documentation", "presentation", "collaboration", "adaptability",
    "english", "research", "writing",
]

# ── Learning Resource Library ─────────────────────────
RESOURCE_LIBRARY = {
    "python":          [{"name": "Python.org Docs",      "url": "https://docs.python.org/3/tutorial/"},
                        {"name": "Kaggle Python",         "url": "https://www.kaggle.com/learn/python"}],
    "machine learning":[{"name": "Andrew Ng (Coursera)", "url": "https://www.coursera.org/learn/machine-learning"},
                        {"name": "fast.ai",               "url": "https://www.fast.ai"}],
    "deep learning":   [{"name": "Deep Learning Spec.",  "url": "https://www.coursera.org/specializations/deep-learning"},
                        {"name": "PyTorch Tutorials",     "url": "https://pytorch.org/tutorials/"}],
    "nlp":             [{"name": "HuggingFace Course",   "url": "https://huggingface.co/course"},
                        {"name": "Stanford NLP (free)",   "url": "https://web.stanford.edu/class/cs224n/"}],
    "sql":             [{"name": "SQLZoo",                "url": "https://sqlzoo.net"},
                        {"name": "Mode SQL Tutorial",     "url": "https://mode.com/sql-tutorial/"}],
    "tensorflow":      [{"name": "TF Tutorials",         "url": "https://www.tensorflow.org/tutorials"},
                        {"name": "TF Keras Guide",        "url": "https://www.tensorflow.org/guide/keras"}],
    "pytorch":         [{"name": "PyTorch Tutorials",    "url": "https://pytorch.org/tutorials/"},
                        {"name": "Udacity PyTorch",       "url": "https://www.udacity.com/course/deep-learning-pytorch--ud188"}],
    "docker":          [{"name": "Docker Get Started",   "url": "https://docs.docker.com/get-started/"},
                        {"name": "Play with Docker",      "url": "https://labs.play-with-docker.com"}],
    "kubernetes":      [{"name": "Kubernetes Docs",      "url": "https://kubernetes.io/docs/tutorials/"},
                        {"name": "KodeKloud Free",        "url": "https://kodekloud.com/courses/labs-kubernetes-for-beginners/"}],
    "aws":             [{"name": "AWS Free Training",    "url": "https://aws.amazon.com/training/"},
                        {"name": "AWS Skill Builder",     "url": "https://explore.skillbuilder.aws"}],
    "react":           [{"name": "React Official Docs",  "url": "https://react.dev/learn"},
                        {"name": "freeCodeCamp React",   "url": "https://www.freecodecamp.org/learn/front-end-development-libraries/"}],
    "javascript":      [{"name": "MDN JS Guide",         "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"},
                        {"name": "javascript.info",       "url": "https://javascript.info"}],
    "typescript":      [{"name": "TypeScript Handbook",  "url": "https://www.typescriptlang.org/docs/handbook/"},
                        {"name": "Execute Program",       "url": "https://www.executeprogram.com/courses/typescript"}],
    "figma":           [{"name": "Figma Academy",        "url": "https://www.figma.com/academy/"},
                        {"name": "Design Course (YT)",   "url": "https://www.youtube.com/c/DesignCourse"}],
    "flutter":         [{"name": "Flutter Codelabs",     "url": "https://docs.flutter.dev/codelabs"},
                        {"name": "Dart Language Tour",   "url": "https://dart.dev/guides/language/language-tour"}],
    "default":         [{"name": "Coursera (free audit)", "url": "https://www.coursera.org"},
                        {"name": "edX Free Courses",      "url": "https://www.edx.org"},
                        {"name": "YouTube Learning",      "url": "https://www.youtube.com"}],
}

# ─────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Lowercase, strip punctuation noise, normalize spaces."""
    text = text.lower()
    text = re.sub(r"[^\w\s\/\.\-\+#]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text: str, skill_pool: list[str]) -> list[str]:
    """Return skills from pool that appear in the text (phrase match)."""
    text_norm = normalize(text)
    found = []
    for skill in skill_pool:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_norm):
            found.append(skill)
    return found


def get_skill_pool(role: str) -> list[str]:
    """Return domain skill pool + common skills."""
    domain_skills = SKILL_TAXONOMY.get(role, [])
    # If no specific domain, use all skills
    if not domain_skills:
        domain_skills = [s for lst in SKILL_TAXONOMY.values() for s in lst]
    return list(set(domain_skills + COMMON_SKILLS))


def calculate_match_score(matched: list, missing: list) -> int:
    """Weighted match score (matched / total required)."""
    total = len(matched) + len(missing)
    if total == 0:
        return 0
    raw = (len(matched) / total) * 100
    return min(100, max(0, round(raw)))


def assign_priority(skill: str, job_text_norm: str) -> str:
    """Assign HIGH/MEDIUM/LOW priority based on frequency in job desc."""
    pattern = r"\b" + re.escape(skill.lower()) + r"\b"
    count = len(re.findall(pattern, job_text_norm))
    if count >= 3:
        return "high"
    elif count == 2:
        return "medium"
    return "low"


def get_gap_description(skill: str) -> str:
    descriptions = {
        "python":           "Python is the primary language for data science and backend dev. Essential.",
        "machine learning": "Core ML algorithms knowledge is required for most data roles.",
        "deep learning":    "Neural network fundamentals are key for advanced AI/ML positions.",
        "nlp":              "NLP skills involve text preprocessing, embeddings, and transformer models.",
        "sql":              "SQL is needed to query and manipulate structured data in databases.",
        "docker":           "Docker containerization is a must-have skill for modern DevOps pipelines.",
        "kubernetes":       "K8s orchestration is standard for production-scale deployments.",
        "react":            "React is the most in-demand frontend library for web applications.",
        "aws":              "Cloud platform experience, especially AWS, is required in most tech roles.",
        "figma":            "Figma is the industry-standard design and prototyping tool.",
        "typescript":       "TypeScript improves JavaScript code quality and is widely adopted.",
        "flutter":          "Flutter enables cross-platform mobile development with a single codebase.",
    }
    return descriptions.get(
        skill.lower(),
        f"'{skill}' appears in the job description as a required or preferred skill. "
        "Building proficiency will strengthen your application."
    )


def build_roadmap(skill_gaps: list, role: str) -> list:
    """Generate a week-by-week learning roadmap for the top skill gaps."""
    # Sort by priority: high first
    priority_order = {"high": 0, "medium": 1, "low": 2}
    sorted_gaps = sorted(skill_gaps, key=lambda g: priority_order.get(g["priority"], 3))
    roadmap = []
    for i, gap in enumerate(sorted_gaps[:8]):  # cap at 8 steps
        skill_lower = gap["skill"].lower()
        resources   = RESOURCE_LIBRARY.get(skill_lower, RESOURCE_LIBRARY["default"])
        week_start  = i * 2 + 1
        week_end    = week_start + 1
        roadmap.append({
            "skill":       gap["skill"],
            "timeline":    f"Week {week_start}–{week_end}",
            "description": f"Learn {gap['skill']} — {gap.get('description', '')}",
            "resources":   resources,
        })
    return roadmap


# ─────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    POST /analyze
    Body: { resume: str, job_desc: str, role: str, exp_level: str }
    Returns: JSON analysis result
    """
    data      = request.get_json(force=True)
    resume    = data.get("resume", "")
    job_desc  = data.get("job_desc", "")
    role      = data.get("role", "")
    exp_level = data.get("exp_level", "mid")

    if not resume or not job_desc:
        return jsonify({"error": "resume and job_desc are required"}), 400

    skill_pool    = get_skill_pool(role)
    job_desc_norm = normalize(job_desc)
    resume_norm   = normalize(resume)

    # Skill extraction
    resume_skills  = extract_skills(resume_norm,   skill_pool)
    job_skills     = extract_skills(job_desc_norm, skill_pool)

    # Classification
    matched_raw = [s for s in resume_skills if s in job_skills]
    missing_raw = [s for s in job_skills    if s not in resume_skills]
    extra_raw   = [s for s in resume_skills if s not in job_skills]

    # Build matched with confidence scores (presence-based simple weighting)
    matched_skills = []
    for s in matched_raw:
        count = len(re.findall(r"\b" + re.escape(s) + r"\b", resume_norm))
        score = min(100, 60 + count * 10)
        matched_skills.append({"name": s, "score": score})

    # Build missing with priority
    missing_skills = []
    skill_gaps     = []
    for s in missing_raw:
        priority = assign_priority(s, job_desc_norm)
        count    = len(re.findall(r"\b" + re.escape(s) + r"\b", job_desc_norm))
        gap_pct  = min(95, 50 + count * 10)
        desc     = get_gap_description(s)
        missing_skills.append({"name": s, "importance": gap_pct})
        skill_gaps.append({
            "skill":       s,
            "priority":    priority,
            "gap_percent": gap_pct,
            "description": desc,
        })

    # Sort skill gaps: high → medium → low, then by gap_percent desc
    priority_order = {"high": 0, "medium": 1, "low": 2}
    skill_gaps.sort(key=lambda g: (priority_order.get(g["priority"], 3), -g["gap_percent"]))

    extra_skills = [{"name": s} for s in extra_raw[:12]]  # cap bonus skills

    match_score = calculate_match_score(matched_skills, missing_skills)
    roadmap     = build_roadmap(skill_gaps, role)

    return jsonify({
        "match_score":    match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills":   extra_skills,
        "skill_gaps":     skill_gaps,
        "roadmap":        roadmap,
        "meta": {
            "role":      role,
            "exp_level": exp_level,
            "total_job_skills": len(job_skills),
        }
    })


# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=False)
