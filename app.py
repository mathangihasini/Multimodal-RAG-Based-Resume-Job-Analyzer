import streamlit as st
import io
import re
import html
from PIL import Image

# ============================================================
# OPTIONAL LIBRARIES
# ============================================================

try:
    import pymupdf
except ImportError:
    pymupdf = None

try:
    import pytesseract
except ImportError:
    pytesseract = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResumeAI | Career Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* =========================
   GLOBAL
========================= */

.stApp {
    background:
        radial-gradient(circle at 5% 5%, rgba(124, 58, 237, 0.28), transparent 28%),
        radial-gradient(circle at 95% 10%, rgba(6, 182, 212, 0.22), transparent 25%),
        radial-gradient(circle at 50% 90%, rgba(236, 72, 153, 0.18), transparent 30%),
        linear-gradient(135deg, #07111f 0%, #0b1024 45%, #111827 100%);
    color: #f8fafc;
}

.main .block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4, p {
    font-family: Inter, system-ui, sans-serif;
}

p {
    color: #cbd5e1;
}


/* =========================
   TOP BAR
========================= */

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 13px 20px;
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    background: rgba(15, 23, 42, 0.72);
    backdrop-filter: blur(18px);
    box-shadow: 0 10px 35px rgba(0,0,0,0.20);
}

.brand {
    font-size: 19px;
    font-weight: 800;
    color: white;
}

