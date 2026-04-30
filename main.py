"""
AI Book Generator
==================
Generates full-length books using AI with parallel chapter generation.
Optimized for speed: chapters generated concurrently, not sequentially.
Supports fiction, non-fiction, technical, biography, and more.
"""

import streamlit as st
from groq import Groq
import openai
import json
import os
import time
import threading
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from markdown import markdown
from dotenv import load_dotenv
import tempfile

load_dotenv()

# --- Page config ------------------------------------------------------------
st.set_page_config(
    page_title="AI Book Generator - Inspired Technology",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Page routing -------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

# Detect ?start=1 query param FIRST (set by landing page CTA buttons)
_qp = st.query_params
if _qp.get("start") == "1" or _qp.get("page") == "app":
    st.session_state.page = "app"
    st.query_params.clear()   # clean URL
    st.rerun()

# Show landing page (same tab - no new window)
if st.session_state.page == "landing":
    from landing import show_landing
    show_landing()
    # Streamlit CTA button - styled to match the landing page design
    st.markdown("""
    <style>
    div[data-testid="stButton"] > button {
        background: #A8FF4B !important;
        color: #09090B !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 36px !important;
        font-size: 17px !important;
        font-weight: 800 !important;
        cursor: pointer !important;
        box-shadow: 0 0 24px rgba(168,255,75,0.4) !important;
        width: auto !important;
        display: block !important;
        margin: 0 auto !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: #BFFF6E !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 36px rgba(168,255,75,0.6) !important;
    }
    /* Center the button in page */
    div[data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
        margin-top: -60px !important;
        position: relative !important;
        z-index: 10 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("Start Writing Free", key="landing_cta", type="primary"):
        st.session_state.page = "app"
        st.rerun()

    st.stop()

# --- Constants ----------------------------------------------------------------
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
    "mixtral-8x7b-32768",
]

OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
]

BOOK_GENRES = [
    "Non-Fiction / Self-Help",
    "Fiction / Novel",
    "Technical / Educational",
    "Biography / Memoir",
    "Business / Finance",
    "Science / Research",
    "History",
    "Philosophy",
    "Children's Book",
    "Fantasy / Sci-Fi",
]

WRITING_STYLES = [
    "Professional & Academic",
    "Conversational & Engaging",
    "Narrative & Storytelling",
    "Technical & Detailed",
    "Inspirational & Motivational",
    "Simple & Clear",
]

# --- Session state ---------------------------------------------------------
def init_state():
    defaults = {
        "provider": "Groq",
        "groq_client": None,
        "openai_client": None,
        "groq_api_key": os.getenv("GROQ_API_KEY", ""),
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "book": None,
        "book_title": "",
        "structure": {},
        "chapters": {},        # {title: content}
        "generating": False,
        "progress": 0,
        "total_chapters": 0,
        "stats": {"tokens": 0, "time": 0, "speed": 0},
        "words_per_chapter": 1500,
        "errors": [],
        "completed": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# --- AI Client --------------------------------------------------------------
def get_client():
    if st.session_state.provider == "OpenAI":
        key = st.session_state.openai_api_key
        if not key:
            return None, "openai"
        if not st.session_state.openai_client:
            st.session_state.openai_client = openai.OpenAI(api_key=key)
        return st.session_state.openai_client, "openai"
    else:
        key = st.session_state.groq_api_key
        if not key:
            return None, "groq"
        if not st.session_state.groq_client:
            st.session_state.groq_client = Groq(api_key=key)
        return st.session_state.groq_client, "groq"

def ai_complete(messages, model, max_tokens=4096, temperature=0.7, stream=False, json_mode=False, client=None):
    """Single AI call with retry logic - supports Groq and OpenAI."""
    if client is None:
        client, _ = get_client()
    if not client:
        raise ValueError("No API key configured")

    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    for attempt in range(3):
        try:
            return client.chat.completions.create(**kwargs)
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)

# --- Generation functions ----------------------------------------------------
def generate_book_title(topic: str, genre: str, language: str, model: str) -> str:
    resp = ai_complete(
        messages=[
            {"role": "system", "content": f"You are a bestselling author. Generate ONE compelling book title in {language}. Output only the title, nothing else."},
            {"role": "user", "content": f"Genre: {genre}\nTopic: {topic}\n\nGenerate a single captivating book title."}
        ],
        model=model,
        max_tokens=80,
        temperature=0.8,
    )
    return resp.choices[0].message.content.strip().strip('"\'')


def generate_book_structure(topic: str, genre: str, style: str, num_chapters: int,
                             language: str, model: str, additional: str) -> dict:
    """
    Generate book structure as JSON.
    Returns nested dict: {chapter_title: {subchapter: description, ...}, ...}
    Optimized: single call, tight prompt, JSON mode.
    """
    resp = ai_complete(
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are an expert book architect. Create detailed book structures in {language}. "
                    f"Output pure JSON only. Format:\n"
                    f'{{"Chapter Title": {{"Subchapter 1": "brief description", "Subchapter 2": "brief description"}}, '
                    f'"Chapter Title 2": {{"Subchapter 1": "description"}}}}'
                )
            },
            {
                "role": "user",
                "content": (
                    f"Create a {num_chapters}-chapter book structure for:\n"
                    f"Topic: {topic}\nGenre: {genre}\nStyle: {style}\n"
                    f"Language: {language}\n"
                    f"Additional instructions: {additional or 'None'}\n\n"
                    f"Each chapter must have 3-5 meaningful subchapters. "
                    f"Include a Prologue/Introduction and Epilogue/Conclusion."
                )
            }
        ],
        model=model,
        max_tokens=4000,
        temperature=0.4,
        json_mode=True,
    )
    return json.loads(resp.choices[0].message.content)


def generate_chapter(
    chapter_title: str,
    chapter_desc: dict,
    book_title: str,
    genre: str,
    style: str,
    language: str,
    model: str,
    additional: str,
    prev_summary: str = "",
    words_per_chapter: int = 1500,
    client=None,
) -> tuple[str, str, dict]:
    """
    Generate a single chapter. Returns (title, content, stats).
    Designed to run in a thread pool for parallel generation.
    """
    subchapters = "\n".join([f"- {k}: {v}" for k, v in chapter_desc.items()]) \
        if isinstance(chapter_desc, dict) else str(chapter_desc)

    context = f"\n\nPrevious chapter summary: {prev_summary}" if prev_summary else ""

    system_prompt = (
        f"You are a bestselling author writing a {genre} book titled '{book_title}' in {language}. "
        f"Writing style: {style}. "
        f"Write richly detailed, engaging, well-structured content. "
        f"Use markdown for formatting (## for subchapter headings). "
        f"Write approximately {words_per_chapter} words for this chapter."
    )

    user_prompt = (
        f"Write the full chapter: **{chapter_title}**\n\n"
        f"Subchapters to cover:\n{subchapters}\n"
        f"{context}\n"
        f"Additional instructions: {additional or 'None'}\n\n"
        f"Target length: ~{words_per_chapter} words. Write the complete chapter now."
    )

    start = time.time()
    dynamic_max_tokens = min(8192, max(2048, int(words_per_chapter * 1.4)))

    resp = ai_complete(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model=model,
        max_tokens=dynamic_max_tokens,
        temperature=0.6,
        stream=False,
        client=client,
    )

    content = resp.choices[0].message.content or ""
    usage = getattr(resp, "usage", None)
    input_tokens = getattr(usage, "prompt_tokens", 0) if usage else 0
    output_tokens = getattr(usage, "completion_tokens", 0) if usage else 0

    elapsed = time.time() - start
    stats = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "time": elapsed,
        "speed": output_tokens / elapsed if elapsed > 0 else 0,
    }
    return chapter_title, content, stats


def summarize_chapter(content: str, model: str, language: str, client=None) -> str:
    """Generate a brief summary of a chapter for continuity context."""
    resp = ai_complete(
        messages=[
            {"role": "system", "content": f"Summarize in 2-3 sentences in {language}. Output only the summary."},
            {"role": "user", "content": f"Summarize this chapter:\n\n{content[:3000]}"}
        ],
        model=model,
        max_tokens=150,
        temperature=0.3,
        client=client,
    )
    return resp.choices[0].message.content.strip()


# --- Export ------------------------------------------------------------------
def build_markdown(title: str, chapters: dict) -> str:
    md = f"# {title}\n\n---\n\n"
    for ch_title, content in chapters.items():
        md += f"## {ch_title}\n\n{content}\n\n---\n\n"
    return md


def build_pdf(title: str, chapters: dict) -> bytes:
    """Pure-Python PDF using fpdf2 - no system libraries required."""
    from fpdf import FPDF
    import re
    from pathlib import Path

    # -- Find a Unicode-capable TTF font --------------------------------------
    unicode_font_loaded = False
    font_candidates = []

    # fpdf2 bundles DejaVu fonts in its package directory
    try:
        import fpdf as _fpdf_mod
        _fpdf_font_dir = Path(_fpdf_mod.__file__).parent / "fonts"
        for name in ("DejaVuSans.ttf", "dejavu-sans.ttf"):
            p = _fpdf_font_dir / name
            if p.exists():
                font_candidates.append(str(p))
                break
    except Exception:
        pass

    # Common system font locations
    font_candidates += [
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(20, 20, 20)

    for font_path in font_candidates:
        try:
            pdf.add_font("Unicode", style="", fname=font_path)
            unicode_font_loaded = True
            break
        except Exception:
            continue

    FONT = "Unicode" if unicode_font_loaded else "Helvetica"

    # -- ASCII fallback map used when no Unicode font is available -------------
    _ASCII_MAP = str.maketrans({
        "-": "--", "-": "-", "-": "-", "-": "-",
        "'": "'",  "'": "'", """: '"', """: '"',
        "...": "...","-": "*", ".": "*", "?": " ",
        "?": " ",  "?": "",  "?": '"', "?": '"',
    })

    def clean(text):
        text = re.sub(r"#{1,6}\s*", "", text)
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
        text = re.sub(r"\*(.+?)\*", r"\1", text)
        text = re.sub(r"`(.+?)`", r"\1", text)
        text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
        if not unicode_font_loaded:
            text = text.translate(_ASCII_MAP)
            text = text.encode("latin-1", errors="replace").decode("latin-1")
        return text.strip()

    # Title page
    pdf.add_page()
    pdf.set_font(FONT, "", 28)
    pdf.set_y(80)
    pdf.multi_cell(0, 12, clean(title), align="C")
    pdf.set_font(FONT, "", 12)
    pdf.set_y(130)
    pdf.cell(0, 8, "Generated by AI Book Generator", align="C")

    for ch_title, content in chapters.items():
        pdf.add_page()
        pdf.set_font(FONT, "", 18)
        pdf.set_text_color(45, 53, 97)
        pdf.multi_cell(0, 10, clean(ch_title))
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)

        pdf.set_font(FONT, "", 11)
        for line in content.split("\n"):
            line = line.strip()
            if not line:
                pdf.ln(3)
                continue
            if line.startswith("## ") or line.startswith("### "):
                pdf.set_font(FONT, "", 14)
                pdf.set_text_color(45, 53, 97)
                pdf.multi_cell(0, 8, clean(line))
                pdf.set_font(FONT, "", 11)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(2)
            else:
                pdf.multi_cell(0, 6, clean(line))

    return bytes(pdf.output())


# --- UI ----------------------------------------------------------------------
st.markdown("""
<style>
/* -- Global app styles ----------------------------------------- */
[data-testid="stAppViewContainer"] { background: #06060f; }
[data-testid="stSidebar"] { background: #11111a; border-right: 1px solid rgba(255,255,255,0.06); }
[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

/* -- Mobile: stack all columns --------------------------------- */
@media (max-width: 768px) {
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        min-width: 100% !important; flex: 1 1 100% !important;
    }
    .block-container { padding: 1rem 1rem 4rem !important; }
    [data-testid="stSidebar"] { min-width: 80vw !important; }
}

/* -- App header ------------------------------------------------ */
.app-header-wrap { margin-bottom: 1.5rem; }
.app-header-title {
    font-size: clamp(1.6rem, 4vw, 2.4rem); font-weight: 900;
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 60%, #ec4899 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1.2; margin-bottom: 0.2rem;
}
.app-header-sub { color: #9ca3af; font-size: 0.95rem; margin-bottom: 0; }

/* -- App navbar ------------------------------------------------ */
.app-navbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 0 18px; margin-bottom: 4px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.app-nav-logo { font-size: 16px; font-weight: 800; color: #f9fafb; }
.app-nav-logo span { color: #8b5cf6; }

/* -- Sidebar stats --------------------------------------------- */
.stat-box {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06); border-radius: 10px;
    padding: 12px 16px; text-align: center; margin-bottom: 8px;
}
.stat-val { font-size: 1.35rem; font-weight: 800; color: #a855f7; }
.stat-label { font-size: .72rem; color: #9ca3af; margin-top: 2px; font-weight: 500; text-transform: uppercase; letter-spacing: .04em; }

/* -- Section headings ------------------------------------------ */
.section-heading {
    font-size: 1rem; font-weight: 700; color: #f9fafb;
    margin: 1.4rem 0 0.7rem; display: flex; align-items: center; gap: 8px;
}

/* -- Form elements --------------------------------------------- */
[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
    border-radius: 10px !important;
    border-color: rgba(255,255,255,0.1) !important;
    font-size: 0.92rem !important;
    background-color: rgba(255,255,255,0.03) !important;
    color: #f9fafb !important;
}
[data-testid="stTextArea"] textarea:focus,
[data-testid="stTextInput"] input:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
}
[data-testid="stSelectbox"] > div > div {
    border-radius: 10px !important;
    border-color: rgba(255,255,255,0.1) !important;
    background-color: rgba(255,255,255,0.03) !important;
}

/* -- Primary button -------------------------------------------- */
[data-testid="stBaseButton-primary"] > button,
button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    border: none !important; border-radius: 10px !important;
    font-weight: 700 !important; font-size: 15px !important;
    color: #fff !important;
    box-shadow: 0 0 16px rgba(124,58,237,0.3) !important;
    transition: transform .15s, box-shadow .15s !important;
}
[data-testid="stBaseButton-primary"] > button:hover,
button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 24px rgba(124,58,237,0.5) !important;
}

/* -- Download buttons ------------------------------------------ */
[data-testid="stDownloadButton"] > button {
    border-radius: 10px !important; font-weight: 600 !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #f9fafb !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.2) !important;
}

/* -- Chapter preview cards ------------------------------------- */
.chapter-card {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px;
    padding: 16px 20px; margin: 8px 0;
    border-left: 4px solid #8b5cf6;
    box-shadow: 0 1px 6px rgba(0,0,0,0.2);
}
.chapter-card-title { font-weight: 700; color: #f9fafb; font-size: 0.9rem; margin-bottom: 6px; }
.chapter-card-preview { color: #9ca3af; font-size: 0.82rem; line-height: 1.6; }

/* -- Info / success / warning tweaks -------------------------- */
[data-testid="stAlert"] { border-radius: 10px !important; }
/* Hide sidebar collapse button text/icon */
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] > div:first-child button { display: none !important; }



/* Hide default Streamlit sidebar collapse arrow that shows as text */
[data-testid="collapsedControl"] { display: none !important; }
button[kind="headerNoPadding"] svg { display: none !important; }

/* -- Tabs ------------------------------------------------------ */
[data-testid="stTabs"] [data-testid="stTab"] {
    font-weight: 600 !important; font-size: 0.85rem !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ── CRITICAL: Hide ALL Streamlit default icon buttons that show as text ── */
button[data-testid="baseButton-headerNoPadding"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarNavToggleButton"],
.st-emotion-cache-1rtdyuf,
.st-emotion-cache-nakul0,
div[data-testid="stSidebarContent"] > div > button,
section[data-testid="stSidebar"] > div > div > button { 
    display: none !important; 
    visibility: hidden !important;
}
/* Hide any span that contains Material icon text */
button span:only-child { font-size: 0 !important; }
</style>
""", unsafe_allow_html=True)

# App page top navbar
st.markdown('''
<div class="app-navbar">
  <div class="app-nav-logo">📚 AI Book<span>Gen</span></div>
  <a href="https://inspiredtechnology.ae" target="_blank" style="color:#a78bfa;font-size:12px;text-decoration:none">by Inspired Technology ↗</a>
</div>
''', unsafe_allow_html=True)

col_back, _ = st.columns([1, 6])
with col_back:
    if st.button("Home", key="back_home", icon=":material/home:"):
        st.session_state.page = "landing"
        st.query_params.clear()
        st.rerun()

st.markdown("""
<div class="app-header-wrap">
  <div class="app-header-title">📚 AI Book Generator</div>
  <div class="app-header-sub">Write full-length books in minutes - powered by parallel AI generation</div>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h3 style='font-size:14px;font-weight:700;color:#e5e7eb;margin-bottom:8px'>📊 Generation Stats</h3>", unsafe_allow_html=True)
    if st.session_state.stats["tokens"] > 0:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="stat-box"><div class="stat-val">{st.session_state.stats["tokens"]:,}</div><div class="stat-label">Total Tokens</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-box"><div class="stat-val">{st.session_state.stats["speed"]:.0f}</div><div class="stat-label">Tokens/sec</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-box"><div class="stat-val">{st.session_state.stats["time"]:.1f}s</div><div class="stat-label">Total Time</div></div>', unsafe_allow_html=True)
    else:
        st.info("Stats will appear after generation")

    if st.session_state.chapters:
        st.markdown("---")
        st.markdown("<h3 style='font-size:14px;font-weight:700;color:#e5e7eb;margin-bottom:8px'>📑 Chapters</h3>", unsafe_allow_html=True)
        for title in st.session_state.structure.keys():
            done = title in st.session_state.chapters
            icon = "✅" if done else "⏳"
            st.markdown(f"{icon} {title[:35]}{'...' if len(title)>35 else ''}")
# --- Main form ----------------------------------------------------------------
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # --- Configuration expander ----------------------------------------
    with st.expander("Configuration", expanded=not (st.session_state.groq_api_key or st.session_state.openai_api_key), icon=":material/settings:"):
        provider = st.radio(
            "AI Provider",
            ["Groq", "OpenAI"],
            index=0 if st.session_state.get("provider", "Groq") == "Groq" else 1,
            horizontal=True,
            help="Groq is free and fast. OpenAI requires a paid key."
        )
        if provider != st.session_state.get("provider", "Groq"):
            st.session_state.provider = provider
            st.session_state.groq_client = None
            st.session_state.openai_client = None

        if provider == "Groq":
            model = st.selectbox("Model", GROQ_MODELS, index=0,
                                  help="Llama 3.3 70B = best quality . Llama 3.1 8B = fastest")
            st.session_state.selected_model = model
        else:
            model = st.selectbox("Model", OPENAI_MODELS, index=0,
                                  help="GPT-4o = best quality . GPT-4o-mini = cheapest")
            st.session_state.selected_model = model

    # Always resolve current values from session state (safe across reruns)
    provider = st.session_state.get("provider", "Groq")
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = GROQ_MODELS[0]
    model = st.session_state.get("selected_model", GROQ_MODELS[0])

    st.markdown('<div class="section-heading">📝 Book Details</div>', unsafe_allow_html=True)

    topic = st.text_area(
        "What is your book about?",
        placeholder="E.g., 'The psychology of habit formation and how to rewire your brain for success'",
        height=250,
    )

    genre = st.selectbox("Genre", BOOK_GENRES)
    writing_style = st.selectbox("Writing Style", WRITING_STYLES)

    c1, c2 = st.columns(2)
    with c1:
        num_chapters = st.slider("Number of Chapters", 5, 25, 10)
    with c2:
        language = st.selectbox("Language", ["English", "Arabic", "French", "Spanish", "German"])

    target_pages = st.slider(
        "⚠️ Target Pages",
        min_value=50, max_value=500, value=150, step=25,
        help="Approximate page count (1 page ⚠️ 300 words)"
    )
    words_per_chapter = max(800, (target_pages * 300) // num_chapters)
    st.caption(f"~{target_pages * 300:,} total words . ~{words_per_chapter:,} words/chapter . ~{target_pages} pages")

    additional = st.text_area(
        "Additional Instructions (optional)",
        placeholder="E.g., 'Include real-world examples', 'Target audience: beginners', 'Add exercises at end of each chapter'",
        height=80,
    )

    parallel = st.toggle("Parallel Generation", value=True,
                          help="Generate multiple chapters simultaneously - much faster but uses more API credits")

    max_workers = st.slider("Parallel Workers", 2, 6, 3,
                             disabled=not parallel,
                             help="How many chapters to generate at once") if parallel else 1

with col_right:
    st.markdown('<div class="section-heading">🚀 Generate</div>', unsafe_allow_html=True)

    if st.session_state.completed and st.session_state.chapters:
        st.success(f"Your book **{st.session_state.book_title}** is ready!")

        # Download buttons
        md_content = build_markdown(st.session_state.book_title, st.session_state.chapters)
        st.download_button(
            "⚠️ Download Markdown",
            data=md_content.encode("utf-8"),
            file_name=f"{st.session_state.book_title}.md",
            mime="text/markdown",
            use_container_width=True,
        )

        try:
            pdf_bytes = build_pdf(st.session_state.book_title, st.session_state.chapters)
            st.download_button(
                "⚠️ Download PDF",
                data=pdf_bytes,
                file_name=f"{st.session_state.book_title}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.warning(f"PDF export unavailable: {e}")

        if st.button("Generate New Book", use_container_width=True, icon=":material/refresh:"):
            for k in ["book", "book_title", "structure", "chapters", "generating", "progress",
                      "total_chapters", "stats", "errors", "completed"]:
                del st.session_state[k]
            st.rerun()

    elif not st.session_state.generating:
        generate_btn = st.button(
            "⚠️ Generate Book",
            type="primary",
            use_container_width=True,
            disabled=len(topic.strip()) < 10,
        )

        if len(topic.strip()) < 10:
            st.info("Enter a book topic to get started")

        if generate_btn and topic.strip():
            st.session_state.generating = True
            st.session_state.completed = False
            st.session_state.chapters = {}
            st.session_state.errors = []
            st.session_state.stats = {"tokens": 0, "time": 0, "speed": 0}
            st.session_state.words_per_chapter = words_per_chapter
            st.rerun()

    # Progress display during generation
    if st.session_state.generating:
        st.info("Generating your book... this may take a few minutes.")
        if st.session_state.total_chapters > 0:
            prog = st.session_state.progress / st.session_state.total_chapters
            st.progress(prog, text=f"{st.session_state.progress}/{st.session_state.total_chapters} chapters complete")
        else:
            st.progress(0, text="Generating structure...")

# --- Generation pipeline -----------------------------------------------------
if st.session_state.generating and not st.session_state.completed:
    words_per_chapter = st.session_state.get("words_per_chapter", 1500)

    ai_client, _ = get_client()
    if not ai_client:
        st.error("No API key configured.")
        st.session_state.generating = False
        st.stop()

    with st.spinner("Building book structure..."):
        try:
            # Step 1: Generate title
            book_title = generate_book_title(topic, genre, language, model)
            st.session_state.book_title = book_title

            # Step 2: Generate structure
            structure = generate_book_structure(
                topic, genre, writing_style, num_chapters,
                language, model, additional
            )
            st.session_state.structure = structure
            chapters_list = list(structure.items())
            st.session_state.total_chapters = len(chapters_list)

        except Exception as e:
            st.error(f"Failed to generate structure: {e}")
            st.session_state.generating = False
            st.stop()

    st.markdown(f"## {book_title}")
    st.markdown(f"*{len(chapters_list)} chapters . {genre} . {language}*")
    st.markdown("---")

    # Step 3: Generate chapters
    start_total = time.time()
    total_tokens = 0
    chapter_placeholders = {}

    # Create placeholders for all chapters
    for ch_title, _ in chapters_list:
        chapter_placeholders[ch_title] = st.empty()

    if parallel and max_workers > 1:
        # -- PARALLEL generation ------------------------------------------
        st.info(f"Generating {len(chapters_list)} chapters in parallel ({max_workers} workers)...")

        # For parallel mode, we can't do sequential summarization easily,
        # so we use the structure description as context instead
        results = {}
        errors = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_title = {
                executor.submit(
                    generate_chapter,
                    ch_title, ch_desc,
                    book_title, genre, writing_style,
                    language, model, additional,
                    "",
                    words_per_chapter,
                    ai_client,
                ): ch_title
                for ch_title, ch_desc in chapters_list
            }

            for future in as_completed(future_to_title):
                ch_title = future_to_title[future]
                try:
                    title, content, stats = future.result()
                    results[title] = content
                    st.session_state.chapters[title] = content
                    st.session_state.progress += 1
                    total_tokens += stats["output_tokens"] + stats["input_tokens"]

                    if title in chapter_placeholders:
                        preview = content[:300].replace("\n", " ").strip()
                        chapter_placeholders[title].markdown(
                            f'<div class="chapter-card"><div class="chapter-card-title">⚠️ {title}</div>'
                            f'<div class="chapter-card-preview">{preview}...</div></div>',
                            unsafe_allow_html=True,
                        )

                except Exception as e:
                    err_msg = f"{ch_title}: {str(e)}"
                    errors.append(err_msg)
                    st.session_state.errors.append(err_msg)
                    if ch_title in chapter_placeholders:
                        chapter_placeholders[ch_title].error(f"⚠️ Failed: {ch_title} - {e}")

        # Reorder chapters to match original structure
        st.session_state.chapters = {
            t: results.get(t, f"*Chapter generation failed - see errors below*")
            for t, _ in chapters_list
        }

    else:
        # -- SEQUENTIAL generation with continuity ----------------------
        st.info("Generating chapters sequentially with continuity context...")
        prev_summary = ""

        for i, (ch_title, ch_desc) in enumerate(chapters_list):
            with st.spinner(f"Writing chapter {i+1}/{len(chapters_list)}: {ch_title}..."):
                try:
                    _, content, stats = generate_chapter(
                        ch_title, ch_desc,
                        book_title, genre, writing_style,
                        language, model, additional,
                        prev_summary,
                        words_per_chapter,
                        ai_client,
                    )
                    st.session_state.chapters[ch_title] = content
                    st.session_state.progress += 1
                    total_tokens += stats["output_tokens"] + stats["input_tokens"]

                    preview = content[:300].replace("\n", " ").strip()
                    chapter_placeholders[ch_title].markdown(
                        f'<div class="chapter-card"><div class="chapter-card-title">⚠️ {ch_title}</div>'
                        f'<div class="chapter-card-preview">{preview}...</div></div>',
                        unsafe_allow_html=True,
                    )

                    # Generate summary for next chapter's context
                    if i < len(chapters_list) - 1:
                        prev_summary = summarize_chapter(content, model, language, ai_client)

                except Exception as e:
                    st.session_state.errors.append(str(e))
                    st.session_state.chapters[ch_title] = f"*Error generating this chapter: {e}*"
                    st.session_state.progress += 1

    # -- Final stats ---------------------------------------------------------
    elapsed = time.time() - start_total
    st.session_state.stats = {
        "tokens": total_tokens,
        "time": elapsed,
        "speed": total_tokens / elapsed if elapsed > 0 else 0,
    }
    st.session_state.generating = False
    st.session_state.completed = True
    st.rerun()

# --- Display completed book --------------------------------------------------
if st.session_state.completed and st.session_state.chapters:
    st.markdown("---")
    st.markdown(f"# {st.session_state.book_title}")

    tabs = st.tabs(list(st.session_state.chapters.keys())[:20])  # Max 20 tabs
    for tab, (ch_title, content) in zip(tabs, list(st.session_state.chapters.items())[:20]):
        with tab:
            st.markdown(content)

    if st.session_state.errors:
        with st.expander(f"{len(st.session_state.errors)} errors during generation"):
            for err in st.session_state.errors:
                st.error(err)

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important; }

/* App page navbar */
.app-navbar {
    background: rgba(9,9,11,0.95); border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 14px 28px; display: flex; align-items: center; justify-content: space-between;
    margin: -1rem -1rem 1.5rem; position: sticky; top: 0; z-index: 100;
    backdrop-filter: blur(12px);
}
.app-nav-logo { font-size: 17px; font-weight: 800; color: #fff; display:flex;align-items:center;gap:8px; }
.app-nav-logo span { color: #A8FF4B; }
.app-nav-back {
    color: #6B7280; font-size: 13px; text-decoration: none;
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.09);
    padding: 6px 14px; border-radius: 7px; transition: all .2s; font-weight: 500;
}
.app-nav-back:hover { color: #fff; background: rgba(255,255,255,0.08); }

/* Main headings */
.main-header {
    font-size: 2.4rem; font-weight: 900;
    background: linear-gradient(135deg, #7C3AED 0%, #A855F7 50%, #EC4899 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: .15em; letter-spacing: -1.5px;
}
.sub-header { color: #6B7280; font-size: 1rem; margin-bottom: 2em; }

/* Stat boxes */
.stat-box {
    background: #111113; border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px; padding: 14px 18px; text-align: center;
}
.stat-val { font-size: 1.5rem; font-weight: 900; color: #A8FF4B; letter-spacing: -1px; }
.stat-label { font-size: .72rem; color: #6B7280; margin-top: 3px; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; }

/* Chapter tracker */
.chapter-done {
    background: rgba(168,255,75,0.07); border-left: 3px solid #A8FF4B;
    padding: 7px 12px; border-radius: 6px; margin: 4px 0; font-size: .88rem; color: #D1D5DB;
}
.chapter-pending {
    background: rgba(255,255,255,0.03); border-left: 3px solid #374151;
    padding: 7px 12px; border-radius: 6px; margin: 4px 0; font-size: .88rem; color: #4B5563;
}

/* Streamlit component overrides */
div[data-testid="stSelectbox"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSlider"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stRadio"] label { color: #9CA3AF !important; font-size: 13px !important; font-weight: 600 !important; }
</style>
''', unsafe_allow_html=True)