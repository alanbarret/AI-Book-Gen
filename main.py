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

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Book Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Constants ────────────────────────────────────────────────────────────────
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

# ─── Session state ─────────────────────────────────────────────────────────
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
        "errors": [],
        "completed": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── AI Client ──────────────────────────────────────────────────────────────
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

def ai_complete(messages, model, max_tokens=4096, temperature=0.7, stream=False, json_mode=False):
    """Single AI call with retry logic — supports Groq and OpenAI."""
    client, provider = get_client()
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

# ─── Generation functions ────────────────────────────────────────────────────
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
        f"Minimum 1500 words per chapter."
    )

    user_prompt = (
        f"Write the full chapter: **{chapter_title}**\n\n"
        f"Subchapters to cover:\n{subchapters}\n"
        f"{context}\n"
        f"Additional instructions: {additional or 'None'}\n\n"
        f"Write the complete chapter now. Be thorough and detailed."
    )

    start = time.time()
    content = ""

    stream = ai_complete(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model=model,
        max_tokens=4096,
        temperature=0.6,
        stream=True,
    )

    input_tokens = output_tokens = 0
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            content += delta
        if hasattr(chunk, 'x_groq') and chunk.x_groq and chunk.x_groq.usage:
            u = chunk.x_groq.usage
            input_tokens = u.prompt_tokens
            output_tokens = u.completion_tokens

    elapsed = time.time() - start
    stats = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "time": elapsed,
        "speed": output_tokens / elapsed if elapsed > 0 else 0,
    }
    return chapter_title, content, stats


