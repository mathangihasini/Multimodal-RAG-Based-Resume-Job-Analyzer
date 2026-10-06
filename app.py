import streamlit as st
import io
import re
import html
from PIL import Image

# ============================================================
# PDF + OCR IMPORTS
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
    page_title="ResumeAI | Resume & Job Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,0.18), transparent 28%),
        radial-gradient(circle at 90% 15%, rgba(168,85,247,0.16), transparent 30%),
        radial-gradient(circle at 50% 90%, rgba(59,130,246,0.10), transparent 35%),
        #070b17;
    color: #f8fafc;
}

/* Main container */

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Hero */

.hero {
    text-align: center;
    padding: 55px 20px 35px;
}

.hero-tag {
    display: inline-block;
    padding: 9px 18px;
    border: 1px solid rgba(139,92,246,0.45);
    border-radius: 30px;
    background: rgba(139,92,246,0.12);
    color: #c4b5fd;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 64px;
    font-weight: 800;
    margin: 0;
    letter-spacing: -2px;
    background: linear-gradient(
        90deg,
        #ffffff,
        #c4b5fd,
        #93c5fd
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero h2 {
    font-size: 25px;
    margin-top: 12px;
    color: #cbd5e1;
    font-weight: 600;
}

.hero p {
    max-width: 800px;
    margin: 18px auto 0;
    color: #94a3b8;
    font-size: 16px;
    line-height: 1.8;
}


/* Section title */

.section-title {
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    margin: 35px 0 25px;
    color: #f8fafc;
}


/* Feature cards */

.feature-card {
    min-height: 205px;
    padding: 27px;
    border-radius: 22px;
    border: 1px solid rgba(148,163,184,0.14);
    background: linear-gradient(
        145deg,
        rgba(30,41,59,0.72),
        rgba(15,23,42,0.82)
    );
    box-shadow: 0 15px 45px rgba(0,0,0,0.22);
    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-6px);
    border-color: rgba(139,92,246,0.45);
    box-shadow: 0 20px 55px rgba(99,102,241,0.14);
}

.feature-icon {
    font-size: 35px;
    margin-bottom: 15px;
}

.feature-title {
    font-size: 18px;
    font-weight: 750;
    color: #f8fafc;
    margin-bottom: 10px;
}

.feature-text {
    font-size: 14px;
    line-height: 1.65;
    color: #94a3b8;
}


/* Analysis section */

.analysis-box {
    margin-top: 45px;
    padding: 35px;
    border-radius: 28px;
    border: 1px solid rgba(139,92,246,0.25);
    background:
        linear-gradient(
            145deg,
            rgba(30,41,59,0.82),
            rgba(15,23,42,0.92)
        );
    box-shadow: 0 20px 70px rgba(0,0,0,0.25);
}

.analysis-title {
    font-size: 30px;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 8px;
}

.analysis-subtitle {
    color: #94a3b8;
    margin-bottom: 25px;
    line-height: 1.6;
}


/* Upload box */

.upload-label {
    font-size: 17px;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 8px;
}


/* Text area */

textarea {
    border-radius: 15px !important;
}


/* Button */

.stButton > button {
    width: 100%;
    border: none;
    border-radius: 14px;
    padding: 14px 20px;
    font-size: 16px;
    font-weight: 750;
    color: white;
    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6,
        #a855f7
    );
    box-shadow: 0 10px 30px rgba(99,102,241,0.28);
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 40px rgba(139,92,246,0.38);
}


/* Metric cards */

.metric-card {
    text-align: center;
    padding: 28px 15px;
    border-radius: 20px;
    background: rgba(15,23,42,0.82);
    border: 1px solid rgba(148,163,184,0.14);
}

.metric-number {
    font-size: 40px;
    font-weight: 800;
    color: #c4b5fd;
}

.metric-label {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 5px;
}


/* Result cards */

.result-card {
    padding: 25px;
    border-radius: 20px;
    background: rgba(15,23,42,0.82);
    border: 1px solid rgba(148,163,184,0.14);
    margin-bottom: 18px;
}

.result-title {
    font-size: 20px;
    font-weight: 750;
    color: #f8fafc;
    margin-bottom: 15px;
}

.skill-pill {
    display: inline-block;
    padding: 7px 12px;
    margin: 4px;
    border-radius: 20px;
    background: rgba(99,102,241,0.14);
    border: 1px solid rgba(129,140,248,0.25);
    color: #c7d2fe;
    font-size: 13px;
}


/* Footer */

.footer {
    text-align: center;
    margin-top: 65px;
    padding: 35px 20px;
    border-top: 1px solid rgba(148,163,184,0.12);
}

.footer-brand {
    font-size: 23px;
    font-weight: 800;
    color: #f8fafc;
}

.footer-title {
    margin-top: 5px;
    color: #a5b4fc;
    font-weight: 600;
}

.footer-text {
    color: #64748b;
    font-size: 14px;
    margin-top: 12px;
}