.brand span {
    background: linear-gradient(90deg, #a78bfa, #22d3ee, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.top-status {
    font-size: 12px;
    color: #a7f3d0;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.25);
    padding: 7px 13px;
    border-radius: 30px;
}


/* =========================
   HERO
========================= */

.hero {
    position: relative;
    overflow: hidden;
    padding: 60px 55px;
    border-radius: 32px;
    margin-bottom: 28px;
    border: 1px solid rgba(255,255,255,0.12);
    background:
        linear-gradient(
            135deg,
            rgba(124,58,237,0.38),
            rgba(15,23,42,0.90) 45%,
            rgba(6,182,212,0.24)
        );
    box-shadow:
        0 30px 80px rgba(0,0,0,0.30),
        inset 0 1px 0 rgba(255,255,255,0.08);
}

.hero:before {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -90px;
    top: -90px;
    background: rgba(34,211,238,0.18);
    border-radius: 50%;
    filter: blur(15px);
}

.hero:after {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    left: -100px;
    bottom: -110px;
    background: rgba(236,72,153,0.18);
    border-radius: 50%;
    filter: blur(20px);
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-tag {
    display: inline-block;
    padding: 8px 15px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.3px;
    color: #ddd6fe;
    background: rgba(139,92,246,0.18);
    border: 1px solid rgba(167,139,250,0.35);
    margin-bottom: 18px;
}

.hero h1 {
    font-size: clamp(42px, 7vw, 72px);
    line-height: 1;
    margin: 0;
    font-weight: 900;
    letter-spacing: -3px;
    background: linear-gradient(
        90deg,
        #ffffff,
        #c4b5fd,
        #67e8f9,
        #f9a8d4
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero h2 {
    font-size: 23px;
    color: #e2e8f0;
    margin-top: 18px;
    margin-bottom: 15px;
    font-weight: 700;
}

.hero p {
    max-width: 780px;
    font-size: 17px;
    line-height: 1.8;
    color: #cbd5e1;
}

.hero-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 25px;
}

.hero-chip {
    padding: 8px 13px;
    border-radius: 20px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: #e2e8f0;
    font-size: 12px;
    font-weight: 700;
}


/* =========================
   SECTION HEADER
========================= */

.section-header {
    text-align: center;
    margin: 42px 0 25px;
}

.section-label {
    display: inline-block;
    color: #67e8f9;
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.section-header h2 {
    font-size: 32px;
    margin: 0;
    color: #f8fafc;
    font-weight: 850;
}

.section-header p {
    margin: 9px auto 0;
    max-width: 720px;
    font-size: 14px;
}


/* =========================
   FEATURE CARDS
========================= */

.feature-card {
    min-height: 210px;
    padding: 27px 24px;
    border-radius: 23px;
    background: rgba(15,23,42,0.78);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 15px 40px rgba(0,0,0,0.20);
    transition: transform 0.25s ease, border-color 0.25s ease;
    position: relative;
    overflow: hidden;
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255,255,255,0.24);
}

.feature-card:before {
    content: "";
    position: absolute;
    height: 4px;
    left: 0;
    right: 0;
    top: 0;
    background: linear-gradient(90deg, #8b5cf6, #22d3ee, #ec4899);
}

.feature-icon {
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    font-size: 25px;
    margin-bottom: 20px;
    background: linear-gradient(
        135deg,
        rgba(139,92,246,0.28),
        rgba(34,211,238,0.16)
    );
    border: 1px solid rgba(255,255,255,0.10);
}

.feature-card h3 {
    font-size: 17px;
    color: white;
    margin: 0 0 9px;
    font-weight: 800;
}

.feature-card p {
    font-size: 13px;
    line-height: 1.65;
    margin: 0;
}


/* =========================
   ANALYSIS PANEL
========================= */

.analysis-wrapper {
    padding: 28px;
    border-radius: 28px;
    background: rgba(15,23,42,0.72);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 25px 60px rgba(0,0,0,0.25);
}

.input-card {
    padding: 22px;
    min-height: 270px;
    border-radius: 22px;
    background: rgba(2,6,23,0.58);
    border: 1px solid rgba(255,255,255,0.09);
}

.input-card.resume {
    border-top: 3px solid #a78bfa;
}

.input-card.job {
    border-top: 3px solid #22d3ee;
}

.input-title {
    font-size: 18px;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 5px;
}

.input-subtitle {
    font-size: 12px;
    color: #94a3b8;
    margin-bottom: 17px;
}

.upload-badge {
    display: inline-block;
    padding: 6px 10px;
    margin-top: 10px;
    border-radius: 12px;
    font-size: 11px;
    color: #c4b5fd;
    background: rgba(139,92,246,0.12);
    border: 1px solid rgba(139,92,246,0.25);
}


/* =========================
   STREAMLIT INPUTS
========================= */

.stFileUploader {
    background: rgba(15,23,42,0.55);
    border-radius: 16px;
}

.stFileUploader section {
    border: 1px dashed rgba(167,139,250,0.45) !important;
    border-radius: 16px !important;
    background: rgba(139,92,246,0.06) !important;
}

.stTextArea textarea {
    background: rgba(2,6,23,0.75) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(34,211,238,0.25) !important;
    border-radius: 15px !important;
    font-size: 14px !important;
}

.stTextArea textarea:focus {
    border-color: #22d3ee !important;
    box-shadow: 0 0 0 2px rgba(34,211,238,0.12) !important;
}


/* =========================
   BUTTON
========================= */

.stButton > button {
    width: 100%;
    min-height: 55px;
    border: none !important;
    border-radius: 17px !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: 850 !important;
    background: linear-gradient(
        100deg,
        #7c3aed,
        #2563eb,
        #06b6d4
    ) !important;
    box-shadow:
        0 12px 30px rgba(37,99,235,0.28),
        inset 0 1px 0 rgba(255,255,255,0.20);
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 17px 38px rgba(37,99,235,0.40),
        inset 0 1px 0 rgba(255,255,255,0.20);
}


/* =========================
   RESULT HEADER
========================= */

.result-banner {
    padding: 25px 28px;
    border-radius: 24px;
    margin: 30px 0 22px;
    background:
        linear-gradient(
            110deg,
            rgba(16,185,129,0.18),
            rgba(6,182,212,0.12),
            rgba(139,92,246,0.16)
        );
    border: 1px solid rgba(52,211,153,0.20);
}

.result-banner h2 {
    margin: 0;
    color: white;
    font-size: 26px;
}

.result-banner p {
    margin: 7px 0 0;
}


/* =========================
   METRICS
========================= */

.metric-card {
    padding: 23px;
    border-radius: 21px;
    min-height: 135px;
    background: rgba(15,23,42,0.78);
    border: 1px solid rgba(255,255,255,0.09);
    box-shadow: 0 15px 35px rgba(0,0,0,0.18);
}

.metric-label {
    color: #94a3b8;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    font-weight: 800;
}

.metric-value {
    font-size: 34px;
    font-weight: 900;
    margin-top: 8px;
    background: linear-gradient(90deg, #c4b5fd, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-small {
    color: #64748b;
    font-size: 11px;
    margin-top: 4px;
}


/* =========================
   SCORE RING
========================= */

.score-ring {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px auto 20px;
    background: conic-gradient(
        #8b5cf6 var(--score),
        rgba(255,255,255,0.08) var(--score)
    );
    position: relative;
}

.score-ring:before {
    content: "";
    width: 116px;
    height: 116px;
    border-radius: 50%;
    position: absolute;
    background: #0b1220;
}

.score-number {
    position: relative;
    z-index: 2;
    font-size: 32px;
    font-weight: 900;
    color: white;
}

.score-label {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
}


/* =========================
   CONTENT CARDS
========================= */

.content-card {
    padding: 24px;
    border-radius: 22px;
    background: rgba(15,23,42,0.76);
    border: 1px solid rgba(255,255,255,0.09);
    margin-top: 20px;
}

.card-title {
    font-size: 19px;
    font-weight: 850;
    color: white;
    margin-bottom: 17px;
}

.skill-pill {
    display: inline-block;
    padding: 7px 12px;
    margin: 4px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    color: #ddd6fe;
    background: rgba(139,92,246,0.13);
    border: 1px solid rgba(139,92,246,0.28);
}

.skill-pill.match {
    color: #a7f3d0;
    background: rgba(16,185,129,0.12);
    border-color: rgba(16,185,129,0.25);
}

.skill-pill.recommended {
    color: #bae6fd;
    background: rgba(6,182,212,0.12);
    border-color: rgba(6,182,212,0.25);
}


/* =========================
   SUGGESTION CARDS
========================= */

.suggestion {
    padding: 15px 17px;
    margin: 9px 0;
    border-radius: 15px;
    background: rgba(245,158,11,0.07);
    border-left: 4px solid #f59e0b;
    color: #e2e8f0;
    font-size: 13px;
    line-height: 1.6;
}


/* =========================
   PROFILE
========================= */

.profile-card {
    padding: 25px;
    border-radius: 22px;
    background:
        linear-gradient(
            135deg,
            rgba(139,92,246,0.17),
            rgba(34,211,238,0.08)
        );
    border: 1px solid rgba(167,139,250,0.20);
}

.profile-name {
    font-size: 27px;
    font-weight: 900;
    color: white;
}

.profile-score {
    display: inline-block;
    margin-top: 9px;
    padding: 7px 12px;
    border-radius: 20px;
    background: rgba(139,92,246,0.18);
    color: #c4b5fd;
    font-size: 12px;
    font-weight: 800;
}


/* =========================
   EXPANDER
========================= */

.streamlit-expanderHeader {
    background: rgba(15,23,42,0.70) !important;
    border-radius: 15px !important;
    color: #e2e8f0 !important;
}


/* =========================
   DOWNLOAD
========================= */

.stDownloadButton > button {
    background: rgba(16,185,129,0.14) !important;
    border: 1px solid rgba(16,185,129,0.30) !important;
    color: #a7f3d0 !important;
    border-radius: 14px !important;
}


/* =========================
   FOOTER
========================= */

.footer {
    margin-top: 55px;
    padding: 30px;
    border-radius: 25px;
    text-align: center;
    background:
        linear-gradient(
            135deg,
            rgba(124,58,237,0.15),
            rgba(6,182,212,0.10)
        );
    border: 1px solid rgba(255,255,255,0.08);
}

.footer-brand {
    font-size: 22px;
    font-weight: 900;
    color: white;
}

.footer-text {
    margin-top: 6px;
    color: #94a3b8;
    font-size: 13px;
}

.footer-highlight {
    margin-top: 16px;
    color: #67e8f9;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.5px;
}


/* =========================
   MOBILE
========================= */

@media (max-width: 768px) {

    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 38px 25px;
        border-radius: 25px;
    }

    .hero h1 {
        font-size: 45px;
        letter-spacing: -2px;
    }

    .hero h2 {
        font-size: 18px;
    }

    .hero p {
        font-size: 14px;
    }

    .analysis-wrapper {
        padding: 17px;
    }

    .top-status {
        display: none;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TOP BAR
# ============================================================

st.markdown("""
<div class="topbar">
    <div class="brand">🚀 <span>ResumeAI</span></div>
    <div class="top-status">● AI Career Intelligence Active</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-content">

        <div class="hero-tag">
            ✦ AI-POWERED CAREER INTELLIGENCE
        </div>

        <h1>
            🚀 ResumeAI
        </h1>

        <h2>
            Multimodal RAG-Based Resume & Job Analyzer
        </h2>

        <p>
            Transform your resume into powerful career insights.
            Analyze your skills, discover your ideal career profile,
            compare job requirements, and receive AI-powered
            recommendations to build a stronger, job-ready resume.
        </p>

        <div class="hero-chips">
            <div class="hero-chip">📄 Resume Parsing</div>
            <div class="hero-chip">🎯 ATS Scoring</div>
            <div class="hero-chip">🧠 Career Analysis</div>
            <div class="hero-chip">⚡ Skill Matching</div>
            <div class="hero-chip">✨ Smart Suggestions</div>
        </div>

    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# FEATURES
# ============================================================

st.markdown("""
<div class="section-header">
    <div class="section-label">POWERFUL AI FEATURES</div>
    <h2>✨ Powerful Resume Intelligence</h2>
    <p>
        Everything you need to understand, improve, and optimize
        your resume for today's competitive job market.
    </p>
</div>
""", unsafe_allow_html=True)

features = [
    (
        "📄",
        "Smart Resume Parsing",
        "Extract important information, skills, keywords, education, and experience from your resume automatically."
    ),
    (
        "🎯",
        "AI Resume Scoring",
        "Get an intelligent resume score based on content quality, skills, keywords, and job relevance."
    ),
    (
        "🧠",
        "Career Profile Analysis",
        "Discover the career profile that best matches your current resume and technical strengths."
    ),
    (
        "📊",
        "Intelligent Skill Analytics",
        "Identify your existing skills and compare them against the requirements of your target job."
    ),
    (
        "✨",
        "AI-Powered Suggestions",
        "Receive practical recommendations to strengthen your resume and improve your job-readiness."
    )
]

cols = st.columns(5)

for i, (icon, title, description) in enumerate(features):
    with cols[i]:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# SKILLS DATABASE
# ============================================================

SKILLS = [
    "Python", "Java", "C", "C++", "SQL",
    "MySQL", "PostgreSQL", "MongoDB",
    "HTML", "CSS", "JavaScript",
    "React", "Node.js", "Flask", "Django",
    "Streamlit", "Git", "GitHub", "Docker",
    "AWS", "Azure", "GCP",
    "Excel", "Power BI", "Tableau", "PowerPoint",
    "MS Office",
    "Pandas", "NumPy", "Matplotlib", "Seaborn",
    "Scikit-learn", "TensorFlow", "PyTorch",
    "Machine Learning", "Deep Learning",
    "Artificial Intelligence", "AI",
    "Data Analysis", "Data Analytics",
    "Data Visualization", "Statistics",
    "Data Cleaning", "Data Preprocessing",
    "Data Mining",
    "NLP", "Natural Language Processing",
    "RAG", "LLM", "Generative AI",
    "Firebase",
    "Communication", "Leadership",
    "Problem Solving", "Teamwork"
]


# ============================================================
# FUNCTIONS
# ============================================================

def extract_pdf_text(uploaded_file):

    if pymupdf is None:
        return "PDF_READER_NOT_AVAILABLE"

    try:
        pdf_bytes = uploaded_file.getvalue()

        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        if len(text.strip()) >= 80:
            return text

        return "OCR_REQUIRED"

    except Exception:
        return "PDF_EXTRACTION_ERROR"


def extract_ocr_text(uploaded_file):

    if pymupdf is None or pytesseract is None:
        return ""

    try:
        pdf_bytes = uploaded_file.getvalue()

        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        full_text = []

        for page in document:

            matrix = pymupdf.Matrix(2, 2)

            pix = page.get_pixmap(
                matrix=matrix,
                alpha=False
            )

            image_bytes = pix.tobytes("png")

            image = Image.open(
                io.BytesIO(image_bytes)
            )

            page_text = pytesseract.image_to_string(
                image,
                config="--psm 6"
            )

            full_text.append(page_text)

        document.close()

        return "\n".join(full_text)

    except Exception:
        return ""


def process_resume(uploaded_file):

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):

        text = extract_pdf_text(uploaded_file)

        if text == "OCR_REQUIRED":

            ocr_text = extract_ocr_text(uploaded_file)

            if ocr_text.strip():
                return ocr_text, True

            return "", True

        if text.startswith("PDF_"):
            return "", False

        return text, False

    if filename.endswith(".txt"):

        try:
            return (
                uploaded_file.getvalue()
                .decode("utf-8", errors="ignore"),
                False
            )
        except Exception:
            return "", False

    return "", False


def extract_skills(text):

    text_lower = text.lower()

    detected = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text_lower):
            detected.append(skill)

    return detected


def extract_keywords(text):

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z+#.\-]{2,}\b",
        text.lower()
    )

    stop_words = {
        "the", "and", "for", "with", "this",
        "that", "from", "your", "you",
        "are", "was", "were", "have",
        "has", "will", "into", "using",
        "our", "their", "about", "which",
        "also", "can", "job", "work"
    }

    frequency = {}

    for word in words:

        if word in stop_words:
            continue

        frequency[word] = frequency.get(word, 0) + 1

    sorted_words = sorted(
        frequency.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [word for word, count in sorted_words[:20]]


def calculate_scores(resume_text, job_text, skills):

    resume_lower = resume_text.lower()

    if job_text.strip():

        job_skills = extract_skills(job_text)

        if job_skills:

            matched = [
                skill for skill in job_skills
                if skill.lower() in resume_lower
            ]

            skill_match = round(
                len(matched) / len(job_skills) * 100
            )

        else:
            skill_match = 0

        resume_keywords = set(
            extract_keywords(resume_text)
        )

        job_keywords = set(
            extract_keywords(job_text)
        )

        if job_keywords:

            keyword_match = round(
                len(
                    resume_keywords.intersection(
                        job_keywords
                    )
                )
                / len(job_keywords)
                * 100
            )

        else:
            keyword_match = 0

    else:

        skill_match = min(
            100,
            len(skills) * 6
        )

        keyword_match = min(
            100,
            len(extract_keywords(resume_text)) * 5
        )

    content_score = min(
        100,
        round(
            45 + len(resume_text) / 80
        )
    )

    overall = round(
        (
            content_score * 0.35
            + skill_match * 0.40
            + keyword_match * 0.25
        )
    )

    overall = max(
        0,
        min(100, overall)
    )

    return (
        overall,
        skill_match,
        keyword_match
    )


def detect_profile(skills, text):

    text_lower = text.lower()

    profiles = {
        "Data Analyst": [
            "python",
            "sql",
            "pandas",
            "excel",
            "power bi",
            "tableau",
            "data analysis",
            "statistics"
        ],

        "AI / ML Engineer": [
            "python",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "artificial intelligence"
        ],

        "Software Developer": [
            "python",
            "java",
            "c++",
            "javascript",
            "react",
            "node.js",
            "git"
        ],

        "Web Developer": [
            "html",
            "css",
            "javascript",
            "react",
            "node.js"
        ],

        "Data Scientist": [
            "python",
            "pandas",
            "numpy",
            "statistics",
            "machine learning",
            "data analysis"
        ],

        "Cloud / DevOps": [
            "aws",
            "azure",
            "gcp",
            "docker",
            "git"
        ]
    }

    scores = {}

    for profile, keywords in profiles.items():

        score = 0

        for keyword in keywords:

            if keyword.lower() in text_lower:
                score += 1

        scores[profile] = score

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:3]


def generate_suggestions(
    resume_text,
    job_text,
    resume_skills,
    job_skills
):

    suggestions = []

    text_lower = resume_text.lower()

    if len(resume_text) < 500:
        suggestions.append(
            "Add more detailed project, internship, education, and achievement information to strengthen your resume."
        )

    if "project" not in text_lower:
        suggestions.append(
            "Add 2–3 relevant projects with technologies used and measurable outcomes."
        )

    if "experience" not in text_lower and "intern" not in text_lower:
        suggestions.append(
            "Include internship, academic, freelance, or practical experience where applicable."
        )

    if "education" not in text_lower:
        suggestions.append(
            "Make your education section clear and easy for ATS systems to identify."
        )

    missing_skills = [
        skill for skill in job_skills
        if skill.lower() not in text_lower
    ]

    if missing_skills:
        suggestions.append(
            "Consider adding relevant missing skills only if you genuinely have experience with them: "
            + ", ".join(missing_skills[:6])
            + "."
        )

    if not suggestions:
        suggestions.append(
            "Your resume has a solid foundation. Focus on measurable achievements and tailoring keywords to each target job."
        )

    return suggestions


def score_message(score):

    if score >= 80:
        return "Excellent Match", "🟢"

    if score >= 65:
        return "Strong Match", "🔵"

    if score >= 50:
        return "Moderate Match", "🟡"

    return "Needs Improvement", "🟠"


# ============================================================
# ANALYSIS SECTION
# ============================================================

st.markdown("""
<div class="section-header">
    <div class="section-label">ANALYSIS WORKSPACE</div>
    <h2>🔍 Start Your Resume Analysis</h2>
    <p>
        Upload your resume and add a target job description
        to discover your skills, match score, career profile,
        and personalized improvement recommendations.
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown(
    '<div class="analysis-wrapper">',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2, gap="large")


# ============================================================
# RESUME INPUT
# ============================================================

with col1:

    st.markdown("""
    <div class="input-card resume">

        <div class="input-title">
            📄 Upload Your Resume
        </div>

        <div class="input-subtitle">
            Upload your PDF or TXT resume for AI-powered analysis.
        </div>

    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose your resume",
        type=["pdf", "txt"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        st.markdown(
            f"""
            <div class="upload-badge">
                ✓ {html.escape(uploaded_file.name)} uploaded successfully
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# JOB DESCRIPTION
# ============================================================

with col2:

    st.markdown("""
    <div class="input-card job">

        <div class="input-title">
            💼 Job Description
        </div>

        <div class="input-subtitle">
            Paste the target job description to compare your resume.
        </div>

    </div>
    """, unsafe_allow_html=True)

    job_description = st.text_area(
        "Job Description",
        placeholder=(
            "Paste the job description here...\n\n"
            "Example:\n"
            "Python, SQL, Pandas, Excel, Power BI, "
            "Data Analysis, Statistics..."
        ),
        height=180,
        label_visibility="collapsed"
    )


st.markdown(
    "<br>",
    unsafe_allow_html=True
)

analyze = st.button(
    "🚀 Analyze My Resume",
    use_container_width=True
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    if uploaded_file is None:

        st.error(
            "📄 Please upload your resume first."
        )
        st.stop()

    with st.spinner(
        "🔄 Analyzing your resume and matching career insights..."
    ):

        resume_text, used_ocr = process_resume(
            uploaded_file
        )

        if not resume_text.strip():

            st.error(
                "❌ Unable to extract text from this resume. "
                "Please upload a text-based PDF or TXT file."
            )
            st.stop()

        resume_skills = extract_skills(
            resume_text
        )

        job_skills = extract_skills(
            job_description
        )

        (
            overall_score,
            skill_match,
            keyword_match
        ) = calculate_scores(
            resume_text,
            job_description,
            resume_skills
        )

        profiles = detect_profile(
            resume_skills,
            resume_text
        )

        suggestions = generate_suggestions(
            resume_text,
            job_description,
            resume_skills,
            job_skills
        )

        matched_skills = [
            skill
            for skill in job_skills
            if skill.lower()
            in resume_text.lower()
        ]

        recommended_skills = [
            skill
            for skill in job_skills
            if skill.lower()
            not in resume_text.lower()
        ][:10]

    # ========================================================
    # RESULT BANNER
    # ========================================================

    status_text, status_icon = score_message(
        overall_score
    )

    st.markdown(
        f"""
        <div class="result-banner">

            <h2>
                ✨ Resume Analysis Complete
            </h2>

            <p>
                {status_icon} <strong>{status_text}</strong>
                — Your resume has been analyzed successfully.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # METRICS
    # ========================================================

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Overall ATS Score
                </div>

                <div class="metric-value">
                    {overall_score}%
                </div>

                <div class="metric-small">
                    Resume strength
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with m2:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Skill Match
                </div>

                <div class="metric-value">
                    {skill_match}%
                </div>

                <div class="metric-small">
                    Job requirements
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with m3:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Keyword Match
                </div>

                <div class="metric-value">
                    {keyword_match}%
                </div>

                <div class="metric-small">
                    Relevant keywords
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with m4:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    Skills Detected
                </div>

                <div class="metric-value">
                    {len(resume_skills)}
                </div>

                <div class="metric-small">
                    Technical & soft skills
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # SCORE + PROFILE
    # ========================================================

    left, right = st.columns([1, 1], gap="large")

    with left:

        score_percentage = f"{overall_score}%"

        st.markdown(
            f"""
            <div class="content-card">

                <div class="card-title">
                    🎯 Overall Resume Strength
                </div>

                <div
                    class="score-ring"
                    style="--score:{score_percentage};"
                >
                    <div class="score-number">
                        {overall_score}
                    </div>
                </div>

                <div class="score-label">
                    Resume / Job Compatibility
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with right:

        primary_profile = (
            profiles[0][0]
            if profiles
            else "General Professional"
        )

        profile_score = (
            profiles[0][1]
            if profiles
            else 0
        )

        st.markdown(
            f"""
            <div class="content-card">

                <div class="card-title">
                    🧠 Detected Career Profile
                </div>

                <div class="profile-card">

                    <div class="profile-name">
                        {html.escape(primary_profile)}
                    </div>

                    <div class="profile-score">
                        Profile relevance: {profile_score} signals
                    </div>

                    <p style="margin-top:18px;">
                        Based on the skills, technologies,
                        and keywords identified in your resume.
                    </p>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # SKILLS
    # ========================================================

    st.markdown(
        '<div class="content-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">🛠️ Skills Detected</div>',
        unsafe_allow_html=True
    )

    if resume_skills:

        skills_html = ""

        for skill in resume_skills:

            skills_html += (
                f'<span class="skill-pill">'
                f'{html.escape(skill)}'
                f'</span>'
            )

        st.markdown(
            skills_html,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No recognized skills were detected."
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # MATCHING SKILLS
    # ========================================================

    match_col, recommend_col = st.columns(
        2,
        gap="large"
    )

    with match_col:

        st.markdown(
            '<div class="content-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="card-title">🤝 Skills Matching the Job</div>',
            unsafe_allow_html=True
        )

        if matched_skills:

            matched_html = ""

            for skill in matched_skills:

                matched_html += (
                    f'<span class="skill-pill match">'
                    f'✓ {html.escape(skill)}'
                    f'</span>'
                )

            st.markdown(
                matched_html,
                unsafe_allow_html=True
            )

        else:

            st.warning(
                "No direct skill matches were detected."
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    with recommend_col:

        st.markdown(
            '<div class="content-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="card-title">💡 Recommended Skills</div>',
            unsafe_allow_html=True
        )

        if recommended_skills:

            recommended_html = ""

            for skill in recommended_skills:

                recommended_html += (
                    f'<span class="skill-pill recommended">'
                    f'+ {html.escape(skill)}'
                    f'</span>'
                )

            st.markdown(
                recommended_html,
                unsafe_allow_html=True
            )

        else:

            st.success(
                "Great! No major missing job skills detected."
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # ========================================================
    # SUGGESTIONS
    # ========================================================

    st.markdown(
        '<div class="content-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">✨ Smart Resume Suggestions</div>',
        unsafe_allow_html=True
    )

    for suggestion in suggestions:

        st.markdown(
            f"""
            <div class="suggestion">
                💡 {html.escape(suggestion)}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SCORE BREAKDOWN
    # ========================================================

    st.markdown(
        '<div class="content-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">📊 Score Breakdown</div>',
        unsafe_allow_html=True
    )

    b1, b2, b3 = st.columns(3)

    with b1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Content Quality
                </div>
                <div class="metric-value">
                    {min(100, round(45 + len(resume_text) / 80))}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with b2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Skill Relevance
                </div>
                <div class="metric-value">
                    {skill_match}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with b3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Keyword Relevance
                </div>
                <div class="metric-value">
                    {keyword_match}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # CAREER PROFILES
    # ========================================================

    if len(profiles) > 1:

        st.markdown(
            '<div class="content-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="card-title">🚀 Other Suitable Career Profiles</div>',
            unsafe_allow_html=True
        )

        profile_html = ""

        for profile, score in profiles:

            profile_html += f"""
            <div class="suggestion">
                <strong>{html.escape(profile)}</strong>
                — {score} matching signals
            </div>
            """

        st.markdown(
            profile_html,
            unsafe_allow_html=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # ========================================================
    # EXTRACTED TEXT
    # ========================================================

    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.text_area(
            "Extracted text",
            resume_text,
            height=350,
            label_visibility="collapsed"
        )

    if used_ocr:

        st.caption(
            "🔎 OCR was used to extract text from your PDF."
        )


    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    report = f"""
ResumeAI - Resume Analysis Report
=================================

Overall ATS Score: {overall_score}%
Skill Match: {skill_match}%
Keyword Match: {keyword_match}%

Detected Career Profile:
{primary_profile}

Skills Detected:
{", ".join(resume_skills)}

Matching Job Skills:
{", ".join(matched_skills)}

Recommended Skills:
{", ".join(recommended_skills)}

Suggestions:
{"".join(chr(10) + "- " + suggestion for suggestion in suggestions)}

Generated by ResumeAI
Multimodal RAG-Based Resume & Job Analyzer
"""

    st.download_button(
        "📥 Download Resume Analysis Report",
        data=report,
        file_name="ResumeAI_Analysis_Report.txt",
        mime="text/plain",
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    <div class="footer-brand">
        🚀 ResumeAI
    </div>

    <div class="footer-text">
        Multimodal Resume & Job Intelligence
    </div>

    <div class="footer-text">
        Built with AI • Streamlit • Python • OCR
    </div>

    <div class="footer-highlight">
        ✦ Analyze. Improve. Get Career-Ready. ✦
    </div>

</div>
""", unsafe_allow_html=True)
