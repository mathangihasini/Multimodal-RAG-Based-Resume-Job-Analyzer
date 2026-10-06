import os
import re

import streamlit as st
import pymupdf
from docx import Document
import numpy as np
from sentence_transformers import SentenceTransformer

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume & Job Analyzer",
    page_icon="📄",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("📄 AI-Powered Resume & Job Description Analyzer")

st.write(
    "Upload a resume and job description to perform "
    "RAG-based semantic matching and skill-gap analysis."
)


# ============================================================
# EMBEDDING MODEL
# ============================================================

@st.cache_resource
def load_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


with st.spinner("Loading AI model..."):

    model = load_model()


# ============================================================
# EXTRACT PDF
# ============================================================

def extract_pdf(file):

    text = ""

    pdf = pymupdf.open(
        stream=file.read(),
        filetype="pdf"
    )

    for page in pdf:

        text += page.get_text()

        text += "\n"

    pdf.close()

    return text


# ============================================================
# EXTRACT DOCX
# ============================================================

def extract_docx(file):

    text = ""

    document = Document(file)

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text += paragraph.text

            text += "\n"

    for table in document.tables:

        for row in table.rows:

            for cell in row.cells:

                text += cell.text

                text += " "

            text += "\n"

    return text


# ============================================================
# EXTRACT TXT
# ============================================================

def extract_txt(file):

    return file.read().decode(
        "utf-8",
        errors="ignore"
    )


# ============================================================
# DOCUMENT EXTRACTION
# ============================================================

def extract_text(file):

    name = file.name.lower()

    if name.endswith(".pdf"):

        return extract_pdf(file)

    if name.endswith(".docx"):

        return extract_docx(file)

    if name.endswith(".txt"):

        return extract_txt(file)

    return ""


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# CHUNK TEXT
# ============================================================

def chunk_text(
    text,
    chunk_size=400,
    overlap=80
):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = min(
            start + chunk_size,
            len(words)
        )

        chunk = " ".join(
            words[start:end]
        )

        if chunk:

            chunks.append(chunk)

        if end >= len(words):

            break

        start = end - overlap

    return chunks


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

def create_embeddings(chunks):

    if not chunks:

        return None

    return model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )


# ============================================================
# RAG RETRIEVAL
# ============================================================

def retrieve_chunks(
    query,
    chunks,
    embeddings,
    top_k=5
):

    if embeddings is None:

        return []

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )[0]

    scores = np.dot(
        embeddings,
        query_embedding
    )

    indices = np.argsort(
        scores
    )[::-1]

    indices = indices[:top_k]

    results = []

    for index in indices:

        results.append(
            {
                "text": chunks[index],
                "score": float(
                    scores[index]
                )
            }
        )

    return results


# ============================================================
# SKILL LIST
# ============================================================

SKILLS = [

    "python",
    "java",
    "c++",
    "javascript",
    "typescript",

    "html",
    "css",

    "react",
    "angular",
    "node.js",

    "django",
    "flask",
    "fastapi",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "computer vision",

    "tensorflow",
    "pytorch",
    "keras",

    "scikit-learn",
    "pandas",
    "numpy",

    "aws",
    "azure",
    "gcp",

    "docker",
    "kubernetes",

    "git",
    "github",
    "linux",

    "power bi",
    "tableau",
    "excel",

    "spark",
    "hadoop",

    "data analysis",
    "data science",

    "rest api",
    "api",

    "cybersecurity",
    "networking",

    "agile",
    "scrum"

]


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(text):

    text = text.lower()

    found = []

    for skill in SKILLS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text
        ):

            found.append(skill)

    return sorted(
        set(found)
    )


# ============================================================
# EXPERIENCE
# ============================================================

def extract_experience(text):

    patterns = [

        r"(\d+(?:\.\d+)?)\+?\s*years?\s+(?:of\s+)?experience",

        r"(\d+(?:\.\d+)?)\+?\s*years?"

    ]

    values = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for value in matches:

            try:

                values.append(
                    float(value)
                )

            except:

                pass

    if values:

        return max(values)

    return 0


