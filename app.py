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
# PREMIUM MODERN UI
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(124,58,237,0.35), transparent 22%),
        radial-gradient(circle at 90% 5%, rgba(6,182,212,0.30), transparent 22%),
        radial-gradient(circle at 50% 35%, rgba(236,72,153,0.16), transparent 28%),
        radial-gradient(circle at 5% 80%, rgba(59,130,246,0.20), transparent 25%),
        linear-gradient(135deg, #050816 0%, #0b1026 45%, #080b19 100%);
    color: white;
}

.block-container {
    max-width: 1380px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    position: relative;
    text-align: center;
    padding: 65px 20px 55px;
}

.hero::before {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    background: rgba(124,58,237,0.16);
    filter: blur(80px);
    border-radius: 50%;
    left: 20%;
    top: 30px;
    z-index: 0;
}

.hero::after {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    background: rgba(6,182,212,0.14);
    filter: blur(80px);
    border-radius: 50%;
    right: 20%;
    top: 20px;
    z-index: 0;
}

.hero > * {
    position: relative;
    z-index: 2;
}

.hero-tag {
    display: inline-block;
    padding: 11px 23px;
    border-radius: 50px;

    background:
        linear-gradient(
            90deg,
            rgba(124,58,237,0.30),
            rgba(6,182,212,0.22),
            rgba(236,72,153,0.22)
        );

    border: 1px solid rgba(196,181,253,0.45);

    color: #e9d5ff;

    font-size: 12px;
    font-weight: 900;
    letter-spacing: 2.5px;

    box-shadow:
        0 0 25px rgba(124,58,237,0.25),
        inset 0 1px 0 rgba(255,255,255,0.15);
}

