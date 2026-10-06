import streamlit as st
import re
import io
from html import escape

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None


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

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(99,102,241,0.18), transparent 28%),
        radial-gradient(circle at 90% 5%, rgba(168,85,247,0.16), transparent 28%),
        linear-gradient(135deg, #070b16 0%, #0b1020 50%, #080b15 100%);
    color: #f8fafc;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main container */
.block-container {
    max-width: 1250px;
    padding-top: 30px;
    padding-bottom: 50px;
}

/* ============================================================
   HERO
   ============================================================ */

.hero {
    text-align: center;
    padding: 55px 20px 35px;
}

.hero-badge {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 30px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(129,140,248,0.28);
    color: #c7d2fe;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 22px;
}

.hero-title {
    font-size: 58px;
    line-height: 1.05;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(
        90deg,
        #818cf8,
        #c084fc,
        #22d3ee
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 21px;
    font-weight: 600;
    color: #e2e8f0;
    margin-top: 18px;
}

.hero-description {
    max-width: 720px;
    margin: 14px auto 0;
    color: #94a3b8;
    font-size: 15px;
    line-height: 1.7;
}

/* ============================================================
   SECTION TITLE
   ============================================================ */

.section-title {
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    color: #f8fafc;
    margin: 35px 0 25px;
}

/* ============================================================
   FEATURE CARDS
   ============================================================ */

.features-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    margin-bottom: 50px;
}

.feature-card {
    min-height: 205px;
    padding: 25px 17px;
    border-radius: 22px;
    text-align: center;

    background:
        linear-gradient(
            145deg,
            rgba(30,41,75,0.82),
            rgba(15,23,42,0.88)
        );

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.22),
        inset 0 1px 1px rgba(255,255,255,0.04);

    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-8px);
    border-color: rgba(129,140,248,0.55);
    box-shadow:
        0 20px 45px rgba(99,102,241,0.20);
}

.feature-icon {
    width: 64px;
    height: 64px;
    margin: 0 auto 18px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 18px;

    font-size: 31px;

    background:
        linear-gradient(
            135deg,
            rgba(99,102,241,0.25),
            rgba(168,85,247,0.20)
        );

    border: 1px solid rgba(129,140,248,0.22);
}

.feature-title {
    font-size: 16px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 10px;
}

.feature-text {
    font-size: 12px;
    line-height: 1.65;
    color: #94a3b8;
}

/* ============================================================
   GLASS CARDS
   ============================================================ */

.glass-card {
    padding: 25px;
    border-radius: 22px;

    background:
        rgba(15,23,42,0.72);

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.20);
}

.card-title {
    font-size: 20px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 8px;
}

.card-description {
    color: #94a3b8;
    font-size: 13px;
    margin-bottom: 18px;
}

/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.025);
    border: 1px dashed rgba(129,140,248,0.35);
    border-radius: 16px;
    padding: 8px;
}

/* ============================================================
   TEXT AREA
   ============================================================ */

