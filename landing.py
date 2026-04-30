"""
Landing Page — AI Book Generator by Inspired Technology
"""
import streamlit as st


def show_landing():
    st.markdown("""
    <style>
    /* ── Reset & base ────────────────────────────────────────────── */
    *, *::before, *::after { box-sizing: border-box; }
    [data-testid="stAppViewContainer"] { background: #06060f; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* ── Navbar ──────────────────────────────────────────────────── */
    .lp-nav {
        position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
        background: rgba(6,6,15,0.85); backdrop-filter: blur(18px);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        height: 60px; padding: 0 40px;
        display: flex; align-items: center; justify-content: space-between;
    }
    .lp-nav-logo { font-size: 17px; font-weight: 800; color: #f9fafb; display: flex; align-items: center; gap: 8px; }
    .lp-nav-logo .ac { color: #8b5cf6; }
    .lp-nav-links { display: flex; gap: 28px; align-items: center; }
    .lp-nav-links a { color: #9ca3af; font-size: 14px; font-weight: 500; text-decoration: none; transition: color .2s; }
    .lp-nav-links a:hover { color: #e5e7eb; }
    .lp-nav-cta {
        background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
        color: #fff !important; padding: 7px 18px !important;
        border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important;
    }

    /* ── Hero ────────────────────────────────────────────────────── */
    .lp-hero {
        min-height: 100vh; display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        padding: 110px 24px 70px; text-align: center;
        background:
            radial-gradient(ellipse 110% 55% at 50% -5%, rgba(124,58,237,0.32) 0%, transparent 68%),
            radial-gradient(ellipse 55% 45% at 85% 65%, rgba(168,85,247,0.13) 0%, transparent 58%),
            #06060f;
        position: relative; overflow: hidden;
    }
    .lp-hero::before {
        content: ""; position: absolute; inset: 0; pointer-events: none;
        background-image: radial-gradient(rgba(139,92,246,0.06) 1px, transparent 1px);
        background-size: 36px 36px;
    }
    .lp-badge {
        position: relative; z-index: 1;
        display: inline-flex; align-items: center; gap: 8px;
        background: rgba(124,58,237,0.1); border: 1px solid rgba(139,92,246,0.35);
        border-radius: 100px; padding: 6px 18px;
        font-size: 12px; color: #c4b5fd; font-weight: 600;
        letter-spacing: .05em; text-transform: uppercase; margin-bottom: 28px;
    }
    .lp-dot { width: 6px; height: 6px; border-radius: 50%; background: #8b5cf6; display:inline-block; animation: lpdot 2s infinite; }
    @keyframes lpdot { 0%,100%{opacity:1} 50%{opacity:.3} }
    .lp-h1 {
        position: relative; z-index: 1;
        font-size: clamp(38px, 6.5vw, 78px); font-weight: 900;
        line-height: 1.04; color: #f9fafb; letter-spacing: -2.5px; margin-bottom: 22px;
    }
    .lp-h1 .gr {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 45%, #ec4899 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .lp-sub {
        position: relative; z-index: 1;
        font-size: clamp(15px, 2.2vw, 19px); color: #6b7280;
        max-width: 580px; margin: 0 auto 40px; line-height: 1.78;
    }
    .lp-btns { position: relative; z-index: 1; display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-bottom: 52px; }
    .lp-btn-p {
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        color: #fff; border: none; border-radius: 12px;
        padding: 15px 34px; font-size: 16px; font-weight: 700;
        cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; gap: 8px;
        box-shadow: 0 0 36px rgba(124,58,237,0.45), 0 4px 20px rgba(0,0,0,0.4);
        transition: transform .2s, box-shadow .2s;
    }
    .lp-btn-p:hover { transform: translateY(-2px); box-shadow: 0 0 52px rgba(124,58,237,0.55), 0 8px 28px rgba(0,0,0,0.5); }
    .lp-btn-g {
        background: rgba(255,255,255,0.04); color: #d1d5db;
        border: 1px solid rgba(255,255,255,0.1); border-radius: 12px;
        padding: 15px 34px; font-size: 16px; font-weight: 600;
        text-decoration: none; display: inline-flex; align-items: center; gap: 8px;
        transition: background .2s, border-color .2s;
    }
    .lp-btn-g:hover { background: rgba(255,255,255,0.07); border-color: rgba(255,255,255,0.18); }
    .lp-pills { position: relative; z-index: 1; display: flex; flex-wrap: wrap; gap: 9px; justify-content: center; max-width: 700px; }
    .lp-pill {
        background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
        border-radius: 100px; padding: 6px 14px; font-size: 13px; color: #9ca3af; white-space: nowrap; line-height: 1;
    }

    /* ── Stats band ──────────────────────────────────────────────── */
    .lp-stats {
        display: flex; flex-wrap: wrap;
        border-top: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        background: rgba(255,255,255,0.015);
    }
    .lp-stat { flex: 1 1 150px; text-align: center; padding: 32px 20px; border-right: 1px solid rgba(255,255,255,0.05); }
    .lp-stat:last-child { border-right: none; }
    .lp-stat-n { font-size: 34px; font-weight: 800; color: #8b5cf6; line-height: 1; }
    .lp-stat-l { font-size: 13px; color: #6b7280; margin-top: 6px; }

    /* ── Sections ────────────────────────────────────────────────── */
    .lp-section { padding: 90px 40px; max-width: 1200px; margin: 0 auto; }
    .lp-eyebrow {
        display: inline-block;
        background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.25);
        border-radius: 100px; padding: 4px 14px;
        font-size: 11px; color: #a78bfa; font-weight: 700;
        text-transform: uppercase; letter-spacing: .1em; margin-bottom: 18px;
    }
    .lp-sh { font-size: clamp(26px, 4vw, 44px); font-weight: 800; color: #f3f4f6; margin-bottom: 14px; letter-spacing: -1px; line-height: 1.15; }
    .lp-sp { font-size: 16px; color: #6b7280; max-width: 540px; line-height: 1.78; }

    /* Feature cards */
    .lp-feat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 52px; }
    .lp-feat-card {
        background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px; padding: 28px 24px;
        transition: border-color .25s, background .25s, transform .25s;
    }
    .lp-feat-card:hover { background: rgba(139,92,246,0.07); border-color: rgba(139,92,246,0.3); transform: translateY(-3px); }
    .lp-feat-icon {
        width: 50px; height: 50px; border-radius: 13px;
        background: linear-gradient(135deg, rgba(124,58,237,0.22), rgba(168,85,247,0.12));
        border: 1px solid rgba(139,92,246,0.2);
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; margin-bottom: 18px;
    }
    .lp-feat-title { font-size: 16px; font-weight: 700; color: #e5e7eb; margin-bottom: 8px; }
    .lp-feat-desc { font-size: 13px; color: #6b7280; line-height: 1.72; }

    /* ── How it works ────────────────────────────────────────────── */
    .lp-how {
        background: rgba(255,255,255,0.012);
        border-top: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding: 90px 40px;
    }
    .lp-how-inner { max-width: 1200px; margin: 0 auto; }
    .lp-steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; margin-top: 52px; position: relative; }
    .lp-steps::before {
        content: ""; position: absolute;
        top: 27px; left: 13%; right: 13%; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139,92,246,0.3) 20%, rgba(139,92,246,0.3) 80%, transparent);
        pointer-events: none;
    }
    .lp-step { text-align: center; padding: 0 16px; }
    .lp-step-n {
        width: 56px; height: 56px; border-radius: 50%;
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        color: #fff; font-weight: 800; font-size: 20px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 20px; position: relative; z-index: 1;
        box-shadow: 0 0 24px rgba(124,58,237,0.4);
    }
    .lp-step-t { font-size: 15px; font-weight: 700; color: #e5e7eb; margin-bottom: 8px; }
    .lp-step-d { font-size: 13px; color: #6b7280; line-height: 1.68; }

    /* ── CTA ─────────────────────────────────────────────────────── */
    .lp-cta {
        margin: 60px 40px; border-radius: 24px; padding: 84px 40px; text-align: center;
        background: linear-gradient(135deg, rgba(124,58,237,0.18), rgba(168,85,247,0.1));
        border: 1px solid rgba(139,92,246,0.25); position: relative; overflow: hidden;
    }
    .lp-cta::before {
        content: ""; position: absolute; top: -80px; right: -80px;
        width: 340px; height: 340px; border-radius: 50%;
        background: radial-gradient(circle, rgba(139,92,246,0.18), transparent 70%); pointer-events: none;
    }
    .lp-cta::after {
        content: ""; position: absolute; bottom: -60px; left: -60px;
        width: 260px; height: 260px; border-radius: 50%;
        background: radial-gradient(circle, rgba(236,72,153,0.1), transparent 70%); pointer-events: none;
    }
    .lp-cta-inner { position: relative; z-index: 1; }
    .lp-cta-h { font-size: clamp(28px, 4vw, 46px); font-weight: 800; color: #f9fafb; margin-bottom: 16px; letter-spacing: -1px; }
    .lp-cta-sub { font-size: 17px; color: #9ca3af; margin-bottom: 38px; max-width: 460px; margin-left: auto; margin-right: auto; }

    /* ── Footer ──────────────────────────────────────────────────── */
    .lp-footer { background: rgba(0,0,0,0.3); border-top: 1px solid rgba(255,255,255,0.05); padding: 64px 40px 32px; }
    .lp-footer-inner { max-width: 1200px; margin: 0 auto; }
    .lp-footer-grid { display: grid; grid-template-columns: 2.2fr 1fr 1fr 1fr; gap: 48px; }
    .lp-footer-brand-p { font-size: 14px; color: #4b5563; margin-top: 12px; max-width: 280px; line-height: 1.72; }
    .lp-footer-col-h { font-size: 11px; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: .1em; margin-bottom: 18px; }
    .lp-footer-col a { display: block; font-size: 14px; color: #4b5563; text-decoration: none; margin-bottom: 10px; transition: color .2s; }
    .lp-footer-col a:hover { color: #a78bfa; }
    .lp-footer-hr { border: none; border-top: 1px solid rgba(255,255,255,0.05); margin: 40px 0 22px; }
    .lp-footer-btm { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; font-size: 13px; color: #374151; }
    .lp-footer-btm a { color: #4b5563; text-decoration: none; }
    .lp-footer-btm a:hover { color: #a78bfa; }

    /* ── Streamlit button overrides for dark landing page ────────── */
    .lp-stbtn > div > div > button {
        background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
        border: none !important; border-radius: 12px !important;
        color: #fff !important; font-weight: 700 !important;
        font-size: 16px !important; padding: 0 36px !important;
        height: 52px !important;
        box-shadow: 0 0 32px rgba(124,58,237,0.4) !important;
        transition: transform .2s, box-shadow .2s !important;
    }
    .lp-stbtn > div > div > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 48px rgba(124,58,237,0.55) !important;
    }

    /* ── Mobile ──────────────────────────────────────────────────── */
    @media (max-width: 900px) {
        .lp-feat-grid { grid-template-columns: repeat(2, 1fr); }
        .lp-steps { grid-template-columns: repeat(2, 1fr); gap: 36px; }
        .lp-steps::before { display: none; }
        .lp-footer-grid { grid-template-columns: 1fr 1fr; gap: 32px; }
    }
    @media (max-width: 640px) {
        .lp-nav { padding: 0 16px; height: 54px; }
        .lp-nav-links { display: none; }
        .lp-hero { padding: 86px 16px 56px; }
        .lp-h1 { letter-spacing: -1.5px; }
        .lp-btns { flex-direction: column; align-items: stretch; max-width: 300px; margin-left: auto; margin-right: auto; }
        .lp-btn-p, .lp-btn-g { padding: 14px 22px; font-size: 15px; width: 100%; justify-content: center; }
        .lp-stat { flex: 1 1 50%; border-right: none; border-bottom: 1px solid rgba(255,255,255,0.05); padding: 22px 14px; }
        .lp-stat:nth-child(odd) { border-right: 1px solid rgba(255,255,255,0.05); }
        .lp-stat:last-child { border-bottom: none; }
        .lp-section { padding: 60px 16px; }
        .lp-feat-grid { grid-template-columns: 1fr; }
        .lp-how { padding: 60px 16px; }
        .lp-steps { grid-template-columns: 1fr; gap: 28px; }
        .lp-cta { margin: 28px 16px; padding: 52px 20px; }
        .lp-footer { padding: 44px 16px 24px; }
        .lp-footer-grid { grid-template-columns: 1fr; gap: 28px; }
        .lp-footer-brand-p { max-width: 100%; }
        .lp-footer-btm { flex-direction: column; text-align: center; }
    }
    </style>

    <!-- Navbar -->
    <div class="lp-nav">
        <div class="lp-nav-logo">📚 AI Book<span class="ac">Gen</span></div>
        <div class="lp-nav-links">
            <a href="#">Features</a>
            <a href="#">How it Works</a>
            <a href="https://inspiredtechnology.ae" target="_blank" class="lp-nav-cta">Inspired Technology ↗</a>
        </div>
    </div>

    <!-- Hero -->
    <div class="lp-hero">
        <div class="lp-badge"><span class="lp-dot"></span>&nbsp;Powered by Inspired Technology</div>
        <h1 class="lp-h1">Write Your Book<br>with <span class="gr">Artificial Intelligence</span></h1>
        <p class="lp-sub">Transform any idea into a full-length, publish-ready book in minutes. Fiction, non-fiction, technical guides, biographies — powered by the fastest AI models available.</p>
        <div class="lp-btns">
            <a href="?start=1" class="lp-btn-p">✨ Start Writing Free</a>
            <a href="https://inspiredtechnology.ae" target="_blank" class="lp-btn-g">Learn More →</a>
        </div>
        <div class="lp-pills">
            <span class="lp-pill">📖 Non-Fiction</span>
            <span class="lp-pill">🎭 Fiction / Novel</span>
            <span class="lp-pill">💻 Technical</span>
            <span class="lp-pill">👤 Biography</span>
            <span class="lp-pill">💼 Business</span>
            <span class="lp-pill">🔬 Science</span>
            <span class="lp-pill">🏛 History</span>
            <span class="lp-pill">🧠 Philosophy</span>
            <span class="lp-pill">🧒 Children's</span>
            <span class="lp-pill">🚀 Fantasy / Sci-Fi</span>
        </div>
    </div>

    <!-- Stats -->
    <div class="lp-stats">
        <div class="lp-stat"><div class="lp-stat-n">10+</div><div class="lp-stat-l">Book Genres</div></div>
        <div class="lp-stat"><div class="lp-stat-n">5x</div><div class="lp-stat-l">Faster Generation</div></div>
        <div class="lp-stat"><div class="lp-stat-n">500</div><div class="lp-stat-l">Max Pages</div></div>
        <div class="lp-stat"><div class="lp-stat-n">5</div><div class="lp-stat-l">Languages</div></div>
        <div class="lp-stat"><div class="lp-stat-n">Free</div><div class="lp-stat-l">With Groq API</div></div>
    </div>

    <!-- Features -->
    <div class="lp-section">
        <div class="lp-eyebrow">Features</div>
        <h2 class="lp-sh">Everything You Need to<br>Write a Great Book</h2>
        <p class="lp-sp">From idea to finished manuscript — the AI handles structure, content, and flow while you stay in control.</p>
        <div class="lp-feat-grid">
            <div class="lp-feat-card">
                <div class="lp-feat-icon">⚡</div>
                <div class="lp-feat-title">Parallel Generation</div>
                <div class="lp-feat-desc">Write multiple chapters simultaneously — up to 5x faster than sequential AI writing. Your whole book, in minutes.</div>
            </div>
            <div class="lp-feat-card">
                <div class="lp-feat-icon">🎭</div>
                <div class="lp-feat-title">10 Book Genres</div>
                <div class="lp-feat-desc">From thriller novels to technical manuals — each genre has its own voice, tone, and structure tailored by AI.</div>
            </div>
            <div class="lp-feat-card">
                <div class="lp-feat-icon">🔗</div>
                <div class="lp-feat-title">Narrative Continuity</div>
                <div class="lp-feat-desc">Sequential mode carries chapter context forward so your book reads as a coherent whole, not disconnected parts.</div>
            </div>
            <div class="lp-feat-card">
                <div class="lp-feat-icon">🌍</div>
                <div class="lp-feat-title">5 Languages</div>
                <div class="lp-feat-desc">Write in English, Arabic, French, Spanish, or German. Full Unicode support for all writing systems and scripts.</div>
            </div>
            <div class="lp-feat-card">
                <div class="lp-feat-icon">🤖</div>
                <div class="lp-feat-title">Groq & OpenAI</div>
                <div class="lp-feat-desc">Use Groq's blazing-fast free Llama models, or switch to GPT-4o for maximum quality. Your choice, any time.</div>
            </div>
            <div class="lp-feat-card">
                <div class="lp-feat-icon">📄</div>
                <div class="lp-feat-title">PDF & Markdown Export</div>
                <div class="lp-feat-desc">Download your book as a formatted PDF or Markdown — print-ready and publish-ready from day one.</div>
            </div>
        </div>
    </div>

    <!-- How it works -->
    <div class="lp-how">
        <div class="lp-how-inner">
            <div class="lp-eyebrow">How it Works</div>
            <h2 class="lp-sh">From Idea to Book in 4 Steps</h2>
            <div class="lp-steps">
                <div class="lp-step">
                    <div class="lp-step-n">1</div>
                    <div class="lp-step-t">Describe Your Book</div>
                    <div class="lp-step-d">Enter your topic, choose a genre, writing style, language, and target page count.</div>
                </div>
                <div class="lp-step">
                    <div class="lp-step-n">2</div>
                    <div class="lp-step-t">AI Builds the Structure</div>
                    <div class="lp-step-d">A detailed chapter-by-chapter outline is generated and tailored to your idea automatically.</div>
                </div>
                <div class="lp-step">
                    <div class="lp-step-n">3</div>
                    <div class="lp-step-t">AI Writes the Book</div>
                    <div class="lp-step-d">Multiple AI workers write chapters in parallel — your full book is ready in minutes, not hours.</div>
                </div>
                <div class="lp-step">
                    <div class="lp-step-n">4</div>
                    <div class="lp-step-t">Download & Publish</div>
                    <div class="lp-step-d">Export as PDF or Markdown and share your finished book with the world instantly.</div>
                </div>
            </div>
        </div>
    </div>

    <!-- CTA -->
    <div class="lp-cta">
        <div class="lp-cta-inner">
            <h2 class="lp-cta-h">Ready to Write Your Book?</h2>
            <p class="lp-cta-sub">Start free with Groq's API — no credit card needed. Your first book is just minutes away.</p>
        </div>
    </div>

    <!-- Footer -->
    <div class="lp-footer">
        <div class="lp-footer-inner">
            <div class="lp-footer-grid">
                <div>
                    <div style="font-size:18px;font-weight:800;color:#e5e7eb">📚 AI BookGen</div>
                    <p class="lp-footer-brand-p">An Inspired Technology product. We blend technology, creativity, and strategy to turn ideas into real-world impact.</p>
                    <div style="margin-top:18px">
                        <a href="https://inspiredtechnology.ae" target="_blank" style="color:#8b5cf6;font-size:13px;text-decoration:none;display:inline-flex;align-items:center;gap:6px;font-weight:600">🌐 inspiredtechnology.ae ↗</a>
                    </div>
                </div>
                <div class="lp-footer-col">
                    <div class="lp-footer-col-h">Product</div>
                    <a href="#">Features</a>
                    <a href="#">How it Works</a>
                    <a href="#">Pricing</a>
                </div>
                <div class="lp-footer-col">
                    <div class="lp-footer-col-h">Company</div>
                    <a href="https://inspiredtechnology.ae" target="_blank">About Us</a>
                    <a href="https://inspiredtechnology.ae" target="_blank">Services</a>
                    <a href="https://inspiredtechnology.ae" target="_blank">Contact</a>
                </div>
                <div class="lp-footer-col">
                    <div class="lp-footer-col-h">Resources</div>
                    <a href="https://console.groq.com" target="_blank">Get Groq Key (Free)</a>
                    <a href="https://platform.openai.com" target="_blank">Get OpenAI Key</a>
                    <a href="https://github.com/alanbarret/AI-Book-Gen" target="_blank">GitHub</a>
                </div>
            </div>
            <hr class="lp-footer-hr">
            <div class="lp-footer-btm">
                <span>© 2026 Inspired Technology. All rights reserved. Making Technology Work for You!</span>
                <span>Built with ❤️ by <a href="https://inspiredtechnology.ae" target="_blank">Inspired Technology</a></span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