.hero h1 {
    margin: 25px 0 0;

    font-size: 78px;
    line-height: 1;

    font-weight: 900;
    letter-spacing: -4px;

    background:
        linear-gradient(
            90deg,
            #ffffff 0%,
            #c4b5fd 20%,
            #67e8f9 45%,
            #f9a8d4 70%,
            #ffffff 100%
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    filter:
        drop-shadow(0 0 18px rgba(139,92,246,0.35));
}

.hero h2 {
    margin: 20px auto 0;

    font-size: 27px;
    font-weight: 800;

    background:
        linear-gradient(
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

    color: #b9c4d8;

    font-size: 16px;
    line-height: 1.85;
}


/* ============================================================
   SECTION HEADER
   ============================================================ */

.section-heading {
    text-align: center;
    margin: 35px 0 28px;
}

.section-heading h2 {
    margin: 0;

    font-size: 31px;
    font-weight: 900;

    background:
        linear-gradient(
            90deg,
            #f5f3ff,
            #a78bfa,
            #67e8f9,
            #f9a8d4
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.section-heading p {
    margin-top: 8px;
    color: #8190aa;
    font-size: 14px;
}


/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-card {
    position: relative;

    min-height: 245px;
    padding: 27px 24px;

    border-radius: 25px;

    background:
        linear-gradient(
            145deg,
            rgba(30,41,80,0.78),
            rgba(13,18,42,0.88)
        );

    border: 1px solid rgba(148,163,184,0.17);

    box-shadow:
        0 18px 45px rgba(0,0,0,0.25),
        inset 0 1px 0 rgba(255,255,255,0.07);

    overflow: hidden;

    transition:
        transform .3s ease,
        border-color .3s ease,
        box-shadow .3s ease;
}

.feature-card::before {
    content: "";
    position: absolute;

    width: 120px;
    height: 120px;

    border-radius: 50%;

    background: rgba(124,58,237,0.16);

    filter: blur(35px);

    top: -50px;
    right: -30px;
}

.feature-card:hover {
    transform: translateY(-10px);

    border-color: rgba(103,232,249,0.55);

    box-shadow:
        0 25px 55px rgba(0,0,0,0.35),
        0 0 30px rgba(99,102,241,0.15);
}

.feature-icon {
    width: 64px;
    height: 64px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 19px;

    font-size: 31px;

    background:
        linear-gradient(
            135deg,
            rgba(124,58,237,0.45),
            rgba(6,182,212,0.28),
            rgba(236,72,153,0.20)
        );

    border: 1px solid rgba(255,255,255,0.15);

    box-shadow:
        0 10px 30px rgba(124,58,237,0.25);

    margin-bottom: 20px;
}

.feature-title {
    color: #ffffff;

    font-size: 17px;
    font-weight: 850;

    margin-bottom: 11px;
}

.feature-text {
    color: #9eabc1;

    font-size: 13px;

    line-height: 1.75;
}


/* ============================================================
   ANALYSIS AREA
   ============================================================ */

.analysis-wrapper {
    margin-top: 65px;
    margin-bottom: 30px;
}

.analysis-title {
    text-align: center;

    font-size: 36px;
    font-weight: 900;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #c4b5fd,
            #67e8f9,
            #f9a8d4
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.analysis-subtitle {
    text-align: center;

    max-width: 760px;
    margin: 12px auto 35px;

    color: #8f9db5;
    font-size: 15px;
    line-height: 1.7;
}


/* ============================================================
   INPUT CARDS
   ============================================================ */

.input-card {
    min-height: 360px;

    padding: 30px;

    border-radius: 26px;

    background:
        linear-gradient(
            145deg,
            rgba(23,32,67,0.88),
            rgba(11,16,37,0.92)
        );

    border: 1px solid rgba(139,92,246,0.25);

    box-shadow:
        0 20px 55px rgba(0,0,0,0.28),
        inset 0 1px 0 rgba(255,255,255,0.05);

    position: relative;
    overflow: hidden;
}

.input-card::before {
    content: "";

    position: absolute;

    width: 180px;
    height: 180px;

    background: rgba(6,182,212,0.09);

    border-radius: 50%;

    filter: blur(55px);

    right: -70px;
    top: -70px;
}

.input-title {
    font-size: 20px;
    font-weight: 850;

    color: #ffffff;

    margin-bottom: 8px;
}

.input-description {
    color: #8997af;

    font-size: 13px;

    line-height: 1.65;

    margin-bottom: 20px;
}

.input-badge {
    display: inline-block;

    padding: 7px 13px;

    margin-top: 8px;

    border-radius: 30px;

    color: #c4b5fd;

    background: rgba(124,58,237,0.13);

    border: 1px solid rgba(167,139,250,0.22);

    font-size: 11px;
    font-weight: 700;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {
    background:
        linear-gradient(
            135deg,
            rgba(124,58,237,0.12),
            rgba(6,182,212,0.08)
        ) !important;

    border: 1px dashed rgba(167,139,250,0.50) !important;

    border-radius: 19px !important;

    padding: 8px !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: #67e8f9 !important;

    box-shadow:
        0 0 25px rgba(103,232,249,0.12);
}


/* ============================================================
   TEXT AREA
   ============================================================ */

textarea {
    border-radius: 18px !important;

    background:
        rgba(5,10,28,0.80) !important;

    border:
        1px solid rgba(129,140,248,0.28) !important;

    color: #ffffff !important;
}

textarea:focus {
    border-color: #67e8f9 !important;

    box-shadow:
        0 0 25px rgba(103,232,249,0.12) !important;
}


/* ============================================================
   ANALYZE BUTTON
   ============================================================ */

.stButton {
    margin-top: 22px;
}

.stButton > button {
    width: 100%;

    min-height: 62px;

    border: none !important;

    border-radius: 18px !important;

    color: white !important;

    font-size: 17px !important;

    font-weight: 900 !important;

    background:
        linear-gradient(
            90deg,
            #7c3aed,
            #6366f1,
            #06b6d4,
            #ec4899,
            #7c3aed
        ) !important;

    background-size: 300% 100% !important;

    box-shadow:
        0 15px 40px rgba(99,102,241,0.35);

    transition:
        transform .25s ease,
        box-shadow .25s ease;
}

.stButton > button:hover {
    transform: translateY(-4px);

   
