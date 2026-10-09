"""
SkillMatch AI – Streamlit App
AI Resume & Skill Gap Matcher
SDG 4: Quality Education | SDG 8: Decent Work & Economic Growth
"""

import re
import streamlit as st

# ─────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkillMatch AI – Resume & Skill Gap Matcher",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .main-header {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    padding: 36px 32px 28px; border-radius: 18px; margin-bottom: 28px; text-align: center;
  }
  .main-header h1 { color: white; font-size: 2.2rem; font-weight: 800; margin: 0 0 8px; }
  .main-header p  { color: rgba(255,255,255,0.85); font-size: 1rem; margin: 0; }
  .badge-row { display:flex; gap:10px; justify-content:center; margin-top:14px; flex-wrap:wrap; }
  .badge { padding:4px 14px; border-radius:20px; font-size:0.75rem; font-weight:700; }
  .badge-sdg4 { background:#dbeafe; color:#1d4ed8; }
  .badge-sdg8 { background:#d1fae5; color:#065f46; }
  .score-box {
    background: linear-gradient(135deg, #f5f3ff, #eff6ff);
    border: 1px solid #c7d2fe; border-radius: 16px; padding: 28px;
    text-align: center; margin-bottom: 20px;
  }
  .score-big { font-size: 4rem; font-weight: 900; line-height: 1; }
  .score-label { font-size: 0.9rem; color: #57606a; margin-top: 4px; }
  .skill-tag {
    display:inline-block; padding:4px 12px; border-radius:8px;
    font-size:0.82rem; font-weight:600; margin:3px;
  }
  .skill-matched { background:#d1fae5; color:#065f46; border:1px solid #6ee7b7; }
  .skill-missing { background:#fee2e2; color:#991b1b; border:1px solid #fca5a5; }
  .skill-extra   { background:#dbeafe; color:#1e40af; border:1px solid #93c5fd; }
  .gap-item {
    background:white; border:1px solid #e5e7eb; border-radius:12px;
    padding:16px 20px; margin-bottom:12px;
  }
  .gap-name  { font-weight:700; font-size:0.95rem; }
  .priority-high   { background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:20px; font-size:0.7rem; font-weight:700; }
  .priority-medium { background:#fef9c3; color:#713f12; padding:3px 10px; border-radius:20px; font-size:0.7rem; font-weight:700; }
  .priority-low    { background:#d1fae5; color:#065f46; padding:3px 10px; border-radius:20px; font-size:0.7rem; font-weight:700; }
  .roadmap-item {
    background:white; border:1px solid #e5e7eb; border-radius:12px;
    padding:18px 20px; margin-bottom:14px; border-left: 4px solid #6366f1;
  }
  .roadmap-week { font-size:0.72rem; font-weight:700; color:#6366f1; text-transform:uppercase; letter-spacing:0.06em; }
  .roadmap-skill { font-size:1rem; font-weight:700; margin:4px 0; }
  .roadmap-desc { font-size:0.85rem; color:#57606a; margin-bottom:10px; }
  .resource-link {
    display:inline-block; padding:4px 12px; border-radius:6px; margin:3px;
    background:#ede9fe; color:#6d28d9; font-size:0.78rem; font-weight:600;
    border:1px solid #c4b5fd; text-decoration:none;
  }
  .sdg-card {
    border-radius:16px; padding:24px; margin-bottom:16px;
  }
  .sdg4-card { background:linear-gradient(135deg,#eff6ff,#f5f3ff); border:1px solid #c7d2fe; }
  .sdg8-card { background:linear-gradient(135deg,#f0fdf4,#f0fdfa); border:1px solid #6ee7b7; }
  .footer-bar {
    text-align:center; color:#57606a; font-size:0.8rem;
    border-top:1px solid #e5e7eb; padding-top:20px; margin-top:40px;
  }
  stProgress > div > div { background-color: #6366f1 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# SKILL TAXONOMY
# ─────────────────────────────────────────────────────────
SKILL_TAXONOMY = {
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
    "devops": [
        "docker", "kubernetes", "k8s", "terraform", "ansible", "jenkins",
        "github actions", "ci/cd", "aws", "gcp", "azure", "linux", "bash",
        "shell scripting", "python", "monitoring", "prometheus", "grafana",
        "nginx", "helm", "argocd", "vault", "networking", "vpc",
        "load balancing", "auto scaling", "elasticsearch", "logstash",
        "kibana", "elk", "cloudformation", "infrastructure as code",
        "site reliability", "sre", "on-call", "incident management",
    ],
    "cybersecurity": [
        "network security", "penetration testing", "ethical hacking",
        "siem", "soc", "firewalls", "ids/ips", "vulnerability assessment",
        "cryptography", "ssl/tls", "zero trust", "iam", "sso", "oauth",
        "python", "linux", "bash", "wireshark", "metasploit", "burp suite",
        "owasp", "iso 27001", "nist", "gdpr", "compliance", "incident response",
        "threat intelligence", "reverse engineering", "malware analysis",
    ],
    "product": [
        "product roadmap", "agile", "scrum", "kanban", "jira",
        "user research", "ux", "a/b testing", "data analysis",
        "market research", "competitive analysis", "kpis", "okrs",
        "stakeholder management", "communication", "prioritization",
        "wireframing", "figma", "go-to-market", "sql", "tableau",
        "product strategy", "mvp", "user stories", "backlog",
    ],
    "design": [
        "figma", "sketch", "adobe xd", "photoshop", "illustrator",
        "user research", "wireframing", "prototyping", "usability testing",
        "design systems", "typography", "color theory", "accessibility",
        "responsive design", "interaction design", "ux writing",
        "html", "css", "javascript", "animation", "after effects",
    ],
    "mobile": [
        "swift", "objective-c", "kotlin", "java", "flutter", "dart",
        "react native", "android", "ios", "xcode", "android studio",
        "firebase", "rest api", "sqlite", "realm", "jetpack compose",
        "swiftui", "mobile testing", "app store", "play store", "ci/cd",
    ],
    "embedded": [
        "c", "c++", "embedded c", "assembly", "rtos", "freertos",
        "arduino", "raspberry pi", "stm32", "esp32", "arm cortex",
        "uart", "spi", "i2c", "can bus", "modbus", "mqtt", "coap",
        "linux", "device drivers", "firmware", "iot", "pcb design",
        "kicad", "soldering", "debugging", "gdb", "openocd",
    ],
}

COMMON_SKILLS = [
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "project management", "time management",
    "documentation", "presentation", "collaboration", "adaptability",
    "english", "research", "writing",
]

RESOURCE_LIBRARY = {
    "python":           [{"name": "Python.org Docs",      "url": "https://docs.python.org/3/tutorial/"},
                         {"name": "Kaggle Python",         "url": "https://www.kaggle.com/learn/python"}],
    "machine learning": [{"name": "Andrew Ng (Coursera)", "url": "https://www.coursera.org/learn/machine-learning"},
                         {"name": "fast.ai",               "url": "https://www.fast.ai"}],
    "deep learning":    [{"name": "Deep Learning Spec.",  "url": "https://www.coursera.org/specializations/deep-learning"},
                         {"name": "PyTorch Tutorials",     "url": "https://pytorch.org/tutorials/"}],
    "nlp":              [{"name": "HuggingFace Course",   "url": "https://huggingface.co/course"},
                         {"name": "Stanford NLP (free)",   "url": "https://web.stanford.edu/class/cs224n/"}],
    "sql":              [{"name": "SQLZoo",                "url": "https://sqlzoo.net"},
                         {"name": "Mode SQL Tutorial",     "url": "https://mode.com/sql-tutorial/"}],
    "tensorflow":       [{"name": "TF Tutorials",         "url": "https://www.tensorflow.org/tutorials"},
                         {"name": "TF Keras Guide",        "url": "https://www.tensorflow.org/guide/keras"}],
    "pytorch":          [{"name": "PyTorch Tutorials",    "url": "https://pytorch.org/tutorials/"},
                         {"name": "Udacity PyTorch",       "url": "https://www.udacity.com/course/deep-learning-pytorch--ud188"}],
    "docker":           [{"name": "Docker Get Started",   "url": "https://docs.docker.com/get-started/"},
                         {"name": "Play with Docker",      "url": "https://labs.play-with-docker.com"}],
    "kubernetes":       [{"name": "Kubernetes Docs",      "url": "https://kubernetes.io/docs/tutorials/"},
                         {"name": "KodeKloud Free",        "url": "https://kodekloud.com/courses/labs-kubernetes-for-beginners/"}],
    "aws":              [{"name": "AWS Free Training",    "url": "https://aws.amazon.com/training/"},
                         {"name": "AWS Skill Builder",     "url": "https://explore.skillbuilder.aws"}],
    "react":            [{"name": "React Official Docs",  "url": "https://react.dev/learn"},
                         {"name": "freeCodeCamp React",   "url": "https://www.freecodecamp.org/learn/front-end-development-libraries/"}],
    "javascript":       [{"name": "MDN JS Guide",         "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"},
                         {"name": "javascript.info",       "url": "https://javascript.info"}],
    "typescript":       [{"name": "TypeScript Handbook",  "url": "https://www.typescriptlang.org/docs/handbook/"},
                         {"name": "Execute Program",       "url": "https://www.executeprogram.com/courses/typescript"}],
    "figma":            [{"name": "Figma Academy",        "url": "https://www.figma.com/academy/"},
                         {"name": "Design Course (YT)",   "url": "https://www.youtube.com/c/DesignCourse"}],
    "flutter":          [{"name": "Flutter Codelabs",     "url": "https://docs.flutter.dev/codelabs"},
                         {"name": "Dart Language Tour",   "url": "https://dart.dev/guides/language/language-tour"}],
    "default":          [{"name": "Coursera (free audit)", "url": "https://www.coursera.org"},
                         {"name": "edX Free Courses",      "url": "https://www.edx.org"},
                         {"name": "YouTube Learning",      "url": "https://www.youtube.com"}],
}

# ─────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────
def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s\/\.\-\+#]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_skills(text: str, skill_pool: list) -> list:
    text_norm = normalize(text)
    found = []
    for skill in skill_pool:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_norm):
            found.append(skill)
    return found

def get_skill_pool(role: str) -> list:
    domain_skills = SKILL_TAXONOMY.get(role, [])
    if not domain_skills:
        domain_skills = [s for lst in SKILL_TAXONOMY.values() for s in lst]
    return list(set(domain_skills + COMMON_SKILLS))

def calculate_match_score(matched: list, missing: list) -> int:
    total = len(matched) + len(missing)
    if total == 0:
        return 0
    return min(100, max(0, round((len(matched) / total) * 100)))

def assign_priority(skill: str, job_text_norm: str) -> str:
    count = len(re.findall(r"\b" + re.escape(skill.lower()) + r"\b", job_text_norm))
    if count >= 3:   return "high"
    elif count == 2: return "medium"
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
    priority_order = {"high": 0, "medium": 1, "low": 2}
    sorted_gaps = sorted(skill_gaps, key=lambda g: priority_order.get(g["priority"], 3))
    roadmap = []
    for i, gap in enumerate(sorted_gaps[:8]):
        resources  = RESOURCE_LIBRARY.get(gap["skill"].lower(), RESOURCE_LIBRARY["default"])
        week_start = i * 2 + 1
        roadmap.append({
            "skill":       gap["skill"],
            "timeline":    f"Week {week_start}–{week_start + 1}",
            "description": f"Learn {gap['skill']} — {gap.get('description', '')}",
            "resources":   resources,
        })
    return roadmap

def analyze(resume: str, job_desc: str, role: str, exp_level: str) -> dict:
    skill_pool    = get_skill_pool(role)
    job_desc_norm = normalize(job_desc)
    resume_norm   = normalize(resume)

    resume_skills = extract_skills(resume_norm,   skill_pool)
    job_skills    = extract_skills(job_desc_norm, skill_pool)

    matched_raw = [s for s in resume_skills if s in job_skills]
    missing_raw = [s for s in job_skills    if s not in resume_skills]
    extra_raw   = [s for s in resume_skills if s not in job_skills]

    matched_skills = []
    for s in matched_raw:
        count = len(re.findall(r"\b" + re.escape(s) + r"\b", resume_norm))
        matched_skills.append({"name": s, "score": min(100, 60 + count * 10)})

    missing_skills = []
    skill_gaps     = []
    for s in missing_raw:
        priority = assign_priority(s, job_desc_norm)
        count    = len(re.findall(r"\b" + re.escape(s) + r"\b", job_desc_norm))
        gap_pct  = min(95, 50 + count * 10)
        desc     = get_gap_description(s)
        missing_skills.append({"name": s, "importance": gap_pct})
        skill_gaps.append({"skill": s, "priority": priority, "gap_percent": gap_pct, "description": desc})

    priority_order = {"high": 0, "medium": 1, "low": 2}
    skill_gaps.sort(key=lambda g: (priority_order.get(g["priority"], 3), -g["gap_percent"]))

    match_score = calculate_match_score(matched_skills, missing_skills)
    return {
        "match_score":    match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills":   [{"name": s} for s in extra_raw[:12]],
        "skill_gaps":     skill_gaps,
        "roadmap":        build_roadmap(skill_gaps, role),
    }

# ─────────────────────────────────────────────────────────
# UI — HEADER
# ─────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🎯 SkillMatch AI</h1>
  <p>AI-Powered Resume & Skill Gap Matcher · Paste your resume and a job description to get your match score and personalized learning roadmap.</p>
  <div class="badge-row">
    <span class="badge badge-sdg4">SDG 4 · Quality Education</span>
    <span class="badge badge-sdg8">SDG 8 · Decent Work</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# UI — INPUT FORM
# ─────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("### 📄 Your Resume")
    resume_input = st.text_area(
        "Paste your resume text here",
        height=240,
        placeholder="John Doe | Software Engineer\nSkills: Python, Machine Learning, TensorFlow, SQL, React\nExperience: 3 years at ABC Corp — built ML pipelines, NLP models\nEducation: B.Sc. Computer Science, 2020",
        label_visibility="collapsed",
    )

    uploaded_file = st.file_uploader("Or upload a .txt resume file", type=["txt"])
    if uploaded_file:
        resume_input = uploaded_file.read().decode("utf-8")
        st.success(f"✅ Loaded: {uploaded_file.name}")

    st.markdown("### 🏢 Job Description")
    job_desc_input = st.text_area(
        "Paste the job description",
        height=200,
        placeholder="We are looking for a Senior Data Scientist with:\n- 4+ years Python, pandas, scikit-learn\n- Deep learning (PyTorch or TensorFlow)\n- NLP and transformer models (BERT, GPT)\n- Cloud platforms: AWS or GCP\n- Strong SQL and data warehousing skills",
        label_visibility="collapsed",
    )

    c1, c2 = st.columns(2)
    with c1:
        job_role = st.selectbox("Target Job Domain", [
            ("", "Select a domain..."),
            ("data_science",   "Data Science / ML"),
            ("web_dev",        "Web Development"),
            ("devops",         "DevOps / Cloud"),
            ("cybersecurity",  "Cybersecurity"),
            ("product",        "Product Management"),
            ("design",         "UI/UX Design"),
            ("mobile",         "Mobile Development"),
            ("embedded",       "Embedded / IoT"),
        ], format_func=lambda x: x[1])
    with c2:
        exp_level = st.selectbox("Experience Level", [
            ("entry",  "Entry Level (0–2 yrs)"),
            ("mid",    "Mid Level (2–5 yrs)"),
            ("senior", "Senior (5+ yrs)"),
        ], index=1, format_func=lambda x: x[1])

    analyze_btn = st.button("🚀 Analyze My Skills", use_container_width=True, type="primary")

# ─────────────────────────────────────────────────────────
# UI — RESULTS
# ─────────────────────────────────────────────────────────
with col_right:
    if not analyze_btn:
        st.markdown("""
        <div style="background:#fafafa;border:2px dashed #e5e7eb;border-radius:16px;
                    padding:60px 32px;text-align:center;min-height:400px;
                    display:flex;flex-direction:column;align-items:center;justify-content:center;">
          <div style="font-size:3rem;margin-bottom:16px">✨</div>
          <h3 style="font-size:1.15rem;font-weight:700;margin-bottom:8px">Your Analysis Will Appear Here</h3>
          <p style="color:#57606a;font-size:0.9rem">Fill in your resume and job description, then click Analyze.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        if not resume_input.strip():
            st.error("⚠️ Please paste or upload your resume.")
        elif not job_desc_input.strip():
            st.error("⚠️ Please paste the job description.")
        else:
            with st.spinner("Analyzing your skills..."):
                result = analyze(resume_input, job_desc_input, job_role[0], exp_level[0])

            score = result["match_score"]

            # Score colour
            if   score >= 75: score_color = "#10b981"; score_title = "🎉 Strong Match!"
            elif score >= 50: score_color = "#f59e0b"; score_title = "👍 Good Potential"
            elif score >= 30: score_color = "#f97316"; score_title = "🚀 Room to Grow"
            else:             score_color = "#ef4444"; score_title = "📚 Start Your Journey"

            # Score card
            st.markdown(f"""
            <div class="score-box">
              <div class="score-big" style="color:{score_color}">{score}%</div>
              <div style="font-size:1.1rem;font-weight:700;margin-top:8px">{score_title}</div>
              <div class="score-label">Overall Match Score</div>
              <div style="margin-top:14px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
                <span style="background:#d1fae5;color:#065f46;padding:3px 12px;border-radius:20px;font-size:0.78rem;font-weight:700">
                  ✓ {len(result['matched_skills'])} Matched
                </span>
                <span style="background:#fee2e2;color:#991b1b;padding:3px 12px;border-radius:20px;font-size:0.78rem;font-weight:700">
                  ✗ {len(result['missing_skills'])} Missing
                </span>
                <span style="background:#dbeafe;color:#1e40af;padding:3px 12px;border-radius:20px;font-size:0.78rem;font-weight:700">
                  + {len(result['extra_skills'])} Bonus
                </span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(score / 100)

            # Tabs
            tab1, tab2, tab3 = st.tabs(["📊 Skills Analysis", "⚠️ Skill Gaps", "🗺️ Learning Roadmap"])

            # ── Tab 1: Skills ────────────────────────────
            with tab1:
                c_match, c_miss = st.columns(2)
                with c_match:
                    st.markdown("**✅ Matched Skills**")
                    if result["matched_skills"]:
                        tags = "".join(
                            f'<span class="skill-tag skill-matched">✓ {s["name"]} <small style="opacity:0.7">{s["score"]}%</small></span>'
                            for s in result["matched_skills"]
                        )
                        st.markdown(tags, unsafe_allow_html=True)
                    else:
                        st.caption("No matched skills found.")

                with c_miss:
                    st.markdown("**❌ Missing Skills**")
                    if result["missing_skills"]:
                        tags = "".join(
                            f'<span class="skill-tag skill-missing">✗ {s["name"]}</span>'
                            for s in result["missing_skills"]
                        )
                        st.markdown(tags, unsafe_allow_html=True)
                    else:
                        st.caption("No missing skills — great match!")

                st.markdown("---")
                st.markdown("**📌 Your Additional Skills**")
                if result["extra_skills"]:
                    tags = "".join(
                        f'<span class="skill-tag skill-extra">+ {s["name"]}</span>'
                        for s in result["extra_skills"]
                    )
                    st.markdown(tags, unsafe_allow_html=True)
                else:
                    st.caption("No extra skills detected.")

            # ── Tab 2: Gaps ──────────────────────────────
            with tab2:
                gaps = result["skill_gaps"]
                if not gaps:
                    st.success("No significant skill gaps — you're a great match!")
                else:
                    for g in gaps:
                        p = g["priority"]
                        p_html = f'<span class="priority-{p}">{p.upper()} PRIORITY</span>'
                        st.markdown(f"""
                        <div class="gap-item">
                          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                            <span class="gap-name">{g['skill']}</span>
                            {p_html}
                          </div>
                          <div style="background:#f3f4f6;border-radius:4px;height:6px;margin-bottom:8px;overflow:hidden">
                            <div style="width:{g['gap_percent']}%;height:100%;background:linear-gradient(90deg,#f87171,#fb923c);border-radius:4px"></div>
                          </div>
                          <p style="font-size:0.83rem;color:#57606a;margin:0">{g['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)

            # ── Tab 3: Roadmap ───────────────────────────
            with tab3:
                roadmap = result["roadmap"]
                if not roadmap:
                    st.success("No roadmap needed — you already match the job well!")
                else:
                    for i, step in enumerate(roadmap):
                        links_html = "".join(
                            f'<a href="{r["url"]}" target="_blank" class="resource-link">{r["name"]}</a>'
                            for r in step["resources"]
                        )
                        st.markdown(f"""
                        <div class="roadmap-item">
                          <div class="roadmap-week">{step['timeline']}</div>
                          <div class="roadmap-skill">Step {i+1}: {step['skill']}</div>
                          <div class="roadmap-desc">{step['description']}</div>
                          <div>{links_html}</div>
                        </div>
                        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
  <strong>SkillMatch AI</strong> · Contributing to UN SDG 4 (Quality Education) &amp; SDG 8 (Decent Work) · Built with Python &amp; Streamlit
</div>
""", unsafe_allow_html=True)
