import streamlit as st
import io
import re
import html
from PIL import Image

# ============================================================
# PDF / OCR IMPORTS
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
# PREMIUM COLORFUL UI
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 5% 5%, rgba(124,58,237,0.30), transparent 25%),
        radial-gradient(circle at 95% 5%, rgba(6,182,212,0.25), transparent 25%),
        radial-gradient(circle at 50% 45%, rgba(236,72,153,0.12), transparent 30%),
        radial-gradient(circle at 80% 90%, rgba(59,130,246,0.20), transparent 30%),
        linear-gradient(135deg, #050816 0%, #0b1026 50%, #090d1c 100%);
    color: #ffffff;
}

.block-container {
    max-width: 1280px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    text-align: center;
    padding: 65px 25px 50px;
}

.hero-tag {
    display: inline-block;
    padding: 10px 22px;
    border-radius: 50px;

    background: linear-gradient(
        90deg,
        rgba(124,58,237,0.22),
        rgba(6,182,212,0.18)
    );

    border: 1px solid rgba(167,139,250,0.45);

    color: #ddd6fe;

    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;

    box-shadow: 0 0 25px rgba(124,58,237,0.20);

    margin-bottom: 22px;
}

.hero h1 {
    font-size: 72px;
    font-weight: 900;

    margin: 0;
    letter-spacing: -3px;

    background: linear-gradient(
        90deg,
        #ffffff 0%,
        #c4b5fd 25%,
        #67e8f9 55%,
        #f0abfc 80%,
        #ffffff 100%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    filter: drop-shadow(
        0 0 20px rgba(139,92,246,0.35)
    );
}

