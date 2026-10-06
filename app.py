import streamlit as st
import io
import re
import html
from PIL import Image

# PDF + OCR imports
try:
    import pymupdf
except ImportError:
    pymupdf = None

try:
    import pytesseract
except ImportError:
    pytesseract = None


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ResumeAI | Resume & Job Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(99,102,241,0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(168,85,247,0.15),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #080b16 0%,
            #0d1224 50%,
            #090d1a 100%
        );

    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* HERO */

.hero {
    padding: 55px 35px;
    border-radius: 28px;
    text-align: center;

    background:
        linear-gradient(
            135deg,
            rgba(99,102,241,0.28),
            rgba(168,85,247,0.18)
        );

    border: 1px solid rgba(255,255,255,0.12);

    box-shadow:
        0 25px 70px rgba(0,0,0,0.35);

    margin-bottom: 30px;
}

.hero-tag {
    color: #a5b4fc;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 15px;
}

.hero h1 {
    font-size: 52px;
    font-weight: 800;
    margin: 0;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #c4b5fd,
            #93c5fd
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero h2 {
    font-size: 24px;
    margin-top: 12px;
    color: #ddd6fe;
}

.hero p {
    max-width: 800px;
    margin: 20px auto 0;
    color: #cbd5e1;
    font-size: 16px;
    line-height: 1.8;
}


/* SECTION */

.section-title {
    font-size: 27px;
    font-weight: 800;
    margin: 35px 0 20px;
}


/* FEATURE CARDS */

.feature-card {
    padding: 25px;
    min-height: 180px;

    border-radius: 22px;

    background: rgba(255,255,255,0.055);

    border:
        1px solid
        rgba(255,255,255,0.10);

    box-shadow:
        0 12px 35px
        rgba(0,0,0,0.20);

    margin-bottom: 15px;

    transition: 0.3s;
}

.feature-card:hover {
    transform: translateY(-4px);

    border-color:
        rgba(165,180,252,0.45);
}

.feature-icon {
    font-size: 32px;
    margin-bottom: 12px;
}

.feature-title {
    font-size: 18px;
    font-weight: 700;
    color: white;
    margin-bottom: 8px;
}

.feature-text {
    color: #aab4c8;
    line-height: 1.6;
    font-size: 14px;
}


/* GLASS */

.glass-card {
    padding: 28px;

    border-radius: 22px;

    background:
        rgba(255,255,255,0.055);

    border:
        1px solid
        rgba(255,255,255,0.10);

    box-shadow:
        0 15px 40px
        rgba(0,0,0,0.25);

    margin-bottom: 20px;
}


/* METRICS */

.metric-card {
    padding: 25px;

    text-align: center;

    border-radius: 20px;

    background:
        rgba(255,255,255,0.06);

    border:
        1px solid
        rgba(255,255,255,0.10);
}

.metric-number {
    font-size: 38px;
    font-weight: 800;
    color: #a5b4fc;
}

.metric-label {
    color: #94a3b8;
    margin-top: 5px;
}


/* SKILLS */

.skill {
    display: inline-block;

    padding: 7px 13px;

    margin: 4px;

    border-radius: 20px;

    background:
        rgba(99,102,241,0.18);

    border:
        1px solid
        rgba(129,140,248,0.35);

    color: #c7d2fe;

    font-size: 13px;
}

.missing-skill {
    display: inline-block;

    padding: 7px 13px;

    margin: 4px;

    border-radius: 20px;

    background:
        rgba(239,68,68,0.12);

    border:
        1px solid
        rgba(248,113,113,0.3);

    color: #fecaca;

    font-size: 13px;
}


/* SUGGESTIONS */

.suggestion {
    padding: 18px;

    border-radius: 16px;

    background:
        rgba(255,255,255,0.045);

    border-left:
        4px solid #818cf8;

    margin-bottom: 12px;
}

.suggestion-title {
    font-weight: 700;
    margin-bottom: 5px;
}

.suggestion-text {
    color: #b7c0d0;
    font-size: 14px;
    line-height: 1.6;
}


/* BUTTON */

div.stButton > button {
    width: 100%;

    border-radius: 14px;

    padding: 14px;

    font-size: 16px;

    font-weight: 700;

    border: none;

    background:
        linear-gradient(
            90deg,
            #6366f1,
            #8b5cf6
        );

    color: white;

    box-shadow:
        0 10px 25px
        rgba(99,102,241,0.25);
}

div.stButton > button:hover {
    background:
        linear-gradient(
            90deg,
            #4f46e5,
            #7c3aed
        );

    color: white;
}


/* FILE UPLOADER */

[data-testid="stFileUploader"] {
    background:
        rgba(255,255,255,0.035);

    border-radius: 18px;

    padding: 10px;

    border:
        1px dashed
        rgba(255,255,255,0.2);
}


/* FOOTER */

.footer {
    text-align: center;

    margin-top: 50px;

    padding: 25px;

    color: #64748b;

    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SKILLS DATABASE
# --------------------------------------------------

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "mysql",
    "postgresql",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "nodejs",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data analysis",
    "data science",
    "data visualization",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "streamlit",
    "flask",
    "django",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "gcp",
    "excel",
    "power bi",
    "tableau",
    "communication",
    "leadership",
    "problem solving",
    "teamwork",
    "nlp",
    "rag",
    "llm",
    "generative ai",
    "mongodb",
    "firebase",
    "statistics",
    "data cleaning",
    "data preprocessing",
    "data mining",
    "ms office",
    "word",
    "powerpoint"
]


# --------------------------------------------------
# PDF TEXT EXTRACTION
# --------------------------------------------------

def extract_pdf_text(pdf_bytes):

    if pymupdf is None:
        return "", "PyMuPDF is not installed"

    text = ""

    try:

        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        for page in document:

            page_text = page.get_text("text")

            if page_text:
                text += page_text + "\n"

        text = text.strip()

        if len(text) >= 100:

            document.close()

            return text, "PDF Text Extraction"

        document.close()

        return "", "OCR Required"

    except Exception as e:

        return "", f"PDF Error: {str(e)}"


# --------------------------------------------------
# OCR EXTRACTION
# --------------------------------------------------

def extract_ocr_text(pdf_bytes):

    if pymupdf is None:
        return "", "PyMuPDF is not installed"

    if pytesseract is None:
        return "", "Tesseract OCR is not installed"

    text = ""

    try:

        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        for page_number in range(len(document)):

            page = document.load_page(page_number)

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

            text += page_text + "\n"

        document.close()

        text = text.strip()

        if len(text) < 20:
            return "", "OCR could not detect readable text"

        return text, "OCR"

    except Exception as e:

        return "", f"OCR Error: {str(e)}"


# --------------------------------------------------
# MAIN PDF PROCESSOR
# --------------------------------------------------

def process_resume(pdf_bytes):

    # First try normal PDF text
    text, method = extract_pdf_text(pdf_bytes)

    if text:
        return text, method

    # If normal extraction fails, try OCR
    ocr_text, ocr_method = extract_ocr_text(pdf_bytes)

    if ocr_text:
        return ocr_text, ocr_method

    return "", ocr_method


# --------------------------------------------------
# SKILL EXTRACTION
# --------------------------------------------------

def extract_skills(text):

    text_lower = text.lower()

    found = []

    for skill in SKILLS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, text_lower):

            found.append(skill)

    return sorted(set(found))


