import streamlit as st
import io
import re
from PIL import Image

# =========================================================
# OPTIONAL LIBRARIES
# =========================================================

try:
    import pymupdf
except ImportError:
    pymupdf = None

try:
    import pytesseract
except ImportError:
    pytesseract = None


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ResumeAI | Career Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# SAFE CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(124,58,237,.22), transparent 25%),
            radial-gradient(circle at 90% 15%, rgba(6,182,212,.18), transparent 25%),
            linear-gradient(135deg, #070b18, #10172a, #0b1220);
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* TOP BAR */
    .topbar {
        padding: 12px 18px;
        border-radius: 16px;
        background: rgba(15,23,42,.75);
        border: 1px solid rgba(255,255,255,.10);
        margin-bottom: 20px;
    }

    .topbar-title {
        font-size: 19px;
        font-weight: 800;
        color: white;
    }

    .topbar-sub {
        font-size: 11px;
        color: #94a3b8;
        margin-top: 2px;
    }

    /* HERO */
    .hero-box {
        padding: 45px 42px;
        border-radius: 28px;
        background:
            linear-gradient(
                135deg,
                rgba(124,58,237,.35),
                rgba(15,23,42,.92) 55%,
                rgba(6,182,212,.20)
            );
        border: 1px solid rgba(255,255,255,.12);
        box-shadow: 0 25px 70px rgba(0,0,0,.30);
        margin-bottom: 28px;
    }

    .hero-tag {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 20px;
        background: rgba(139,92,246,.18);
        border: 1px solid rgba(167,139,250,.30);
        color: #ddd6fe;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .hero-title {
        font-size: 58px;
        line-height: 1;
        font-weight: 900;
        margin: 16px 0 8px;
        color: white;
    }

    .hero-subtitle {
        font-size: 23px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 14px;
    }

    .hero-description {
        max-width: 780px;
        color: #cbd5e1;
        font-size: 15px;
        line-height: 1.7;
    }

    /* CHIPS */
    .chip {
        display: inline-block;
        padding: 7px 11px;
        margin: 4px 4px 0 0;
        border-radius: 20px;
        background: rgba(255,255,255,.08);
        border: 1px solid rgba(255,255,255,.10);
        color: #e2e8f0;
        font-size: 11px;
        font-weight: 700;
    }

    /* SECTION */
    .section-box {
        text-align: center;
        margin: 38px 0 22px;
    }

    .section-label {
        color: #67e8f9;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 2px;
    }

    .section-title {
        color: white;
        font-size: 30px;
        font-weight: 850;
        margin: 5px 0;
    }

    .section-description {
        color: #94a3b8;
        font-size: 13px;
    }

    /* FEATURE CARD */
    .feature {
        min-height: 190px;
        padding: 23px;
        border-radius: 20px;
        background: rgba(15,23,42,.80);
        border: 1px solid rgba(255,255,255,.09);
        box-shadow: 0 12px 30px rgba(0,0,0,.18);
    }

    .feature-icon {
        font-size: 28px;
        margin-bottom: 12px;
    }

    .feature-title {
        color: white;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .feature-text {
        color: #94a3b8;
        font-size: 12px;
        line-height: 1.6;
    }

    /* INPUT CARDS */
    .input-card {
        padding: 20px;
        border-radius: 20px;
        background: rgba(15,23,42,.75);
        border: 1px solid rgba(255,255,255,.09);
        min-height: 110px;
    }

    .input-title {
        color: white;
        font-size: 18px;
        font-weight: 800;
    }

    .input-description {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 5px;
    }

    /* RESULTS */
    .result-card {
        padding: 20px;
        border-radius: 19px;
        background: rgba(15,23,42,.80);
        border: 1px solid rgba(255,255,255,.09);
    }

    .result-label {
        color: #94a3b8;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .result-number {
        color: white;
        font-size: 32px;
        font-weight: 900;
        margin-top: 5px;
    }

    .result-small {
        color: #64748b;
        font-size: 11px;
    }

    /* PROFILE */
    .profile-card {
        padding: 24px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            rgba(124,58,237,.18),
            rgba(6,182,212,.08)
        );
        border: 1px solid rgba(167,139,250,.18);
    }

    .profile-name {
        color: white;
        font-size: 26px;
        font-weight: 900;
    }

    .profile-info {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 7px;
    }

    /* SKILLS */
    .skill {
        display: inline-block;
        padding: 7px 11px;
        margin: 3px;
        border-radius: 20px;
        color: #ddd6fe;
        background: rgba(139,92,246,.13);
        border: 1px solid rgba(139,92,246,.25);
        font-size: 11px;
        font-weight: 700;
    }

    .skill-match {
        color: #a7f3d0;
        background: rgba(16,185,129,.12);
        border-color: rgba(16,185,129,.25);
    }

    .skill-recommend {
        color: #bae6fd;
        background: rgba(6,182,212,.12);
        border-color: rgba(6,182,212,.25);
    }

    /* SUGGESTION */
    .suggestion {
        padding: 13px 15px;
        margin: 8px 0;
        border-radius: 13px;
        background: rgba(245,158,11,.08);
        border-left: 3px solid #f59e0b;
        color: #cbd5e1;
        font-size: 12px;
        line-height: 1.6;
    }

    /* FOOTER */
    .footer {
        text-align: center;
        padding: 28px;
        margin-top: 45px;
        border-radius: 22px;
        background: rgba(15,23,42,.65);
        border: 1px solid rgba(255,255,255,.08);
    }

    .footer-title {
        color: white;
        font-size: 20px;
        font-weight: 900;
    }

    .footer-text {
        color: #64748b;
        font-size: 12px;
        margin-top: 5px;
    }

    .footer-highlight {
        color: #67e8f9;
        font-size: 11px;
        font-weight: 800;
        margin-top: 13px;
    }

    /* BUTTON */
    .stButton > button {
        min-height: 52px;
        border-radius: 15px;
        border: none;
        color: white;
        font-weight: 800;
        background: linear-gradient(
            100deg,
            #7c3aed,
            #2563eb,
            #06b6d4
        );
        box-shadow: 0 10px 25px rgba(37,99,235,.25);
    }

    .stButton > button:hover {
        border: none;
        color: white;
        transform: translateY(-2px);
    }

    .stTextArea textarea {
        background: rgba(2,6,23,.75) !important;
        color: white !important;
        border-radius: 14px !important;
        border: 1px solid rgba(6,182,212,.25) !important;
    }

    @media(max-width:768px) {
        .hero-box {
            padding: 30px 22px;
        }

        .hero-title {
            font-size: 43px;
        }

        .hero-subtitle {
            font-size: 18px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TOP BAR
# =========================================================

st.markdown(
    """
    <div class="topbar">
        <div class="topbar-title">🚀 ResumeAI</div>
        <div class="topbar-sub">
            AI Career Intelligence • Resume • Skills • Jobs
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero-box">

        <div class="hero-tag">
            ✦ AI-POWERED CAREER INTELLIGENCE
        </div>

        <div class="hero-title">
            🚀 ResumeAI
        </div>

        <div class="hero-subtitle">
            Multimodal RAG-Based Resume & Job Analyzer
        </div>

        <div class="hero-description">
            Transform your resume into powerful career insights.
            Analyze your skills, discover your ideal career profile,
            compare job requirements, and receive AI-powered
            recommendations to build a stronger, job-ready resume.
        </div>

        <br>

        <span class="chip">📄 Resume Parsing</span>
        <span class="chip">🎯 ATS Scoring</span>
        <span class="chip">🧠 Career Analysis</span>
        <span class="chip">⚡ Skill Matching</span>
        <span class="chip">✨ Smart Suggestions</span>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SECTION HEADER
# =========================================================

st.markdown(
    """
    <div class="section-box">
        <div class="section-label">POWERFUL AI FEATURES</div>
        <div class="section-title">✨ Powerful Resume Intelligence</div>
        <div class="section-description">
            Everything you need to understand, improve, and optimize
            your resume for today's competitive job market.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FEATURES
# =========================================================

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

feature_columns = st.columns(5)

for i, feature in enumerate(features):

    icon, title, description = feature

    with feature_columns[i]:

        st.markdown(
            f"""
            <div class="feature">

                <div class="feature-icon">
                    {icon}
                </div>

                <div class="feature-title">
                    {title}
                </div>

                <div class="feature-text">
                    {description}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# SKILL DATABASE
# =========================================================

SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Flask",
    "Django",
    "Streamlit",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Azure",
    "GCP",
    "Excel",
    "Power BI",
    "Tableau",
    "PowerPoint",
    "MS Office",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "AI",
    "Data Analysis",
    "Data Analytics",
    "Data Visualization",
    "Statistics",
    "Data Cleaning",
    "Data Preprocessing",
    "Data Mining",
    "NLP",
    "Natural Language Processing",
    "RAG",
    "LLM",
    "Generative AI",
    "Firebase",
    "Communication",
    "Leadership",
    "Problem Solving",
    "Teamwork"
]


# =========================================================
# FUNCTIONS
# =========================================================

def extract_pdf_text(uploaded_file):

    if pymupdf is None:
        return ""

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

        return text

    except Exception:
        return ""


def extract_ocr_text(uploaded_file):

    if pymupdf is None or pytesseract is None:
        return ""

    try:

        pdf_bytes = uploaded_file.getvalue()

        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        pages = []

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

            text = pytesseract.image_to_string(
                image,
                config="--psm 6"
            )

            pages.append(text)

        document.close()

        return "\n".join(pages)

    except Exception:
        return ""


def process_resume(uploaded_file):

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):

        text = extract_pdf_text(uploaded_file)

        if len(text.strip()) >= 80:
            return text, False

        ocr_text = extract_ocr_text(uploaded_file)

        return ocr_text, True

    if filename.endswith(".txt"):

        try:
            text = uploaded_file.getvalue().decode(
                "utf-8",
                errors="ignore"
            )

            return text, False

        except Exception:
            return "", False

    return "", False


def extract_skills(text):

    text_lower = text.lower()

    detected = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(
            skill.lower()
        ) + r"\b"

        if re.search(pattern, text_lower):

            detected.append(skill)

    return detected


def extract_keywords(text):

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z+#.\-]{2,}\b",
        text.lower()
    )

    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "this",
        "that",
        "from",
        "your",
        "you",
        "are",
        "was",
        "were",
        "have",
        "has",
        "will",
        "into",
        "using",
        "our",
        "their",
        "about",
        "which",
        "also",
        "can",
        "job",
        "work"
    }

    frequency = {}

    for word in words:

        if word in stop_words:
            continue

        frequency[word] = frequency.get(
            word,
            0
        ) + 1

    sorted_words = sorted(
        frequency.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        word
        for word, count in sorted_words[:20]
    ]


def calculate_scores(
    resume_text,
    job_text,
    resume_skills
):

    resume_lower = resume_text.lower()

    job_skills = extract_skills(
        job_text
    )

    if job_skills:

        matched = [
            skill
            for skill in job_skills
            if skill.lower() in resume_lower
        ]

        skill_match = round(
            len(matched)
            / len(job_skills)
            * 100
        )

    else:

        skill_match = min(
            100,
            len(resume_skills) * 6
        )

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

        keyword_match = min(
            100,
            len(resume_keywords) * 5
        )

    content_score = min(
        100,
        round(
            45 + len(resume_text) / 80
        )
    )

    overall = round(
        content_score * 0.35
        + skill_match * 0.40
        + keyword_match * 0.25
    )

    overall = max(
        0,
        min(100, overall)
    )

    return (
        overall,
        skill_match,
        keyword_match,
        job_skills
    )


def detect_profile(
    skills,
    text
):

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
    job_skills
):

    suggestions = []

    text_lower = resume_text.lower()

    if len(resume_text) < 500:

        suggestions.append(
            "Add more detailed project, internship, education, and achievement information."
        )

    if "project" not in text_lower:

        suggestions.append(
            "Add 2–3 relevant projects with technologies used and measurable results."
        )

    if (
        "experience" not in text_lower
        and "intern" not in text_lower
    ):

        suggestions.append(
            "Include internship, academic, freelance, or practical experience where applicable."
        )

    if "education" not in text_lower:

        suggestions.append(
            "Make your education section clear and easy for ATS systems to identify."
        )

    missing = [
        skill
        for skill in job_skills
        if skill.lower() not in text_lower
    ]

    if missing:

        suggestions.append(
            "Consider adding relevant missing skills only if you genuinely have experience with them: "
            + ", ".join(missing[:6])
            + "."
        )

    if not suggestions:

        suggestions.append(
            "Your resume has a solid foundation. Focus on measurable achievements and tailoring keywords to each target job."
        )

    return suggestions


# =========================================================
# ANALYSIS SECTION
# =========================================================

st.markdown(
    """
    <div class="section-box">
        <div class="section-label">ANALYSIS WORKSPACE</div>

        <div class="section-title">
            🔍 Start Your Resume Analysis
        </div>

        <div class="section-description">
            Upload your resume and add a target job description
            to discover your skills, match score, career profile,
            and personalized improvement recommendations.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INPUT AREA
# =========================================================

left, right = st.columns(
    2,
    gap="large"
)


with left:

    st.markdown(
        """
        <div class="input-card">

            <div class="input-title">
                📄 Upload Your Resume
            </div>

            <div class="input-description">
                Upload your PDF or TXT resume for AI-powered analysis.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Resume",
        type=["pdf", "txt"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        st.success(
            f"✓ {uploaded_file.name} uploaded"
        )


with right:

    st.markdown(
        """
        <div class="input-card">

            <div class="input-title">
                💼 Job Description
            </div>

            <div class="input-description">
                Paste the target job description to compare your resume.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    job_description = st.text_area(
        "Job Description",
        placeholder=(
            "Paste the target job description here..."
        ),
        height=180,
        label_visibility="collapsed"
    )


st.write("")


analyze_button = st.button(
    "🚀 Analyze My Resume",
    use_container_width=True
)


# =========================================================
# ANALYSIS RESULT
# =========================================================

if analyze_button:

    if uploaded_file is None:

        st.warning(
            "📄 Please upload your resume first."
        )

        st.stop()

    with st.spinner(
        "🔄 Analyzing your resume..."
    ):

        resume_text, used_ocr = process_resume(
            uploaded_file
        )

        if not resume_text.strip():

            st.error(
                "❌ Unable to extract text from this resume."
            )

            st.stop()

        resume_skills = extract_skills(
            resume_text
        )

        (
            overall_score,
            skill_match,
            keyword_match,
            job_skills
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


    # =====================================================
    # RESULT HEADER
    # =====================================================

    if overall_score >= 80:

        result_message = "Excellent Match 🟢"

    elif overall_score >= 65:

        result_message = "Strong Match 🔵"

    elif overall_score >= 50:

        result_message = "Moderate Match 🟡"

    else:

        result_message = "Needs Improvement 🟠"


    st.success(
        f"✨ Resume Analysis Complete — {result_message}"
    )


    # =====================================================
    # METRICS
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">
                    Overall ATS Score
                </div>
                <div class="result-number">
                    {overall_score}%
                </div>
                <div class="result-small">
                    Resume strength
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">
                    Skill Match
                </div>
                <div class="result-number">
                    {skill_match}%
                </div>
                <div class="result-small">
                    Job requirements
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">
                    Keyword Match
                </div>
                <div class="result-number">
                    {keyword_match}%
                </div>
                <div class="result-small">
                    Relevant keywords
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">
                    Skills Detected
                </div>
                <div class="result-number">
                    {len(resume_skills)}
                </div>
                <div class="result-small">
                    Resume skills
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.write("")


    # =====================================================
    # PROFILE
    # =====================================================

    profile_col, score_col = st.columns(
        2,
        gap="large"
    )


    with profile_col:

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
            <div class="profile-card">

                <div class="result-label">
                    DETECTED CAREER PROFILE
                </div>

                <div class="profile-name">
                    🧠 {primary_profile}
                </div>

                <div class="profile-info">
                    Based on the technologies, skills,
                    and keywords found in your resume.
                </div>

                <div class="profile-info">
                    Matching signals: {profile_score}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with score_col:

        st.markdown(
            f"""
            <div class="profile-card">

                <div class="result-label">
                    RESUME HEALTH
                </div>

                <div class="profile-name">
                    {result_message}
                </div>

                <div class="profile-info">
                    Your current resume compatibility score
                    is {overall_score}%.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # DETECTED SKILLS
    # =====================================================

    st.subheader(
        "🛠️ Skills Detected"
    )

    if resume_skills:

        skill_html = ""

        for skill in resume_skills:

            skill_html += (
                f'<span class="skill">'
                f'{skill}'
                f'</span>'
            )

        st.markdown(
            skill_html,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No recognized skills were detected."
        )


    # =====================================================
    # MATCHING / RECOMMENDED
    # =====================================================

    match_col, recommend_col = st.columns(
        2,
        gap="large"
    )


    with match_col:

        st.subheader(
            "🤝 Skills Matching the Job"
        )

        if matched_skills:

            html_text = ""

            for skill in matched_skills:

                html_text += (
                    f'<span class="skill skill-match">'
                    f'✓ {skill}'
                    f'</span>'
                )

            st.markdown(
                html_text,
                unsafe_allow_html=True
            )

        else:

            st.warning(
                "No direct skill matches detected."
            )


    with recommend_col:

        st.subheader(
            "💡 Recommended Skills"
        )

        if recommended_skills:

            html_text = ""

            for skill in recommended_skills:

                html_text += (
                    f'<span class="skill skill-recommend">'
                    f'+ {skill}'
                    f'</span>'
                )

            st.markdown(
                html_text,
                unsafe_allow_html=True
            )

        else:

            st.success(
                "Great! No major missing job skills detected."
            )


    # =====================================================
    # SUGGESTIONS
    # =====================================================

    st.subheader(
        "✨ Smart Resume Suggestions"
    )

    for suggestion in suggestions:

        st.markdown(
            f"""
            <div class="suggestion">
                💡 {suggestion}
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # SCORE BREAKDOWN
    # =====================================================

    st.subheader(
        "📊 Score Breakdown"
    )

    b1, b2, b3 = st.columns(3)

    content_score = min(
        100,
        round(
            45 + len(resume_text) / 80
        )
    )


    with b1:

        st.metric(
            "Content Quality",
            f"{content_score}%"
        )

    with b2:

        st.metric(
            "Skill Relevance",
            f"{skill_match}%"
        )

    with b3:

        st.metric(
            "Keyword Relevance",
            f"{keyword_match}%"
        )


    # =====================================================
    # OTHER PROFILES
    # =====================================================

    if len(profiles) > 1:

        st.subheader(
            "🚀 Other Suitable Career Profiles"
        )

        for profile, score in profiles:

            st.write(
                f"**{profile}** — {score} matching signals"
            )


    # =====================================================
    # OCR MESSAGE
    # =====================================================

    if used_ocr:

        st.info(
            "🔎 OCR was used because your PDF did not contain enough selectable text."
        )


    # =====================================================
    # EXTRACTED TEXT
    # =====================================================

    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.text_area(
            "Extracted resume text",
            resume_text,
            height=350,
            label_visibility="collapsed"
        )


    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================

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
"""

    for suggestion in suggestions:

        report += (
            f"\n- {suggestion}"
        )


    report += """

---------------------------------
ResumeAI
Multimodal Resume & Job Intelligence
Analyze. Improve. Get Career-Ready.
"""


    st.download_button(
        "📥 Download Resume Analysis Report",
        data=report,
        file_name="ResumeAI_Analysis_Report.txt",
        mime="text/plain",
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        <div class="footer-title">
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
    """,
    unsafe_allow_html=True
)