.hero h2 {
    margin-top: 15px;

    font-size: 26px;
    font-weight: 700;

    background: linear-gradient(
        90deg,
        #a78bfa,
        #67e8f9,
        #f0abfc
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 820px;

    margin: 20px auto 0;

    color: #b8c4d9;

    font-size: 16px;
    line-height: 1.8;
}


/* ============================================================
   SECTION TITLE
   ============================================================ */

.section-title {
    text-align: center;

    font-size: 30px;
    font-weight: 900;

    margin: 45px 0 28px;

    background: linear-gradient(
        90deg,
        #c4b5fd,
        #67e8f9,
        #f9a8d4
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-card {
    position: relative;

    min-height: 225px;

    padding: 28px;

    border-radius: 24px;

    background:
        linear-gradient(
            145deg,
            rgba(30,41,80,0.90),
            rgba(15,23,50,0.92)
        );

    border: 1px solid rgba(129,140,248,0.25);

    box-shadow:
        0 12px 35px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.05);

    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border 0.3s ease;

    overflow: hidden;
}

.feature-card:hover {
    transform: translateY(-9px);

    border-color: rgba(103,232,249,0.55);

    box-shadow:
        0 20px 50px rgba(99,102,241,0.25),
        0 0 25px rgba(103,232,249,0.10);
}

.feature-icon {
    width: 58px;
    height: 58px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 17px;

    font-size: 30px;

    background: linear-gradient(
        135deg,
        rgba(124,58,237,0.30),
        rgba(6,182,212,0.20)
    );

    border: 1px solid rgba(167,139,250,0.30);

    box-shadow:
        0 8px 25px rgba(124,58,237,0.18);

    margin-bottom: 18px;
}

.feature-title {
    font-size: 18px;

    font-weight: 800;

    color: #ffffff;

    margin-bottom: 11px;
}

.feature-text {
    font-size: 14px;

    line-height: 1.7;

    color: #aebbd0;
}


/* ============================================================
   ANALYSIS BOX
   ============================================================ */

.analysis-box {
    position: relative;

    margin-top: 50px;

    padding: 40px;

    border-radius: 30px;

    background:
        linear-gradient(
            135deg,
            rgba(30,41,90,0.90),
            rgba(18,24,55,0.94)
        );

    border: 1px solid rgba(139,92,246,0.38);

    box-shadow:
        0 25px 80px rgba(0,0,0,0.35),
        0 0 40px rgba(99,102,241,0.10);

    overflow: hidden;
}

.analysis-title {
    font-size: 32px;

    font-weight: 900;

    background: linear-gradient(
        90deg,
        #ffffff,
        #c4b5fd,
        #67e8f9
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.analysis-subtitle {
    margin-top: 10px;

    color: #aebbd0;

    font-size: 15px;

    line-height: 1.7;
}


/* ============================================================
   UPLOAD LABEL
   ============================================================ */

.upload-label {
    font-size: 18px;

    font-weight: 800;

    color: #ffffff;

    margin-bottom: 8px;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {
    background:
        linear-gradient(
            135deg,
            rgba(79,70,229,0.12),
            rgba(6,182,212,0.08)
        );

    border: 1px dashed rgba(129,140,248,0.55);

    border-radius: 18px;

    padding: 8px;
}

[data-testid="stFileUploader"]:hover {
    border-color: #67e8f9;

    box-shadow:
        0 0 25px rgba(103,232,249,0.10);
}


/* ============================================================
   TEXT AREA
   ============================================================ */

textarea {
    border-radius: 17px !important;

    background: rgba(10,15,35,0.85) !important;

    border: 1px solid rgba(129,140,248,0.30) !important;

    color: #ffffff !important;
}

textarea:focus {
    border-color: #67e8f9 !important;

    box-shadow:
        0 0 20px rgba(103,232,249,0.15) !important;
}


/* ============================================================
   ANALYZE BUTTON
   ============================================================ */

.stButton > button {
    width: 100%;

    min-height: 58px;

    border: none;

    border-radius: 17px;

    font-size: 17px;

    font-weight: 900;

    color: #ffffff;

    background:
        linear-gradient(
            90deg,
            #7c3aed,
            #6366f1,
            #06b6d4,
            #8b5cf6
        );

    background-size: 250% 100%;

    box-shadow:
        0 12px 35px rgba(99,102,241,0.35);

    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);

    background-position: 100% 0;

    box-shadow:
        0 18px 45px rgba(124,58,237,0.40);
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

.metric-card {
    text-align: center;

    padding: 30px 15px;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(30,41,80,0.88),
            rgba(15,23,50,0.92)
        );

    border: 1px solid rgba(129,140,248,0.25);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.25);
}

.metric-number {
    font-size: 43px;

    font-weight: 900;

    background: linear-gradient(
        90deg,
        #a78bfa,
        #67e8f9
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-label {
    color: #94a3b8;

    font-size: 14px;

    margin-top: 7px;
}


/* ============================================================
   RESULT CARDS
   ============================================================ */

.result-card {
    padding: 27px;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(25,34,70,0.86),
            rgba(10,16,35,0.92)
        );

    border: 1px solid rgba(129,140,248,0.20);

    margin-bottom: 20px;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.20);
}

.result-title {
    font-size: 21px;

    font-weight: 850;

    margin-bottom: 16px;

    color: #ffffff;
}


/* ============================================================
   SKILL PILLS
   ============================================================ */

.skill-pill {
    display: inline-block;

    padding: 8px 14px;

    margin: 4px;

    border-radius: 30px;

    background:
        linear-gradient(
            90deg,
            rgba(124,58,237,0.20),
            rgba(6,182,212,0.14)
        );

    border: 1px solid rgba(129,140,248,0.30);

    color: #ddd6fe;

    font-size: 13px;

    font-weight: 600;
}


/* ============================================================
   DOWNLOAD BUTTON
   ============================================================ */

.stDownloadButton > button {
    width: 100%;

    min-height: 52px;

    border-radius: 15px;

    border: 1px solid rgba(103,232,249,0.35);

    background:
        linear-gradient(
            90deg,
            rgba(6,182,212,0.18),
            rgba(124,58,237,0.20)
        );

    color: #ffffff;

    font-weight: 750;
}

.stDownloadButton > button:hover {
    border-color: #67e8f9;
}


/* ============================================================
   EXPANDER
   ============================================================ */

[data-testid="stExpander"] {
    border-radius: 18px !important;

    border: 1px solid rgba(129,140,248,0.22) !important;

    background: rgba(15,23,50,0.70) !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;

    margin-top: 75px;

    padding: 45px 20px;

    border-top: 1px solid rgba(129,140,248,0.18);
}

.footer-brand {
    font-size: 28px;

    font-weight: 900;

    background: linear-gradient(
        90deg,
        #c4b5fd,
        #67e8f9,
        #f0abfc
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.footer-title {
    margin-top: 7px;

    color: #c4b5fd;

    font-weight: 700;

    font-size: 15px;
}

.footer-text {
    max-width: 600px;

    margin: 14px auto 0;

    color: #7f8da5;

    font-size: 14px;

    line-height: 1.7;
}

.footer-line {
    margin-top: 20px;

    font-size: 14px;

    font-weight: 800;

    background: linear-gradient(
        90deg,
        #a78bfa,
        #67e8f9,
        #f0abfc
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


/* ============================================================
   STREAMLIT CLEANUP
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .hero {
        padding-top: 35px;
    }

    .hero h1 {
        font-size: 45px;
    }

    .hero h2 {
        font-size: 20px;
    }

    .analysis-box {
        padding: 25px;
    }

    .analysis-title {
        font-size: 25px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SKILLS DATABASE
# ============================================================

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


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_bytes):

    if pymupdf is None:
        return ""

    try:

        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        text = ""

        for page in document:
            text += page.get_text("text") + "\n"

        document.close()

        if len(text.strip()) >= 100:
            return text.strip()

        return "OCR_REQUIRED"

    except Exception:
        return "OCR_REQUIRED"


# ============================================================
# OCR EXTRACTION
# ============================================================

def extract_ocr_text(pdf_bytes):

    if pymupdf is None or pytesseract is None:
        return ""

    try:

        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        full_text = ""

        for page in document:

            pix = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2),
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

            full_text += page_text + "\n"

        document.close()

        return full_text.strip()

    except Exception:
        return ""


# ============================================================
# PROCESS RESUME
# ============================================================

def process_resume(pdf_bytes):

    normal_text = extract_pdf_text(pdf_bytes)

    if normal_text and normal_text != "OCR_REQUIRED":
        return normal_text, False

    ocr_text = extract_ocr_text(pdf_bytes)

    if ocr_text:
        return ocr_text, True

    return "", False


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text):

    text_lower = text.lower()

    found = []

    for skill in SKILLS:

        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(skill.lower())
            + r"(?![a-zA-Z0-9])"
        )

        if re.search(pattern, text_lower):

            if skill not in found:
                found.append(skill)

    return found


# ============================================================
# KEYWORD EXTRACTION
# ============================================================

def extract_keywords(text):

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z+#.-]{2,}\b",
        text.lower()
    )

    stopwords = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "this",
        "that",
        "are",
        "you",
        "your",
        "our",
        "will",
        "have",
        "has",
        "using",
        "use",
        "into",
        "about",
        "their",
        "they",
        "can",
        "job",
        "work",
        "role",
        "candidate",
        "should"
    }

    keywords = []

    for word in words:

        if word not in stopwords and word not in keywords:
            keywords.append(word)

    return keywords[:100]


# ============================================================
# SCORE CALCULATION
# ============================================================

def calculate_scores(
    resume_text,
    job_description,
    resume_skills,
    job_skills
):

    if not job_description.strip():

        skill_match = 0
        keyword_match = 0

    else:

        job_skill_names = {
            skill.lower()
            for skill in job_skills
        }

        resume_skill_names = {
            skill.lower()
            for skill in resume_skills
        }

        if job_skill_names:

            matched = (
                resume_skill_names
                .intersection(job_skill_names)
            )

            skill_match = round(
                len(matched)
                / len(job_skill_names)
                * 100
            )

        else:

            skill_match = 50


        resume_keywords = set(
            extract_keywords(resume_text)
        )

        job_keywords = set(
            extract_keywords(job_description)
        )

        if job_keywords:

            matched_keywords = (
                resume_keywords
                .intersection(job_keywords)
            )

            keyword_match = round(
                len(matched_keywords)
                / len(job_keywords)
                * 100
            )

        else:

            keyword_match = 50


    content_score = min(
        100,
        round(45 + len(resume_text) / 80)
    )

    overall = round(
        skill_match * 0.45
        + keyword_match * 0.30
        + content_score * 0.25
    )

    overall = min(100, overall)

    return (
        overall,
        skill_match,
        keyword_match,
        content_score
    )


# ============================================================
# PROFILE DETECTION
# ============================================================

def detect_profile(text):

    text_lower = text.lower()

    profiles = []

    profile_keywords = {

        "Data Analyst": [
            "data analyst",
            "data analysis",
            "power bi",
            "tableau",
            "excel",
            "sql",
            "pandas"
        ],

        "AI / ML Engineer": [
            "machine learning",
            "artificial intelligence",
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "deep learning"
        ],

        "Software Developer": [
            "software developer",
            "software engineer",
            "java",
            "python",
            "c++",
            "javascript"
        ],

        "Web Developer": [
            "html",
            "css",
            "javascript",
            "react",
            "node.js"
        ],

        "Data Scientist": [
            "data science",
            "statistics",
            "machine learning",
            "pandas",
            "numpy"
        ],

        "AI / GenAI Developer": [
            "generative ai",
            "llm",
            "rag",
            "nlp",
            "large language model"
        ]
    }

    for profile, keywords in profile_keywords.items():

        score = sum(
            1
            for keyword in keywords
            if keyword in text_lower
        )

        if score >= 2:
            profiles.append(
                (profile, score)
            )

    profiles.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return [
        profile
        for profile, score in profiles[:3]
    ]


# ============================================================
# SMART SUGGESTIONS
# ============================================================

def generate_suggestions(
    resume_text,
    resume_skills,
    job_skills,
    overall_score
):

    suggestions = []

    resume_lower = resume_text.lower()

    missing_skills = [
        skill
        for skill in job_skills
        if skill.lower() not in resume_lower
    ]

    if overall_score < 60:

        suggestions.append(
            "Improve your resume with more job-specific keywords and measurable achievements."
        )

    elif overall_score < 80:

        suggestions.append(
            "Your resume has a good foundation. Add more role-specific keywords to improve ATS matching."
        )

    else:

        suggestions.append(
            "Your resume shows strong alignment with the target role. Keep the content concise and achievement-focused."
        )


    if "project" not in resume_lower:

        suggestions.append(
            "Add relevant academic or personal projects with technologies and measurable outcomes."
        )


    if "experience" not in resume_lower:

        suggestions.append(
            "Include internships, practical experience, volunteering, or project-based experience where applicable."
        )


    if "education" not in resume_lower:

        suggestions.append(
            "Make sure your education section clearly lists your degree and relevant academic details."
        )


    if missing_skills:

        suggestions.append(
            "Consider highlighting relevant skills such as: "
            + ", ".join(missing_skills[:8])
            + "."
        )

    return suggestions[:5], missing_skills


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

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

</div>
""", unsafe_allow_html=True)


# ============================================================
# FEATURES
# ============================================================

st.markdown(
    '<div class="section-title">✨ Powerful Resume Intelligence</div>',
    unsafe_allow_html=True
)

features = [

    (
        "📄",
        "Smart Resume Parsing",
        "Automatically extract and understand key information, skills, education, and experience from your resume."
    ),

    (
        "🎯",
        "AI Resume Scoring",
        "Get an instant resume score with ATS compatibility and actionable insights to strengthen your profile."
    ),

    (
        "🧠",
        "Career Profile Analysis",
        "Identify your career profile and discover job roles that best match your skills and experience."
    ),

    (
        "📊",
        "Intelligent Skill Analytics",
        "Discover your technical and professional strengths, matched skills, and important skill gaps."
    ),

    (
        "💡",
        "AI-Powered Suggestions",
        "Receive personalized recommendations to improve your resume, strengthen your skills, and become more job-ready."
    )
]


cols = st.columns(5)

for col, feature in zip(cols, features):

    icon, title, description = feature

    with col:

        st.markdown(
            f"""
            <div class="feature-card">

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


# ============================================================
# ANALYSIS HEADER
# ============================================================

st.markdown("""
<div class="analysis-box">

    <div class="analysis-title">
        🔍 Start Your Resume Analysis
    </div>

    <div class="analysis-subtitle">
        Upload your resume and provide a target job description.
        ResumeAI will analyze your profile and show how well your
        resume matches the role.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# INPUTS
# ============================================================

col1, col2 = st.columns(2, gap="large")


with col1:

    st.markdown(
        '<div class="upload-label">📄 Upload Your Resume</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Upload your PDF resume and let ResumeAI analyze your profile, skills, keywords, and career potential."
    )

    uploaded_file = st.file_uploader(
        "Choose your resume",
        type=["pdf"],
        label_visibility="collapsed"
    )

    st.caption(
        "200MB per file • PDF format supported"
    )


with col2:

    st.markdown(
        '<div class="upload-label">💼 Job Description</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Paste the job description you are targeting. ResumeAI will compare your profile with the role."
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=220,
        placeholder=(
            "Paste the job description here...\n\n"
            "Example:\n"
            "Python, SQL, Pandas, Power BI, "
            "Data Analysis, Machine Learning..."
        ),
        label_visibility="collapsed"
    )


# ============================================================
# BUTTON
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

analyze = st.button(
    "🚀 Analyze My Resume"
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    if uploaded_file is None:

        st.error(
            "📄 Please upload your PDF resume first."
        )

    else:

        with st.spinner(
            "🤖 ResumeAI is analyzing your resume..."
        ):

            pdf_bytes = uploaded_file.read()

            resume_text, used_ocr = process_resume(
                pdf_bytes
            )

        if not resume_text:

            st.error(
                "❌ Unable to extract text from this PDF. "
                "Please upload a readable PDF."
            )

        else:

            if used_ocr:

                st.success(
                    "✅ Resume successfully analyzed using OCR."
                )

            else:

                st.success(
                    "✅ Resume text successfully extracted."
                )


            # ====================================================
            # EXTRACT DATA
            # ====================================================

            resume_skills = extract_skills(
                resume_text
            )

            job_skills = extract_skills(
                job_description
            )


            (
                overall_score,
                skill_match,
                keyword_match,
                content_score
            ) = calculate_scores(
                resume_text,
                job_description,
                resume_skills,
                job_skills
            )


            profiles = detect_profile(
                resume_text
            )


            suggestions, missing_skills = generate_suggestions(
                resume_text,
                resume_skills,
                job_skills,
                overall_score
            )


            # ====================================================
            # RESULT TITLE
            # ====================================================

            st.markdown(
                '<div class="section-title">📈 Your Resume Intelligence Report</div>',
                unsafe_allow_html=True
            )


            # ====================================================
            # METRICS
            # ====================================================

            m1, m2, m3, m4 = st.columns(4)


            with m1:

                st.markdown(
                    f"""
                    <div class="metric-card">

                        <div class="metric-number">
                            {overall_score}%
                        </div>

                        <div class="metric-label">
                            Overall ATS Score
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            with m2:

                st.markdown(
                    f"""
                    <div class="metric-card">

                        <div class="metric-number">
                            {skill_match}%
                        </div>

                        <div class="metric-label">
                            Skill Match
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            with m3:

                st.markdown(
                    f"""
                    <div class="metric-card">

                        <div class="metric-number">
                            {keyword_match}%
                        </div>

                        <div class="metric-label">
                            Keyword Match
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            with m4:

                st.markdown(
                    f"""
                    <div class="metric-card">

                        <div class="metric-number">
                            {len(resume_skills)}
                        </div>

                        <div class="metric-label">
                            Skills Detected
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            st.markdown("<br>", unsafe_allow_html=True)


            # ====================================================
            # PROFILE + SKILLS
            # ====================================================

            left, right = st.columns(2, gap="large")


            with left:

                st.markdown(
                    """
                    <div class="result-card">

                        <div class="result-title">
                            🧠 Detected Career Profile
                        </div>
                    """,
                    unsafe_allow_html=True
                )

                if profiles:

                    for profile in profiles:

                        st.markdown(
                            f"""
                            <span class="skill-pill">
                                🎯 {html.escape(profile)}
                            </span>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.info(
                        "Add more role-specific information to your resume for better profile detection."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            with right:

                st.markdown(
                    """
                    <div class="result-card">

                        <div class="result-title">
                            🛠️ Skills Detected
                        </div>
                    """,
                    unsafe_allow_html=True
                )

                if resume_skills:

                    for skill in resume_skills:

                        st.markdown(
                            f"""
                            <span class="skill-pill">
                                {html.escape(skill)}
                            </span>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.info(
                        "No predefined skills detected."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            # ====================================================
            # JOB MATCH
            # ====================================================

            matched_skills = []

            if job_description.strip():

                resume_skill_lower = {
                    skill.lower(): skill
                    for skill in resume_skills
                }

                job_skill_lower = {
                    skill.lower(): skill
                    for skill in job_skills
                }

                matched_keys = set(
                    resume_skill_lower.keys()
                ).intersection(
                    job_skill_lower.keys()
                )

                matched_skills = [
                    resume_skill_lower[key]
                    for key in matched_keys
                ]


                # ------------------------------------------------
                # MATCHED SKILLS
                # ------------------------------------------------

                st.markdown(
                    """
                    <div class="result-card">

                        <div class="result-title">
                            🤝 Skills Matching the Job
                        </div>
                    """,
                    unsafe_allow_html=True
                )

                if matched_skills:

                    for skill in matched_skills:

                        st.markdown(
                            f"""
                            <span class="skill-pill">
                                ✅ {html.escape(skill)}
                            </span>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.warning(
                        "No direct skill matches were found."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


                # ------------------------------------------------
                # MISSING SKILLS
                # ------------------------------------------------

                st.markdown(
                    """
                    <div class="result-card">

                        <div class="result-title">
                            📌 Recommended Skills
                        </div>
                    """,
                    unsafe_allow_html=True
                )

                if missing_skills:

                    for skill in missing_skills[:12]:

                        st.markdown(
                            f"""
                            <span class="skill-pill">
                                💡 {html.escape(skill)}
                            </span>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.success(
                        "🎉 Your resume already contains the main detected job skills."
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            # ====================================================
            # SMART SUGGESTIONS
            # ====================================================

            st.markdown(
                """
                <div class="result-card">

                    <div class="result-title">
                        💡 Smart Resume Suggestions
                    </div>
                """,
                unsafe_allow_html=True
            )

            for suggestion in suggestions:

                st.markdown(
                    f"""
                    <div style="
                        padding: 14px 17px;
                        margin: 9px 0;
                        border-radius: 13px;

                        background:
                            linear-gradient(
                                90deg,
                                rgba(124,58,237,0.12),
                                rgba(6,182,212,0.08)
                            );

                        border:
                            1px solid
                            rgba(129,140,248,0.16);

                        color: #d5def0;
                    ">
                        ✦ {html.escape(suggestion)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


            # ====================================================
            # SCORE BREAKDOWN
            # ====================================================

            st.markdown(
                """
                <div class="result-card">

                    <div class="result-title">
                        📊 Score Breakdown
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            s1, s2, s3 = st.columns(3)


            with s1:

                st.metric(
                    "Skill Compatibility",
                    f"{skill_match}%"
                )


            with s2:

                st.metric(
                    "Keyword Relevance",
                    f"{keyword_match}%"
                )


            with s3:

                st.metric(
                    "Resume Content",
                    f"{content_score}%"
                )


            # ====================================================
            # EXTRACTED TEXT
            # ====================================================

            with st.expander(
                "📄 View Extracted Resume Text"
            ):

                st.text_area(
                    "Extracted Content",
                    resume_text,
                    height=400,
                    label_visibility="collapsed"
                )


            # ====================================================
            # DOWNLOAD REPORT
            # ====================================================

            report = f"""
============================================================
                        RESUMEAI
              MULTIMODAL RESUME INTELLIGENCE
============================================================

OVERALL ATS SCORE
{overall_score}%

SKILL MATCH
{skill_match}%

KEYWORD MATCH
{keyword_match}%

CONTENT SCORE
{content_score}%

------------------------------------------------------------
DETECTED CAREER PROFILES
------------------------------------------------------------

{", ".join(profiles) if profiles else "Not detected"}

------------------------------------------------------------
SKILLS DETECTED
------------------------------------------------------------

{", ".join(resume_skills) if resume_skills else "None"}

------------------------------------------------------------
MATCHED JOB SKILLS
------------------------------------------------------------

{", ".join(matched_skills) if matched_skills else "None"}

------------------------------------------------------------
RECOMMENDED SKILLS
------------------------------------------------------------

{", ".join(missing_skills) if missing_skills else "None"}

------------------------------------------------------------
SMART SUGGESTIONS
------------------------------------------------------------

{"".join(chr(10) + "- " + suggestion for suggestion in suggestions)}

------------------------------------------------------------
EXTRACTED RESUME TEXT
------------------------------------------------------------

{resume_text}

============================================================
              Analyze. Improve. Get Career-Ready.
============================================================
"""


            st.download_button(
                label="📥 Download Resume Analysis Report",
                data=report,
                file_name="ResumeAI_Analysis_Report.txt",
                mime="text/plain"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    <div class="footer-brand">
        🚀 ResumeAI
    </div>

    <div class="footer-title">
        Multimodal Resume & Job Intelligence
    </div>

    <div class="footer-text">
        Built with AI to help you understand your potential,
        improve your resume, and prepare smarter for your career.
    </div>

    <div class="footer-line">
        ✦ Analyze. Improve. Get Career-Ready. ✦
    </div>

</div>
""", unsafe_allow_html=True)