def summarize_chapter(content: str, model: str, language: str) -> str:
    """Generate a brief summary of a chapter for continuity context."""
    resp = ai_complete(
        messages=[
            {"role": "system", "content": f"Summarize in 2-3 sentences in {language}. Output only the summary."},
            {"role": "user", "content": f"Summarize this chapter:\n\n{content[:3000]}"}
        ],
        model=model,
        max_tokens=150,
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()


# ─── Export ──────────────────────────────────────────────────────────────────
def build_markdown(title: str, chapters: dict) -> str:
    md = f"# {title}\n\n---\n\n"
    for ch_title, content in chapters.items():
        md += f"## {ch_title}\n\n{content}\n\n---\n\n"
    return md


def build_pdf(title: str, chapters: dict) -> bytes:
    md_content = build_markdown(title, chapters)
    html = markdown(md_content, extensions=["extra"])
    styled = f"""
    <html><head><style>
    @page {{ margin: 2.5cm; }}
    body {{ font-family: Georgia, serif; line-height: 1.8; font-size: 12pt; color: #222; }}
    h1 {{ font-size: 28pt; color: #1a1a2e; text-align: center; page-break-after: always; margin-top: 40%; }}
    h2 {{ font-size: 18pt; color: #2d3561; margin-top: 2em; page-break-before: always; border-bottom: 2px solid #2d3561; padding-bottom: .3em; }}
    h3 {{ font-size: 14pt; color: #444; margin-top: 1.5em; }}
    p {{ margin-bottom: .8em; text-align: justify; }}
    hr {{ border: none; border-top: 1px solid #ccc; margin: 2em 0; }}
    blockquote {{ border-left: 4px solid #2d3561; padding-left: 1em; font-style: italic; color: #555; }}
    </style></head><body>{html}</body></html>
    """
    from weasyprint import HTML as WHTML
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        WHTML(string=styled).write_pdf(f.name)
        return open(f.name, "rb").read()


# ─── UI ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main-header { font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: .2em; }
.sub-header { color: #666; font-size: 1rem; margin-bottom: 2em; }
.stat-box { background: #f8f9fa; border-radius: 8px; padding: 12px 16px; text-align: center; }
.stat-val { font-size: 1.4rem; font-weight: 700; color: #2d3561; }
.stat-label { font-size: .75rem; color: #888; margin-top: 2px; }
.chapter-done { background: #d4edda; border-left: 4px solid #28a745; padding: 6px 12px;
    border-radius: 4px; margin: 4px 0; font-size: .9rem; }
.chapter-pending { background: #f8f9fa; border-left: 4px solid #ccc; padding: 6px 12px;
    border-radius: 4px; margin: 4px 0; font-size: .9rem; color: #888; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📚 AI Book Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Write full-length books in minutes — with parallel AI generation</div>', unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    provider = st.radio(
        "AI Provider",
        ["Groq", "OpenAI"],
        index=0 if st.session_state.provider == "Groq" else 1,
        horizontal=True,
        help="Groq is free and fast. OpenAI requires a paid key."
    )
    if provider != st.session_state.provider:
        st.session_state.provider = provider
        st.session_state.groq_client = None
        st.session_state.openai_client = None

    if provider == "Groq":
        api_key = st.text_input(
            "Groq API Key",
            value=st.session_state.groq_api_key,
            type="password",
            help="Free at console.groq.com",
        )
        if api_key != st.session_state.groq_api_key:
            st.session_state.groq_api_key = api_key
            st.session_state.groq_client = None
        model = st.selectbox("Model", GROQ_MODELS, index=0,
                              help="Llama 3.3 70B = best quality · Llama 3.1 8B = fastest")
    else:
        api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.openai_api_key,
            type="password",
            help="Get your key at platform.openai.com",
        )
        if api_key != st.session_state.openai_api_key:
            st.session_state.openai_api_key = api_key
            st.session_state.openai_client = None
        model = st.selectbox("Model", OPENAI_MODELS, index=0,
                              help="GPT-4o = best quality · GPT-4o-mini = cheapest")

    st.markdown("---")
    st.markdown("### 📊 Generation Stats")
    if st.session_state.stats["tokens"] > 0:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="stat-box"><div class="stat-val">{st.session_state.stats["tokens"]:,}</div><div class="stat-label">Total Tokens</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-box"><div class="stat-val">{st.session_state.stats["speed"]:.0f}</div><div class="stat-label">Tokens/sec</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-box"><div class="stat-val">{st.session_state.stats["time"]:.1f}s</div><div class="stat-label">Total Time</div></div>', unsafe_allow_html=True)
    else:
        st.info("Stats will appear during generation")

    if st.session_state.chapters:
        st.markdown("---")
        st.markdown("### 📑 Chapters")
        for title in st.session_state.structure.keys():
            done = title in st.session_state.chapters
            icon = "✅" if done else "⏳"
            st.markdown(f"{icon} {title[:35]}{'...' if len(title)>35 else ''}")

# ─── Main form ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("### 📝 Book Details")

    topic = st.text_area(
        "What is your book about?",
        placeholder="E.g., 'The psychology of habit formation and how to rewire your brain for success'",
        height=100,
    )

    genre = st.selectbox("Genre", BOOK_GENRES)
    writing_style = st.selectbox("Writing Style", WRITING_STYLES)

    c1, c2 = st.columns(2)
    with c1:
        num_chapters = st.slider("Number of Chapters", 5, 25, 10)
    with c2:
        language = st.selectbox("Language", ["English", "Arabic", "French", "Spanish", "German"])

    additional = st.text_area(
        "Additional Instructions (optional)",
        placeholder="E.g., 'Include real-world examples', 'Target audience: beginners', 'Add exercises at end of each chapter'",
        height=80,
    )

    parallel = st.toggle("⚡ Parallel Generation", value=True,
                          help="Generate multiple chapters simultaneously — much faster but uses more API credits")

    max_workers = st.slider("Parallel Workers", 2, 6, 3,
                             disabled=not parallel,
                             help="How many chapters to generate at once") if parallel else 1

with col_right:
    st.markdown("### 🚀 Generate")

    if st.session_state.completed and st.session_state.chapters:
        st.success(f"✅ **{st.session_state.book_title}** is ready!")

        # Download buttons
        md_content = build_markdown(st.session_state.book_title, st.session_state.chapters)
        st.download_button(
            "📄 Download Markdown",
            data=md_content.encode("utf-8"),
            file_name=f"{st.session_state.book_title}.md",
            mime="text/markdown",
            use_container_width=True,
        )

        try:
            pdf_bytes = build_pdf(st.session_state.book_title, st.session_state.chapters)
            st.download_button(
                "📕 Download PDF",
                data=pdf_bytes,
                file_name=f"{st.session_state.book_title}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.warning(f"PDF export unavailable: {e}")

        if st.button("🔄 Generate New Book", use_container_width=True):
            for k in ["book", "book_title", "structure", "chapters", "generating", "progress",
                      "total_chapters", "stats", "errors", "completed"]:
                del st.session_state[k]
            st.rerun()

    elif not st.session_state.generating:
        generate_btn = st.button(
            "✨ Generate Book",
            type="primary",
            use_container_width=True,
            disabled=not (st.session_state.groq_api_key or st.session_state.openai_api_key) or len(topic.strip()) < 10,
        )

        has_key = st.session_state.groq_api_key if st.session_state.provider == "Groq" else st.session_state.openai_api_key
        if not has_key:
            st.warning(f"⚠️ Enter your {st.session_state.provider} API key in the sidebar")
        elif len(topic.strip()) < 10:
            st.info("Enter a book topic to get started")

        active_key = st.session_state.groq_api_key if st.session_state.provider == "Groq" else st.session_state.openai_api_key
        if generate_btn and topic.strip() and active_key:
            st.session_state.generating = True
            st.session_state.completed = False
            st.session_state.chapters = {}
            st.session_state.errors = []
            st.session_state.stats = {"tokens": 0, "time": 0, "speed": 0}
            st.rerun()

    # Progress display during generation
    if st.session_state.generating:
        st.info("🔄 Generating your book... this may take a few minutes.")
        if st.session_state.total_chapters > 0:
            prog = st.session_state.progress / st.session_state.total_chapters
            st.progress(prog, text=f"{st.session_state.progress}/{st.session_state.total_chapters} chapters complete")
        else:
            st.progress(0, text="Generating structure...")

# ─── Generation pipeline ─────────────────────────────────────────────────────
if st.session_state.generating and not st.session_state.completed:

    with st.spinner("🏗️ Building book structure..."):
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
            st.error(f"❌ Failed to generate structure: {e}")
            st.session_state.generating = False
            st.stop()

    st.markdown(f"## 📖 {book_title}")
    st.markdown(f"*{len(chapters_list)} chapters · {genre} · {language}*")
    st.markdown("---")

    # Step 3: Generate chapters
    start_total = time.time()
    total_tokens = 0
    chapter_placeholders = {}

    # Create placeholders for all chapters
    for ch_title, _ in chapters_list:
        chapter_placeholders[ch_title] = st.empty()

    if parallel and max_workers > 1:
        # ── PARALLEL generation ──────────────────────────────────────────
        st.info(f"⚡ Generating {len(chapters_list)} chapters in parallel ({max_workers} workers)...")

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
                    ""  # No prev summary in parallel mode
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

                    # Update placeholder
                    if title in chapter_placeholders:
                        chapter_placeholders[title].markdown(
                            f"### ✅ {title}\n\n{content[:500]}...\n\n---"
                        )

                except Exception as e:
                    errors.append(f"{ch_title}: {str(e)}")
                    st.session_state.errors.append(str(e))

        # Reorder chapters to match original structure
        st.session_state.chapters = {
            t: results.get(t, "*Chapter generation failed*")
            for t, _ in chapters_list
        }

    else:
        # ── SEQUENTIAL generation with continuity ──────────────────────
        st.info("📝 Generating chapters sequentially with continuity context...")
        prev_summary = ""

        for i, (ch_title, ch_desc) in enumerate(chapters_list):
            with st.spinner(f"Writing chapter {i+1}/{len(chapters_list)}: {ch_title}..."):
                try:
                    _, content, stats = generate_chapter(
                        ch_title, ch_desc,
                        book_title, genre, writing_style,
                        language, model, additional,
                        prev_summary
                    )
                    st.session_state.chapters[ch_title] = content
                    st.session_state.progress += 1
                    total_tokens += stats["output_tokens"] + stats["input_tokens"]

                    chapter_placeholders[ch_title].markdown(
                        f"### ✅ {ch_title}\n\n{content[:400]}...\n\n---"
                    )

                    # Generate summary for next chapter's context
                    if i < len(chapters_list) - 1:
                        prev_summary = summarize_chapter(content, model, language)

                except Exception as e:
                    st.session_state.errors.append(str(e))
                    st.session_state.chapters[ch_title] = f"*Error generating this chapter: {e}*"
                    st.session_state.progress += 1

    # ── Final stats ─────────────────────────────────────────────────────────
    elapsed = time.time() - start_total
    st.session_state.stats = {
        "tokens": total_tokens,
        "time": elapsed,
        "speed": total_tokens / elapsed if elapsed > 0 else 0,
    }
    st.session_state.generating = False
    st.session_state.completed = True
    st.rerun()

# ─── Display completed book ──────────────────────────────────────────────────
if st.session_state.completed and st.session_state.chapters:
    st.markdown("---")
    st.markdown(f"# 📖 {st.session_state.book_title}")

    tabs = st.tabs(list(st.session_state.chapters.keys())[:20])  # Max 20 tabs
    for tab, (ch_title, content) in zip(tabs, list(st.session_state.chapters.items())[:20]):
        with tab:
            st.markdown(content)

    if st.session_state.errors:
        with st.expander(f"⚠️ {len(st.session_state.errors)} errors during generation"):
            for err in st.session_state.errors:
                st.error(err)