# ============================================================
# SKILL ANALYSIS
# ============================================================

def analyze_skills(
    resume,
    job
):

    resume_skills = set(
        extract_skills(resume)
    )

    job_skills = set(
        extract_skills(job)
    )

    matched = sorted(
        resume_skills & job_skills
    )

    missing = sorted(
        job_skills - resume_skills
    )

    if job_skills:

        score = (
            len(matched)
            /
            len(job_skills)
        ) * 100

    else:

        score = 0

    return (
        resume_skills,
        job_skills,
        matched,
        missing,
        round(score, 2)
    )


# ============================================================
# SEMANTIC SCORE
# ============================================================

def semantic_score(
    resume,
    job
):

    embeddings = model.encode(
        [resume, job],
        normalize_embeddings=True
    )

    similarity = np.dot(
        embeddings[0],
        embeddings[1]
    )

    return round(
        max(
            0,
            min(
                100,
                similarity * 100
            )
        ),
        2
    )


# ============================================================
# OPENAI ANALYSIS
# ============================================================

def ai_analysis(
    resume,
    job,
    retrieved,
    matched,
    missing
):

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:

        return None

    if OpenAI is None:

        return None

    context = "\n\n".join(

        item["text"]

        for item in retrieved

    )

    client = OpenAI(
        api_key=api_key
    )

    prompt = f"""

You are an expert technical recruiter.

Analyze this resume against this job description.

RESUME:

{resume[:10000]}


JOB DESCRIPTION:

{job[:8000]}


RETRIEVED RESUME EVIDENCE:

{context[:6000]}


MATCHING SKILLS:

{matched}


MISSING SKILLS:

{missing}


Give:

1. Overall assessment
2. Strong matching areas
3. Missing skills
4. Experience gaps
5. Resume improvement suggestions
6. Recommended skills to learn
7. Five interview questions
8. Final recommendation

Do not invent information.

"""

    try:

        response = client.chat.completions.create(

            model=os.getenv(
                "OPENAI_MODEL",
                "gpt-4o-mini"
            ),

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are an expert recruitment analyst."
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.2

        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        return f"AI error: {e}"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Settings")

    top_k = st.slider(
        "RAG chunks",
        1,
        10,
        5
    )

    st.divider()

    st.write(
        "Supported files:"
    )

    st.write(
        "📄 PDF"
    )

    st.write(
        "📝 DOCX"
    )

    st.write(
        "📃 TXT"
    )


# ============================================================
# UPLOAD FILES
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader(
        "📄 Resume"
    )

    resume_file = st.file_uploader(
        "Upload Resume",
        type=[
            "pdf",
            "docx",
            "txt"
        ]
    )


with col2:

    st.subheader(
        "💼 Job Description"
    )

    job_file = st.file_uploader(
        "Upload Job Description",
        type=[
            "pdf",
            "docx",
            "txt"
        ]
    )


# ============================================================
# ANALYZE
# ============================================================

if st.button(
    "🚀 Analyze Resume",
    type="primary",
    use_container_width=True
):

    if resume_file is None:

        st.warning(
            "Please upload a resume."
        )

        st.stop()


    if job_file is None:

        st.warning(
            "Please upload a job description."
        )

        st.stop()


    # --------------------------------------------------------
    # TEXT EXTRACTION
    # --------------------------------------------------------

    with st.spinner(
        "Reading documents..."
    ):

        resume = clean_text(
            extract_text(
                resume_file
            )
        )

        job = clean_text(
            extract_text(
                job_file
            )
        )


    if not resume:

        st.error(
            "Could not extract resume text."
        )

        st.stop()


    if not job:

        st.error(
            "Could not extract job description."
        )

        st.stop()


    # --------------------------------------------------------
    # RAG
    # --------------------------------------------------------

    with st.spinner(
        "Creating RAG embeddings..."
    ):

        chunks = chunk_text(
            resume
        )

        embeddings = create_embeddings(
            chunks
        )


    # --------------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------------

    with st.spinner(
        "Retrieving relevant resume information..."
    ):

        retrieved = retrieve_chunks(
            job,
            chunks,
            embeddings,
            top_k
        )


    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    with st.spinner(
        "Analyzing skills..."
    ):

        (
            resume_skills,
            job_skills,
            matched,
            missing,
            skill_score
        ) = analyze_skills(
            resume,
            job
        )


    # --------------------------------------------------------
    # SEMANTIC SCORE
    # --------------------------------------------------------

    with st.spinner(
        "Calculating semantic similarity..."
    ):

        semantic = semantic_score(
            resume,
            job
        )


    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    final_score = round(
        (
            semantic * 0.6
            +
            skill_score * 0.4
        ),
        2
    )


    # ========================================================
    # RESULTS
    # ========================================================

    st.divider()

    st.header(
        "📊 Analysis Results"
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Overall Match",
            f"{final_score}%"
        )


    with c2:

        st.metric(
            "Semantic Match",
            f"{semantic}%"
        )


    with c3:

        st.metric(
            "Skill Match",
            f"{skill_score}%"
        )


    st.progress(
        final_score / 100
    )


    if final_score >= 80:

        st.success(
            "🟢 Strong Match"
        )

    elif final_score >= 60:

        st.warning(
            "🟡 Moderate Match"
        )

    else:

        st.error(
            "🔴 Low Match"
        )


    # ========================================================
    # SKILLS
    # ========================================================

    st.header(
        "🧠 Skill Analysis"
    )


    c1, c2 = st.columns(2)


    with c1:

        st.subheader(
            "✅ Matching Skills"
        )

        if matched:

            for skill in matched:

                st.success(
                    skill.title()
                )

        else:

            st.info(
                "No matching skills found."
            )


    with c2:

        st.subheader(
            "❌ Missing Skills"
        )

        if missing:

            for skill in missing:

                st.error(
                    skill.title()
                )

        else:

            st.success(
                "No major missing skills."
            )


    # ========================================================
    # EXPERIENCE
    # ========================================================

    resume_exp = extract_experience(
        resume
    )

    job_exp = extract_experience(
        job
    )


    st.header(
        "💼 Experience Analysis"
    )


    c1, c2 = st.columns(2)


    with c1:

        st.metric(
            "Resume Experience",
            f"{resume_exp} years"
        )


    with c2:

        st.metric(
            "Required Experience",
            f"{job_exp} years"
        )


    # ========================================================
    # RAG EVIDENCE
    # ========================================================

    st.header(
        "🔎 RAG Retrieved Evidence"
    )


    for i, item in enumerate(
        retrieved,
        1
    ):

        with st.expander(
            f"Evidence {i} "
            f"Similarity: {item['score']:.2f}"
        ):

            st.write(
                item["text"]
            )


    # ========================================================
    # AI ANALYSIS
    # ========================================================

    st.header(
        "🤖 AI Recruiter Analysis"
    )


    with st.spinner(
        "Generating AI analysis..."
    ):

        analysis = ai_analysis(
            resume,
            job,
            retrieved,
            matched,
            missing
        )


    if analysis:

        st.markdown(
            analysis
        )

    else:

        st.info(
            "OpenAI analysis is disabled. "
            "Set OPENAI_API_KEY to enable it."
        )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.header(
        "🎯 Recommendations"
    )


    if missing:

        for skill in missing:

            st.markdown(
                f"- Learn or improve **{skill.title()}**"
            )

    else:

        st.success(
            "The candidate has all detected required skills."
        )


    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    report = f"""

AI RESUME & JOB DESCRIPTION ANALYZER
=====================================

Overall Match: {final_score}%

Semantic Match: {semantic}%

Skill Match: {skill_score}%


MATCHING SKILLS
---------------
{", ".join(matched)}


MISSING SKILLS
--------------
{", ".join(missing)}


Resume Experience:
{resume_exp} years


Required Experience:
{job_exp} years


AI ANALYSIS
-----------
{analysis if analysis else "Not enabled."}

"""


    st.download_button(
        "📥 Download Report",
        report,
        "resume_analysis.txt",
        "text/plain",
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI-Powered Multimodal Resume & Job Description Analyzer using RAG"
)