# --------------------------------------------------
# KEYWORD EXTRACTION
# --------------------------------------------------

def extract_keywords(text):

    words = re.findall(
        r"\b[a-zA-Z]{4,}\b",
        text.lower()
    )

    stopwords = {
        "this",
        "that",
        "with",
        "from",
        "have",
        "will",
        "your",
        "their",
        "they",
        "about",
        "into",
        "using",
        "work",
        "working",
        "candidate",
        "requirements",
        "responsibilities",
        "experience",
        "skills",
        "knowledge",
        "should",
        "must",
        "looking",
        "which",
        "where",
        "when",
        "while",
        "there",
        "these",
        "those"
    }

    return {
        word
        for word in words
        if word not in stopwords
    }


# --------------------------------------------------
# SCORE CALCULATION
# --------------------------------------------------

def calculate_scores(
    resume_text,
    job_description
):

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )

    matched_skills = sorted(
        set(resume_skills)
        &
        set(job_skills)
    )

    missing_skills = sorted(
        set(job_skills)
        -
        set(resume_skills)
    )

    if job_skills:

        skill_score = (
            len(matched_skills)
            /
            len(job_skills)
        ) * 100

    else:

        skill_score = 0


    resume_keywords = extract_keywords(
        resume_text
    )

    job_keywords = extract_keywords(
        job_description
    )

    if job_keywords:

        keyword_score = (
            len(
                resume_keywords
                &
                job_keywords
            )
            /
            len(job_keywords)
        ) * 100

    else:

        keyword_score = 0


    final_score = (
        skill_score * 0.70
        +
        keyword_score * 0.30
    )

    return (
        round(final_score),
        round(skill_score),
        round(keyword_score),
        matched_skills,
        missing_skills
    )