.footer-line {
    margin-top: 18px;
    color: #818cf8;
    font-size: 13px;
    font-weight: 600;
}


/* Hide Streamlit menu */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* Responsive */

@media (max-width: 768px) {

    .hero h1 {
        font-size: 43px;
    }

    .hero h2 {
        font-size: 20px;
    }

    .analysis-box {
        padding: 22px;
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

    except Exception as e:
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

        pattern = r"(?<![a-zA-Z0-9])" + re.escape(
            skill.lower()
        ) + r"(?![a-zA-Z0-9])"

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

        if job_skills:

            matched = set(
                skill.lower()
                for skill in resume_skills
            ).intersection(
                set(
                    skill.lower()
                    for skill in job_skills
                )
            )

            skill_match = round(
                len(matched) / len(set(
                    skill.lower()
                    for skill in job_skills
                )) * 100
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
                resume_keywords.intersection(
                    job_keywords
                )
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
        45 + len(resume_text) / 80
    )

    overall = round(
        (
            skill_match * 0.45
            + keyword_match * 0.30
            + content_score * 0.25
        )
    )

    overall = min(100, overall)

    return (
        overall,
        skill_match,
        keyword_match,
        round(content_score)
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
# SUGGESTIONS
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
        if skill.lower()
        not in resume_lower
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
# HERO SECTION
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
# ANALYSIS SECTION
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


col1, col2 = st.columns(2, gap="large")


# ============================================================
# RESUME UPLOAD
# ============================================================

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


# ============================================================
# JOB DESCRIPTION
# ============================================================

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
# ANALYZE BUTTON
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


            # ------------------------------------------------
            # SKILLS
            # ------------------------------------------------

            resume_skills = extract_skills(
                resume_text
            )

            job_skills = extract_skills(
                job_description
            )


            # ------------------------------------------------
            # SCORES
            # ------------------------------------------------

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


            # ------------------------------------------------
            # PROFILE
            # ------------------------------------------------

            profiles = detect_profile(
                resume_text
            )


            # ------------------------------------------------
            # SUGGESTIONS
            # ------------------------------------------------

            suggestions, missing_skills = generate_suggestions(
                resume_text,
                resume_skills,
                job_skills,
                overall_score
            )


            # =================================================
            # RESULTS TITLE
            # =================================================

            st.markdown(
                '<div class="section-title">📈 Your Resume Intelligence Report</div>',
                unsafe_allow_html=True
            )


            # =================================================
            # METRICS
            # =================================================

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


            # =================================================
            # PROFILE + SKILLS
            # =================================================

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
                            <div class="skill-pill">
                                🎯 {html.escape(profile)}
                            </div>
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


            # =================================================
            # MATCHED SKILLS
            # =================================================

            if job_description.strip():

                matched_skills = [
                    skill
                    for skill in resume_skills
                    if skill.lower()
                    in [
                        s.lower()
                        for s in job_skills
                    ]
                ]

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


                # =================================================
                # MISSING SKILLS
                # =================================================

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


            # =================================================
            # SMART SUGGESTIONS
            # =================================================

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
                        padding: 12px 15px;
                        margin: 8px 0;
                        border-radius: 12px;
                        background: rgba(99,102,241,0.08);
                        border: 1px solid rgba(129,140,248,0.12);
                        color: #cbd5e1;
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


            # =================================================
            # SCORE BREAKDOWN
            # =================================================

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

            score1, score2, score3 = st.columns(3)

            with score1:

                st.metric(
                    "Skill Compatibility",
                    f"{skill_match}%"
                )

            with score2:

                st.metric(
                    "Keyword Relevance",
                    f"{keyword_match}%"
                )

            with score3:

                st.metric(
                    "Resume Content",
                    f"{content_score}%"
                )


            # =================================================
            # EXTRACTED TEXT
            # =================================================

            with st.expander(
                "📄 View Extracted Resume Text"
            ):

                st.text_area(
                    "Extracted Content",
                    resume_text,
                    height=400,
                    label_visibility="collapsed"
                )


            # =================================================
            # DOWNLOAD REPORT
            # =================================================

            report = f"""
RESUMEAI
Multimodal Resume & Job Intelligence
=====================================

OVERALL ATS SCORE:
{overall_score}%

SKILL MATCH:
{skill_match}%

KEYWORD MATCH:
{keyword_match}%

CONTENT SCORE:
{content_score}%

DETECTED CAREER PROFILES:
{", ".join(profiles) if profiles else "Not detected"}

SKILLS DETECTED:
{", ".join(resume_skills) if resume_skills else "None"}

MATCHED JOB SKILLS:
{", ".join(matched_skills) if job_description.strip() and matched_skills else "None"}

RECOMMENDED SKILLS:
{", ".join(missing_skills) if missing_skills else "None"}

SMART SUGGESTIONS:
{"".join(chr(10) + "- " + suggestion for suggestion in suggestions)}

=====================================

EXTRACTED RESUME TEXT:

{resume_text}
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