textarea {
    background: #0f172a !important;
    color: #f8fafc !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* ============================================================
   BUTTON
   ============================================================ */

.stButton > button {
    width: 100%;
    min-height: 50px;

    border: none;
    border-radius: 14px;

    background:
        linear-gradient(
            90deg,
            #6366f1,
            #8b5cf6
        );

    color: white;
    font-size: 15px;
    font-weight: 700;

    box-shadow:
        0 10px 25px rgba(99,102,241,0.25);

    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 14px 30px rgba(139,92,246,0.35);
}

/* ============================================================
   SCORE CARD
   ============================================================ */

.score-card {
    padding: 30px;
    text-align: center;
    border-radius: 24px;

    background:
        radial-gradient(
            circle at center,
            rgba(99,102,241,0.20),
            rgba(15,23,42,0.75)
        );

    border: 1px solid rgba(129,140,248,0.25);
}

.score-number {
    font-size: 62px;
    font-weight: 800;
    background: linear-gradient(
        90deg,
        #818cf8,
        #c084fc
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.score-label {
    color: #94a3b8;
    font-size: 13px;
}

/* ============================================================
   METRICS
   ============================================================ */

.metric-card {
    text-align: center;
    padding: 25px 15px;
    min-height: 130px;

    border-radius: 20px;

    background:
        rgba(15,23,42,0.72);

    border: 1px solid rgba(255,255,255,0.08);
}

.metric-number {
    font-size: 30px;
    font-weight: 800;
    color: #c4b5fd;
}

.metric-label {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 5px;
}

/* ============================================================
   SKILL PILLS
   ============================================================ */

.skill-pill {
    display: inline-block;

    padding: 7px 13px;
    margin: 4px;

    border-radius: 30px;

    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(129,140,248,0.25);

    color: #c7d2fe;
    font-size: 12px;
    font-weight: 500;
}

.missing-pill {
    display: inline-block;

    padding: 7px 13px;
    margin: 4px;

    border-radius: 30px;

    background: rgba(245,158,11,0.10);
    border: 1px solid rgba(245,158,11,0.25);

    color: #fcd34d;
    font-size: 12px;
}

/* ============================================================
   SUGGESTION
   ============================================================ */

.suggestion {
    padding: 16px 18px;
    margin: 10px 0;

    border-radius: 14px;

    background: rgba(99,102,241,0.07);
    border-left: 3px solid #818cf8;

    color: #cbd5e1;
    font-size: 13px;
    line-height: 1.6;
}

/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
    margin-top: 55px;
    padding: 25px;

    color: #64748b;
    font-size: 12px;

    border-top: 1px solid rgba(255,255,255,0.06);
}

/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 1100px) {
    .features-grid {
        grid-template-columns: repeat(3, 1fr);
    }

    .hero-title {
        font-size: 46px;
    }
}

@media (max-width: 700px) {
    .features-grid {
        grid-template-columns: repeat(1, 1fr);
    }

    .hero-title {
        font-size: 38px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SKILLS DATABASE
# ============================================================

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
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data analysis",
    "data science",
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
    "firebase"
]


# ============================================================
# FUNCTIONS
# ============================================================

def clean_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_pdf_text(uploaded_file):

    if PyPDF2 is None:
        return ""

    try:
        data = uploaded_file.read()

        reader = PyPDF2.PdfReader(
            io.BytesIO(data)
        )

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    except Exception:
        return ""


def extract_skills(text):

    text = clean_text(text)

    found = []

    for skill in SKILLS:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found.append(skill)

    return sorted(set(found))


def calculate_skill_score(resume_skills, job_skills):

    if not job_skills:
        return 0

    matched = set(resume_skills) & set(job_skills)

    return round(
        len(matched) / len(set(job_skills)) * 100
    )


def calculate_keyword_score(resume, job):

    resume_words = set(
        clean_text(resume).split()
    )

    job_words = set(
        clean_text(job).split()
    )

    important_words = {
        word
        for word in job_words
        if len(word) >= 5
        and word.isalpha()
    }

    if not important_words:
        return 0

    matched = resume_words & important_words

    return round(
        len(matched) /
        len(important_words) *
        100
    )


def generate_suggestions(
    resume_text,
    resume_skills,
    job_skills
):

    suggestions = []

    resume_lower = clean_text(resume_text)

    missing = sorted(
        set(job_skills) -
        set(resume_skills)
    )

    if missing:
        suggestions.append(
            "Add relevant missing skills to your resume "
            "only if you genuinely have those skills: "
            + ", ".join(missing)
        )

    if (
        "summary" not in resume_lower
        and "objective" not in resume_lower
        and "profile" not in resume_lower
    ):
        suggestions.append(
            "Add a short professional summary near the top "
            "of your resume."
        )

    if "project" not in resume_lower:
        suggestions.append(
            "Add 2–3 strong projects with technologies, "
            "your role, and measurable results."
        )

    if "github" not in resume_lower:
        suggestions.append(
            "Add your GitHub or portfolio link if you have one."
        )

    if "certification" not in resume_lower:
        suggestions.append(
            "Add relevant certifications, courses, or achievements."
        )

    if len(resume_text.split()) < 180:
        suggestions.append(
            "Your resume appears short. Consider adding "
            "relevant projects, achievements, and technical details."
        )

    if not suggestions:
        suggestions.append(
            "Your resume contains the major detected keywords. "
            "Focus on measurable achievements and role-specific wording."
        )

    return suggestions


def score_message(score):

    if score >= 80:
        return "Excellent match 🚀"

    if score >= 65:
        return "Strong match ✨"

    if score >= 50:
        return "Moderate match 👍"

    return "Needs improvement 💡"


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-badge">
✦ AI-POWERED CAREER INTELLIGENCE
</div>

<div class="hero-title">
🚀 ResumeAI
</div>

<div class="hero-subtitle">
Multimodal RAG-Based Resume & Job Analyzer
</div>

<div class="hero-description">
Analyze your resume, understand your career profile,
discover your skills, compare job requirements,
and get intelligent suggestions to improve your resume.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# FEATURES
# ============================================================

st.markdown("""
<div class="section-title">
✨ Powerful Resume Intelligence
</div>

<div class="features-grid">

<div class="feature-card">

<div class="feature-icon">
📄
</div>

<div class="feature-title">
Resume Parsing
</div>

<div class="feature-text">
Extract resume information automatically
from your uploaded document.
</div>

</div>


<div class="feature-card">

<div class="feature-icon">
🎯
</div>

<div class="feature-title">
Resume Scoring
</div>

<div class="feature-text">
Evaluate resume quality and
ATS compatibility instantly.
</div>

</div>


<div class="feature-card">

<div class="feature-icon">
🧠
</div>

<div class="feature-title">
Profile Analysis
</div>

<div class="feature-text">
Detect your career profile and
identify suitable job roles.
</div>

</div>


<div class="feature-card">

<div class="feature-icon">
📊
</div>

<div class="feature-title">
Skill Analytics
</div>

<div class="feature-text">
Discover your technical and
professional skills.
</div>

</div>


<div class="feature-card">

<div class="feature-icon">
💡
</div>

<div class="feature-title">
Smart Suggestions
</div>

<div class="feature-text">
Get personalized recommendations
to improve your resume.
</div>

</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown("""
<div class="section-title">
🔍 Start Your Resume Analysis
</div>
""", unsafe_allow_html=True)


col1, col2 = st.columns(
    2,
    gap="large"
)


with col1:

    st.markdown("""
    <div class="glass-card">

    <div class="card-title">
    📄 Upload Your Resume
    </div>

    <div class="card-description">
    Upload a PDF resume to extract and analyze your information.
    </div>

    </div>
    """, unsafe_allow_html=True)

    resume_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )


with col2:

    st.markdown("""
    <div class="glass-card">

    <div class="card-title">
    💼 Job Description
    </div>

    <div class="card-description">
    Paste the job description you want to compare with your resume.
    </div>

    </div>
    """, unsafe_allow_html=True)

    job_description = st.text_area(
        "Job Description",
        height=180,
        placeholder=(
            "Example:\n\n"
            "We are looking for a Python Developer with "
            "experience in Machine Learning, SQL, Pandas, "
            "NumPy and Git..."
        ),
        label_visibility="collapsed"
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

analyze = st.button(
    "🚀 Analyze My Resume",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    if not resume_file:

        st.warning(
            "📄 Please upload your resume PDF first."
        )

    elif not job_description.strip():

        st.warning(
            "💼 Please enter the job description."
        )

    else:

        with st.spinner(
            "🧠 AI is analyzing your resume..."
        ):

            resume_text = extract_pdf_text(
                resume_file
            )

            if not resume_text.strip():

                st.error(
                    "Unable to extract text from this PDF."
                )

            else:

                resume_skills = extract_skills(
                    resume_text
                )

                job_skills = extract_skills(
                    job_description
                )

                matched_skills = sorted(
                    set(resume_skills) &
                    set(job_skills)
                )

                missing_skills = sorted(
                    set(job_skills) -
                    set(resume_skills)
                )

                skill_score = calculate_skill_score(
                    resume_skills,
                    job_skills
                )

                keyword_score = calculate_keyword_score(
                    resume_text,
                    job_description
                )

                final_score = round(
                    skill_score * 0.7 +
                    keyword_score * 0.3
                )

                suggestions = generate_suggestions(
                    resume_text,
                    resume_skills,
                    job_skills
                )

                st.session_state.result = {
                    "resume_text": resume_text,
                    "resume_skills": resume_skills,
                    "job_skills": job_skills,
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills,
                    "skill_score": skill_score,
                    "keyword_score": keyword_score,
                    "final_score": final_score,
                    "suggestions": suggestions
                }


# ============================================================
# RESULTS
# ============================================================

if "result" in st.session_state:

    result = st.session_state.result

    st.markdown("---")

    st.markdown("""
    <div class="section-title">
    📊 Resume Analysis Dashboard
    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # SCORE + METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(
        4,
        gap="medium"
    )

    with c1:

        st.markdown(f"""
        <div class="score-card">

        <div class="score-number">
        {result["final_score"]}%
        </div>

        <div class="score-label">
        ATS Match Score
        </div>

        </div>
        """, unsafe_allow_html=True)


    with c2:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-number">
        {len(result["matched_skills"])}
        </div>

        <div class="metric-label">
        Matched Skills
        </div>

        </div>
        """, unsafe_allow_html=True)


    with c3:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-number">
        {len(result["missing_skills"])}
        </div>

        <div class="metric-label">
        Missing Skills
        </div>

        </div>
        """, unsafe_allow_html=True)


    with c4:

        st.markdown(f"""
        <div class="metric-card">

        <div class="metric-number">
        {result["keyword_score"]}%
        </div>

        <div class="metric-label">
        Keyword Match
        </div>

        </div>
        """, unsafe_allow_html=True)


    st.markdown(
        f"""
        <div style="
            text-align:center;
            margin:18px 0 30px;
            color:#a5b4fc;
            font-weight:600;
        ">
        {score_message(result["final_score"])}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # MATCHED / MISSING
    # --------------------------------------------------------

    left, right = st.columns(
        2,
        gap="large"
    )


    with left:

        matched_html = ""

        for skill in result["matched_skills"]:

            matched_html += (
                f'<span class="skill-pill">'
                f'✓ {escape(skill)}'
                f'</span>'
            )

        if not matched_html:

            matched_html = (
                '<span style="color:#94a3b8;">'
                'No matching skills detected.'
                '</span>'
            )

        st.markdown(f"""
        <div class="glass-card">

        <div class="card-title">
        ✅ Matched Skills
        </div>

        <div class="card-description">
        Skills found in both your resume and the job description.
        </div>

        {matched_html}

        </div>
        """, unsafe_allow_html=True)


    with right:

        missing_html = ""

        for skill in result["missing_skills"]:

            missing_html += (
                f'<span class="missing-pill">'
                f'+ {escape(skill)}'
                f'</span>'
            )

        if not missing_html:

            missing_html = (
                '<span style="color:#94a3b8;">'
                '🎉 No major missing skills detected.'
                '</span>'
            )

        st.markdown(f"""
        <div class="glass-card">

        <div class="card-title">
        ⚠️ Skills to Improve
        </div>

        <div class="card-description">
        Job-related skills not detected in your resume.
        </div>

        {missing_html}

        </div>
        """, unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)


    # --------------------------------------------------------
    # SCORE BREAKDOWN
    # --------------------------------------------------------

    st.markdown("""
    <div class="glass-card">

    <div class="card-title">
    📈 Score Breakdown
    </div>

    <div class="card-description">
    Understand how your overall compatibility score was calculated.
    </div>

    </div>
    """, unsafe_allow_html=True)


    st.write(
        f"🎯 Skill Match — {result['skill_score']}%"
    )

    st.progress(
        result["skill_score"] / 100
    )


    st.write(
        f"🔎 Keyword Match — {result['keyword_score']}%"
    )

    st.progress(
        result["keyword_score"] / 100
    )


    st.markdown("<br>", unsafe_allow_html=True)


    # --------------------------------------------------------
    # SMART SUGGESTIONS
    # --------------------------------------------------------

    suggestions_html = ""

    for suggestion in result["suggestions"]:

        suggestions_html += (
            f'<div class="suggestion">'
            f'💡 {escape(suggestion)}'
            f'</div>'
        )

    st.markdown(f"""
    <div class="glass-card">

    <div class="card-title">
    💡 Smart Resume Suggestions
    </div>

    <div class="card-description">
    Personalized recommendations based on your resume and target job.
    </div>

    {suggestions_html}

    </div>
    """, unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)


    # --------------------------------------------------------
    # RESUME PROFILE
    # --------------------------------------------------------

    st.markdown("""
    <div class="glass-card">

    <div class="card-title">
    🧠 Detected Resume Profile
    </div>

    <div class="card-description">
    Technical skills detected from your resume.
    </div>

    </div>
    """, unsafe_allow_html=True)


    profile_skills = result["resume_skills"]

    if profile_skills:

        profile_html = ""

        for skill in profile_skills:

            profile_html += (
                f'<span class="skill-pill">'
                f'{escape(skill)}'
                f'</span>'
            )

        st.markdown(
            profile_html,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No predefined technical skills were detected."
        )


    # --------------------------------------------------------
    # EXTRACTED TEXT
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.text(
            result["resume_text"]
        )


    # --------------------------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------------------------

    report = f"""
RESUMEAI
MULTIMODAL RAG-BASED RESUME & JOB ANALYZER
============================================

ATS MATCH SCORE
---------------
{result["final_score"]}%

SKILL MATCH
-----------
{result["skill_score"]}%

KEYWORD MATCH
-------------
{result["keyword_score"]}%

MATCHED SKILLS
--------------
{", ".join(result["matched_skills"])}

MISSING SKILLS
--------------
{", ".join(result["missing_skills"])}

SMART SUGGESTIONS
-----------------
"""

    for suggestion in result["suggestions"]:

        report += f"\n- {suggestion}"

    report += """

============================================
Generated by ResumeAI
"""


    st.download_button(
        "📥 Download Analysis Report",
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

🚀 <b>ResumeAI</b>
<br>
Multimodal RAG-Based Resume & Job Analyzer
<br><br>
Analyze • Understand • Improve • Get Hired

</div>
""", unsafe_allow_html=True)