# --------------------------------------------------
# PROFILE DETECTION
# --------------------------------------------------

def detect_profile(skills):

    skill_set = set(skills)

    profiles = []


    if skill_set & {
        "python",
        "sql",
        "pandas",
        "numpy",
        "data analysis",
        "power bi",
        "tableau"
    }:

        profiles.append(
            "Data Analyst"
        )


    if skill_set & {
        "python",
        "machine learning",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "deep learning"
    }:

        profiles.append(
            "Machine Learning / AI"
        )


    if skill_set & {
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "nodejs"
    }:

        profiles.append(
            "Web Developer"
        )


    if skill_set & {
        "java",
        "c",
        "c++",
        "python",
        "sql"
    }:

        profiles.append(
            "Software Developer"
        )


    if skill_set & {
        "rag",
        "llm",
        "generative ai",
        "nlp"
    }:

        profiles.append(
            "Generative AI / NLP"
        )


    if not profiles:

        profiles.append(
            "General Technology Profile"
        )


    return profiles


# --------------------------------------------------
# SMART SUGGESTIONS
# --------------------------------------------------

def generate_suggestions(
    resume_text,
    job_description,
    missing_skills
):

    suggestions = []


    if missing_skills:

        skills_text = ", ".join(
            missing_skills[:8]
        )

        suggestions.append({
            "title":
                "Add Missing Job Skills",

            "text":
                (
                    "Consider adding relevant "
                    "skills from the job description "
                    "if you genuinely have experience "
                    f"with them: {skills_text}."
                )
        })


    if len(resume_text) < 1000:

        suggestions.append({
            "title":
                "Add More Resume Content",

            "text":
                (
                    "Your extracted resume content "
                    "is relatively short. Consider "
                    "adding stronger project descriptions, "
                    "achievements, certifications, "
                    "and relevant technical skills."
                )
        })


    if not re.search(
        r"summary|objective|profile",
        resume_text,
        re.IGNORECASE
    ):

        suggestions.append({
            "title":
                "Add a Professional Summary",

            "text":
                (
                    "Add a short professional summary "
                    "describing your technical skills, "
                    "education, projects, and career interests."
                )
        })


    if not re.search(
        r"project|projects",
        resume_text,
        re.IGNORECASE
    ):

        suggestions.append({
            "title":
                "Add Projects",

            "text":
                (
                    "Include 2–3 relevant academic or "
                    "personal projects with technologies "
                    "used and measurable outcomes."
                )
        })


    if not re.search(
        r"github|portfolio|linkedin",
        resume_text,
        re.IGNORECASE
    ):

        suggestions.append({
            "title":
                "Add Professional Links",

            "text":
                (
                    "Consider adding your GitHub, "
                    "LinkedIn, or portfolio link "
                    "if you have one."
                )
        })


    if not re.search(
        r"certification|certificate",
        resume_text,
        re.IGNORECASE
    ):

        suggestions.append({
            "title":
                "Add Certifications",

            "text":
                (
                    "Add relevant certifications or "
                    "completed courses that support "
                    "your target job role."
                )
        })


    if not suggestions:

        suggestions.append({
            "title":
                "Good Foundation",

            "text":
                (
                    "Your resume contains relevant "
                    "information. Continue improving "
                    "it with measurable achievements "
                    "and job-specific keywords."
                )
        })


    return suggestions


# --------------------------------------------------
# HERO
# --------------------------------------------------

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
        Analyze your resume, understand your career profile,
        discover your skills, compare job requirements,
        and get intelligent suggestions to improve your resume.
    </p>

</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# FEATURES
# --------------------------------------------------

st.markdown(
    '<div class="section-title">'
    '✨ Powerful Resume Intelligence'
    '</div>',
    unsafe_allow_html=True
)


features = [

    (
        "📄",
        "Resume Parsing",
        "Extract resume information automatically from your uploaded document."
    ),

    (
        "🎯",
        "Resume Scoring",
        "Evaluate resume quality and ATS compatibility instantly."
    ),

    (
        "🧠",
        "Profile Analysis",
        "Detect your career profile and identify suitable job roles."
    ),

    (
        "📊",
        "Skill Analytics",
        "Discover your technical and professional skills."
    ),

    (
        "💡",
        "Smart Suggestions",
        "Get personalized recommendations to improve your resume."
    )

]


cols = st.columns(5)


for col, feature in zip(
    cols,
    features
):

    with col:

        st.markdown(
            f"""
            <div class="feature-card">

                <div class="feature-icon">
                    {feature[0]}
                </div>

                <div class="feature-title">
                    {feature[1]}
                </div>

                <div class="feature-text">
                    {feature[2]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">'
    '🔍 Start Your Resume Analysis'
    '</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(
    [1, 1]
)


# RESUME UPLOAD

with col1:

    st.markdown(
        """
        <div class="glass-card">

        <h3>
            📄 Upload Your Resume
        </h3>

        <p style="color:#94a3b8;">
            Upload a PDF resume to extract
            and analyze your information.
        </p>
        """,
        unsafe_allow_html=True
    )


    uploaded_file = st.file_uploader(
        "Choose your resume PDF",
        type=["pdf"],
        help=(
            "Both normal text PDFs and "
            "scanned/image PDFs are supported."
        )
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# JOB DESCRIPTION

with col2:

    st.markdown(
        """
        <div class="glass-card">

        <h3>
            💼 Job Description
        </h3>

        <p style="color:#94a3b8;">
            Paste the job description you want
            to compare with your resume.
        </p>
        """,
        unsafe_allow_html=True
    )


    job_description = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder=(
            "Example:\n\n"
            "We are looking for a Data Analyst Intern "
            "with knowledge of Python, SQL, Pandas, "
            "NumPy, Excel, Power BI and data visualization..."
        ),
        label_visibility="collapsed"
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)


analyze = st.button(
    "🚀 Analyze My Resume"
)


# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

if analyze:

    if uploaded_file is None:

        st.error(
            "⚠️ Please upload your resume PDF first."
        )

        st.stop()


    if not job_description.strip():

        st.error(
            "⚠️ Please paste a job description first."
        )

        st.stop()


    with st.spinner(
        "🔎 Reading and analyzing your resume..."
    ):

        pdf_bytes = uploaded_file.getvalue()

        resume_text, extraction_method = (
            process_resume(pdf_bytes)
        )


    # EXTRACTION ERROR

    if not resume_text:

        st.error(
            "❌ Unable to extract text from this PDF."
        )

        st.warning(
            f"Reason: {extraction_method}"
        )

        st.info(
            "Please upload a clear PDF resume. "
            "Scanned PDFs require OCR support."
        )

        st.stop()


    # SCORE

    (
        final_score,
        skill_score,
        keyword_score,
        matched_skills,
        missing_skills
    ) = calculate_scores(
        resume_text,
        job_description
    )


    resume_skills = extract_skills(
        resume_text
    )


    profiles = detect_profile(
        resume_skills
    )


    suggestions = generate_suggestions(
        resume_text,
        job_description,
        missing_skills
    )


    # SUCCESS

    st.success(
        f"✅ Resume successfully analyzed using "
        f"{extraction_method}."
    )


    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🎯 Resume Analysis Results'
        '</div>',
        unsafe_allow_html=True
    )


    score_col, skill_col, keyword_col = (
        st.columns(3)
    )


    with score_col:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-number">
                    {final_score}%
                </div>

                <div class="metric-label">
                    Overall ATS Score
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with skill_col:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-number">
                    {skill_score}%
                </div>

                <div class="metric-label">
                    Skill Match
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with keyword_col:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-number">
                    {keyword_score}%
                </div>

                <div class="metric-label">
                    Keyword Match
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------
    # SKILL COMPARISON
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🛠️ Skill Comparison'
        '</div>',
        unsafe_allow_html=True
    )


    skill_col1, skill_col2 = (
        st.columns(2)
    )


    with skill_col1:

        st.markdown(
            """
            <div class="glass-card">

            <h3>
                ✅ Matched Skills
            </h3>
            """,
            unsafe_allow_html=True
        )


        if matched_skills:

            skills_html = ""

            for skill in matched_skills:

                skills_html += (
                    '<span class="skill">'
                    f'{html.escape(skill.title())}'
                    '</span>'
                )

            st.markdown(
                skills_html,
                unsafe_allow_html=True
            )

        else:

            st.write(
                "No matching skills detected."
            )


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    with skill_col2:

        st.markdown(
            """
            <div class="glass-card">

            <h3>
                ⚠️ Missing / Recommended Skills
            </h3>
            """,
            unsafe_allow_html=True
        )


        if missing_skills:

            skills_html = ""

            for skill in missing_skills:

                skills_html += (
                    '<span class="missing-skill">'
                    f'{html.escape(skill.title())}'
                    '</span>'
                )

            st.markdown(
                skills_html,
                unsafe_allow_html=True
            )

        else:

            st.write(
                "🎉 No major missing skills detected."
            )


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # --------------------------------------------------
    # PROFILE ANALYSIS
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🧠 Profile Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="glass-card">',
        unsafe_allow_html=True
    )


    st.write(
        "**Detected Career Profiles:**"
    )


    for profile in profiles:

        st.markdown(
            f'<span class="skill">'
            f'{html.escape(profile)}'
            f'</span>',
            unsafe_allow_html=True
        )


    st.markdown(
        "<br><br>**Skills Detected From Resume:**",
        unsafe_allow_html=True
    )


    if resume_skills:

        skills_html = ""

        for skill in resume_skills:

            skills_html += (
                '<span class="skill">'
                f'{html.escape(skill.title())}'
                '</span>'
            )

        st.markdown(
            skills_html,
            unsafe_allow_html=True
        )

    else:

        st.write(
            "No predefined skills detected."
        )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # SMART SUGGESTIONS
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '💡 Smart Suggestions'
        '</div>',
        unsafe_allow_html=True
    )


    for suggestion in suggestions:

        st.markdown(
            f"""
            <div class="suggestion">

                <div class="suggestion-title">
                    {html.escape(
                        suggestion["title"]
                    )}
                </div>

                <div class="suggestion-text">
                    {html.escape(
                        suggestion["text"]
                    )}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------
    # SCORE BREAKDOWN
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📊 Score Breakdown'
        '</div>',
        unsafe_allow_html=True
    )


    breakdown_col1, breakdown_col2 = (
        st.columns(2)
    )


    with breakdown_col1:

        st.markdown(
            '<div class="glass-card">',
            unsafe_allow_html=True
        )

        st.write(
            "**Skill Match — 70% Weight**"
        )

        st.progress(
            min(
                skill_score / 100,
                1.0
            )
        )

        st.write(
            f"{skill_score}% skill compatibility"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    with breakdown_col2:

        st.markdown(
            '<div class="glass-card">',
            unsafe_allow_html=True
        )

        st.write(
            "**Keyword Match — 30% Weight**"
        )

        st.progress(
            min(
                keyword_score / 100,
                1.0
            )
        )

        st.write(
            f"{keyword_score}% keyword compatibility"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # --------------------------------------------------
    # EXTRACTED TEXT
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📄 Extracted Resume Text'
        '</div>',
        unsafe_allow_html=True
    )


    with st.expander(
        "View extracted resume text"
    ):

        st.text_area(
            "Resume Text",
            resume_text,
            height=400,
            label_visibility="collapsed"
        )


    # --------------------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------------------

    report = f"""
RESUMEAI - RESUME & JOB ANALYZER
================================

Extraction Method:
{extraction_method}

OVERALL ATS SCORE
-----------------
{final_score}%

SKILL MATCH
-----------
{skill_score}%

KEYWORD MATCH
-------------
{keyword_score}%

MATCHED SKILLS
--------------
{", ".join(matched_skills) if matched_skills else "None"}

MISSING / RECOMMENDED SKILLS
----------------------------
{", ".join(missing_skills) if missing_skills else "None"}

DETECTED CAREER PROFILES
------------------------
{", ".join(profiles)}

RESUME SKILLS
-------------
{", ".join(resume_skills) if resume_skills else "None"}

SUGGESTIONS
-----------
"""


    for suggestion in suggestions:

        report += (
            f"\n{suggestion['title']}\n"
            f"{suggestion['text']}\n"
        )


    report += """

EXTRACTED RESUME TEXT
---------------------
"""


    report += resume_text


    st.download_button(
        label="⬇️ Download Analysis Report",
        data=report,
        file_name="ResumeAI_Analysis_Report.txt",
        mime="text/plain"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">

        🚀 ResumeAI ·
        Multimodal Resume & Job Intelligence

        <br>

        Built for smarter career preparation.

    </div>
    """,
    unsafe_allow_html=True
)
