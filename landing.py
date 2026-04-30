"""
Landing Page — AI Book Generator by Inspired Technology
Redesigned: Dark SaaS style with purple/violet sections + neon green accents
"""
import streamlit as st


def show_landing():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

    /* ── Reset ── */
    [data-testid="stAppViewContainer"] { background: #09090B !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    * { font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; box-sizing: border-box; }

    /* ── Navbar ── */
    .navbar {
        position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
        background: rgba(9,9,11,0.88); backdrop-filter: blur(16px);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        padding: 16px 48px; display: flex; align-items: center; justify-content: space-between;
    }
    .nav-logo { display: flex; align-items: center; gap: 8px; text-decoration: none; }
    .nav-logo-icon {
        width: 34px; height: 34px; border-radius: 8px;
        background: linear-gradient(135deg, #7C3AED, #A855F7);
        display: flex; align-items: center; justify-content: center;
        font-size: 18px;
    }
    .nav-logo-text { font-size: 17px; font-weight: 800; color: #fff; letter-spacing: -.3px; }
    .nav-logo-text span { color: #A8FF4B; }
    .nav-links { display: flex; gap: 32px; }
    .nav-links a { color: #9CA3AF; font-size: 14px; font-weight: 500; text-decoration: none; transition: color .2s; }
    .nav-links a:hover { color: #fff; }
    .nav-cta {
        background: #A8FF4B; color: #09090B !important; padding: 9px 22px !important;
        border-radius: 8px; font-weight: 700 !important; font-size: 14px !important;
        transition: all .2s; box-shadow: 0 0 20px rgba(168,255,75,0.3);
    }
    .nav-cta:hover { background: #BFFF6E !important; transform: translateY(-1px); box-shadow: 0 0 28px rgba(168,255,75,0.45) !important; }

    /* ── Hero ── */
    .hero {
        min-height: 100vh; padding: 130px 48px 80px;
        background: radial-gradient(ellipse 70% 50% at 50% -5%, rgba(124,58,237,0.3) 0%, transparent 65%),
                    radial-gradient(ellipse 40% 40% at 80% 60%, rgba(168,85,247,0.12) 0%, transparent 60%),
                    #09090B;
        display: flex; flex-direction: column; align-items: center; text-align: center;
    }
    .hero-badge {
        display: inline-flex; align-items: center; gap: 8px;
        background: rgba(124,58,237,0.15); border: 1px solid rgba(124,58,237,0.4);
        border-radius: 100px; padding: 7px 18px; font-size: 13px; color: #C4B5FD;
        font-weight: 600; margin-bottom: 32px; letter-spacing: .02em;
    }
    .badge-dot { width: 6px; height: 6px; background: #A8FF4B; border-radius: 50%; animation: pulse 2s infinite; }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
    .hero-title {
        font-size: clamp(42px, 6.5vw, 78px); font-weight: 900; color: #fff;
        line-height: 1.05; letter-spacing: -2.5px; margin-bottom: 24px;
        max-width: 900px;
    }
    .hero-title .hi { color: #A8FF4B; }
    .hero-title .vi {
        background: linear-gradient(135deg, #7C3AED 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-sub { font-size: clamp(16px,2vw,19px); color: #6B7280; max-width: 580px; line-height: 1.75; margin-bottom: 40px; }

    .hero-btns { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; margin-bottom: 64px; }
    .btn-green {
        background: #A8FF4B; color: #09090B; border: none; border-radius: 10px;
        padding: 14px 32px; font-size: 16px; font-weight: 800; cursor: pointer;
        box-shadow: 0 0 24px rgba(168,255,75,0.35); transition: all .2s;
        text-decoration: none; display: inline-block;
    }
    .btn-green:hover { background: #BFFF6E; transform: translateY(-2px); box-shadow: 0 0 36px rgba(168,255,75,0.5); }
    .btn-outline {
        background: transparent; color: #E5E7EB; border: 1px solid rgba(255,255,255,0.15);
        border-radius: 10px; padding: 14px 32px; font-size: 16px; font-weight: 600;
        cursor: pointer; transition: all .2s; text-decoration: none; display: inline-block;
    }
    .btn-outline:hover { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.3); }

    /* Hero stats cards */
    .hero-stats { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
    .stat-card {
        background: #141414; border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px; padding: 18px 24px; text-align: center; min-width: 130px;
    }
    .stat-card .num { font-size: 28px; font-weight: 900; color: #A8FF4B; letter-spacing: -1px; }
    .stat-card .lbl { font-size: 12px; color: #6B7280; margin-top: 4px; font-weight: 500; }

    /* Trust logos */
    .trust-row {
        display: flex; align-items: center; justify-content: center; gap: 36px;
        padding: 40px 48px; border-top: 1px solid rgba(255,255,255,0.05);
        border-bottom: 1px solid rgba(255,255,255,0.05);
        background: rgba(255,255,255,0.015);
    }
    .trust-label { font-size: 12px; color: #4B5563; font-weight: 600; text-transform: uppercase; letter-spacing: .1em; }
    .trust-logo { font-size: 14px; font-weight: 700; color: #374151; letter-spacing: -.3px; }

    /* ── Section base ── */
    .section { padding: 90px 48px; max-width: 1200px; margin: 0 auto; }
    .section-full { padding: 90px 48px; }
    .chip {
        display: inline-block; background: rgba(124,58,237,0.12);
        border: 1px solid rgba(124,58,237,0.3); border-radius: 100px;
        padding: 5px 14px; font-size: 12px; color: #A78BFA; font-weight: 700;
        text-transform: uppercase; letter-spacing: .08em; margin-bottom: 18px;
    }
    .s-title { font-size: clamp(30px,4vw,48px); font-weight: 900; color: #fff; letter-spacing: -1.5px; line-height: 1.1; margin-bottom: 14px; }
    .s-sub { font-size: 17px; color: #6B7280; line-height: 1.7; max-width: 520px; }

    /* ── Why choose us — Purple section ── */
    .purple-section {
        background: linear-gradient(145deg, #6D28D9 0%, #7C3AED 40%, #8B5CF6 100%);
        padding: 90px 48px; position: relative; overflow: hidden;
    }
    .purple-section::before {
        content:''; position:absolute; top:-50%; right:-10%; width:600px; height:600px;
        border-radius:50%; background:rgba(255,255,255,0.05); pointer-events:none;
    }
    .purple-section .s-title { color: #fff; }
    .purple-section .s-sub { color: rgba(255,255,255,0.7); }
    .why-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; margin-top: 50px; }
    .why-card {
        background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px; padding: 28px; backdrop-filter: blur(10px); transition: all .25s;
    }
    .why-card:hover { background: rgba(255,255,255,0.13); transform: translateY(-4px); }
    .why-icon { font-size: 28px; margin-bottom: 14px; }
    .why-title { font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 8px; }
    .why-desc { font-size: 14px; color: rgba(255,255,255,0.65); line-height: 1.65; }

    /* ── Features ── */
    .features-split { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }
    .feature-list { display: flex; flex-direction: column; gap: 14px; margin-top: 32px; }
    .feature-item {
        display: flex; align-items: flex-start; gap: 14px;
        background: #141414; border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px; padding: 16px 18px; transition: all .2s;
    }
    .feature-item:hover { border-color: rgba(124,58,237,0.4); background: rgba(124,58,237,0.05); }
    .feature-icon { font-size: 22px; flex-shrink: 0; margin-top: 2px; }
    .feature-title { font-size: 15px; font-weight: 700; color: #E5E7EB; }
    .feature-desc { font-size: 13px; color: #6B7280; margin-top: 3px; line-height: 1.55; }

    /* ── Stats visual ── */
    .stats-visual {
        background: #111113; border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px; padding: 28px; position: relative; overflow: hidden;
    }
    .stats-visual::before {
        content:''; position:absolute; top:0; left:0; right:0; height:2px;
        background: linear-gradient(90deg, #7C3AED, #A8FF4B, #7C3AED);
    }
    .speed-num { font-size: 56px; font-weight: 900; color: #fff; letter-spacing: -2px; line-height: 1; }
    .speed-unit { font-size: 16px; color: #A8FF4B; font-weight: 700; margin-left: 4px; }
    .mini-bar { height: 6px; border-radius: 3px; background: rgba(255,255,255,0.08); margin: 8px 0; overflow: hidden; }
    .mini-bar-fill { height: 100%; border-radius: 3px; background: linear-gradient(90deg, #7C3AED, #A8FF4B); }

    /* ── Testimonials ── */
    .testimonials-section { background: #0D0D10; padding: 90px 48px; }
    .testimonial-card {
        background: #141414; border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px; padding: 36px; max-width: 680px; margin: 48px auto 0;
        position: relative;
    }
    .testimonial-card::before { content: '"'; font-size: 80px; color: rgba(124,58,237,0.2); position:absolute; top:10px; left:24px; font-family:Georgia,serif; line-height:1; }
    .test-stars { color: #A8FF4B; font-size: 18px; margin-bottom: 16px; }
    .test-quote { font-size: 16px; color: #D1D5DB; line-height: 1.75; font-style: italic; margin-bottom: 24px; }
    .test-author { display: flex; align-items: center; gap: 12px; }
    .test-avatar { width: 44px; height: 44px; border-radius: 50%; background: linear-gradient(135deg,#7C3AED,#A855F7); display:flex;align-items:center;justify-content:center;font-size:18px; }
    .test-name { font-weight: 700; color: #fff; font-size: 15px; }
    .test-role { font-size: 12px; color: #6B7280; }

    /* ── Final CTA ── */
    .cta-section {
        margin: 0; padding: 90px 48px; text-align: center;
        background: linear-gradient(145deg, #6D28D9 0%, #7C3AED 50%, #5B21B6 100%);
        position: relative; overflow: hidden;
    }
    .cta-section::before {
        content:''; position:absolute; bottom:-30%; right:-5%; width:500px; height:500px;
        border-radius:50%; background:rgba(168,255,75,0.07); pointer-events:none;
    }
    .cta-title { font-size: clamp(32px,5vw,58px); font-weight: 900; color: #fff; letter-spacing: -2px; margin-bottom: 16px; line-height:1.1; }
    .cta-sub { font-size: 18px; color: rgba(255,255,255,0.72); margin-bottom: 40px; }

    /* ── Footer ── */
    .footer { background: #07070A; border-top: 1px solid rgba(255,255,255,0.05); padding: 60px 48px 30px; }
    .footer-grid { display: grid; grid-template-columns: 2.2fr 1fr 1fr 1fr; gap: 48px; max-width: 1200px; margin: 0 auto; }
    .footer-brand-desc { font-size: 14px; color: #4B5563; margin-top: 14px; max-width: 260px; line-height: 1.7; }
    .footer-col h4 { font-size: 12px; font-weight: 700; color: #E5E7EB; text-transform: uppercase; letter-spacing: .1em; margin-bottom: 18px; }
    .footer-col a { display: block; font-size: 14px; color: #4B5563; text-decoration: none; margin-bottom: 10px; transition: color .2s; }
    .footer-col a:hover { color: #A78BFA; }
    .footer-bottom {
        max-width: 1200px; margin: 44px auto 0; padding-top: 22px;
        border-top: 1px solid rgba(255,255,255,0.05);
        display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;
        font-size: 13px; color: #374151;
    }
    .footer-bottom a { color: #4B5563; text-decoration: none; }
    .footer-bottom a:hover { color: #A78BFA; }

    /* ── Mobile ── */
    @media (max-width: 768px) {
        .navbar { padding: 14px 20px; }
        .nav-links { display: none; }
        .hero { padding: 110px 20px 60px; }
        .why-grid { grid-template-columns: 1fr; }
        .features-split { grid-template-columns: 1fr; }
        .footer-grid { grid-template-columns: 1fr 1fr; }
        .section { padding: 60px 20px; }
        .section-full, .purple-section, .cta-section, .testimonials-section { padding: 60px 20px; }
        .trust-row { gap: 20px; flex-wrap: wrap; padding: 30px 20px; }
    }
    </style>

    <!-- NAVBAR -->
    <div class="navbar">
        <a class="nav-logo" href="#">
            <div class="nav-logo-icon">📚</div>
            <div class="nav-logo-text">AI Book<span>Gen</span></div>
        </a>
        <div class="nav-links">
            <a href="#">Features</a>
            <a href="#">How it Works</a>
            <a href="#">Pricing</a>
            <a href="https://inspiredtechnology.ae" target="_blank">Inspired Technology</a>
        </div>
        <a href="#" onclick="window.top.location.href=window.top.location.pathname+'?start=1'; return false;" class="nav-cta" id="navCta">Try for Free</a>
    </div>

    <!-- HERO -->
    <div class="hero">
        <div class="hero-badge">
            <span class="badge-dot"></span>
            AI-Powered · Powered by Inspired Technology
        </div>
        <h1 class="hero-title">
            The <span class="hi">Smartest</span> Way<br>
            to Write Your <span class="vi">Book</span>
        </h1>
        <p class="hero-sub">
            Transform your ideas into full-length books in minutes using parallel AI generation.
            Fiction, non-fiction, technical guides, biographies — any genre, any language.
        </p>
        <div class="hero-btns">
            <a href="#" onclick="window.top.location.href=window.top.location.pathname+'?start=1'; return false;" class="btn-green" id="heroStart">Start Writing Free</a>
            <a href="https://inspiredtechnology.ae" target="_blank" class="btn-outline">Learn More →</a>
        </div>
        <div class="hero-stats">
            <div class="stat-card"><div class="num">10+</div><div class="lbl">Book Genres</div></div>
            <div class="stat-card"><div class="num">5x</div><div class="lbl">Faster with AI</div></div>
            <div class="stat-card"><div class="num">500</div><div class="lbl">Max Pages</div></div>
            <div class="stat-card"><div class="num">5</div><div class="lbl">Languages</div></div>
            <div class="stat-card"><div class="num">2</div><div class="lbl">AI Providers</div></div>
        </div>
    </div>

    <!-- TRUST ROW -->
    <div class="trust-row">
        <span class="trust-label">Powered by</span>
        <span class="trust-logo">🤖 Groq</span>
        <span class="trust-logo">🧠 OpenAI</span>
        <span class="trust-logo">📄 fpdf2</span>
        <span class="trust-logo">⚡ Streamlit</span>
        <span class="trust-logo">🏢 Inspired Technology</span>
    </div>

    <!-- WHY CHOOSE US — Purple -->
    <div class="purple-section">
        <div style="max-width:1200px;margin:0 auto;position:relative;z-index:1">
            <div class="chip">Why AI BookGen</div>
            <h2 class="s-title">The Reason Why<br>Choose Us?</h2>
            <p class="s-sub">We blend technology and creativity to give you everything you need to write a world-class book — faster than ever.</p>
            <div class="why-grid">
                <div class="why-card">
                    <div class="why-icon">⚡</div>
                    <div class="why-title">Parallel Generation</div>
                    <div class="why-desc">Multiple chapters written simultaneously — up to 5x faster than any sequential approach. Your book is ready in minutes.</div>
                </div>
                <div class="why-card">
                    <div class="why-icon">🎯</div>
                    <div class="why-title">Perfect Structure</div>
                    <div class="why-desc">AI builds a detailed chapter-by-chapter outline tailored to your topic, genre, and writing style before writing a single word.</div>
                </div>
                <div class="why-card">
                    <div class="why-icon">🌍</div>
                    <div class="why-title">Multi-Language</div>
                    <div class="why-desc">Write in English, Arabic, French, Spanish, or German. Full Unicode and RTL support for every writing system.</div>
                </div>
                <div class="why-card">
                    <div class="why-icon">🔗</div>
                    <div class="why-title">Chapter Continuity</div>
                    <div class="why-desc">Sequential mode passes chapter summaries as context — your book flows naturally, like a real author wrote it.</div>
                </div>
                <div class="why-card">
                    <div class="why-icon">🤖</div>
                    <div class="why-title">Dual AI Providers</div>
                    <div class="why-desc">Switch between Groq (free, blazing fast) and OpenAI GPT-4o (maximum quality). You're always in control.</div>
                </div>
                <div class="why-card">
                    <div class="why-icon">📄</div>
                    <div class="why-title">PDF & Markdown Export</div>
                    <div class="why-desc">Download your finished book as a beautifully formatted PDF or Markdown file — ready to publish or share instantly.</div>
                </div>
            </div>
        </div>
    </div>

    <!-- FEATURES SPLIT -->
    <div class="section-full" style="background:#09090B;padding:90px 48px">
        <div style="max-width:1200px;margin:0 auto">
            <div class="features-split">
                <div>
                    <div class="chip">Meet Your AI Author</div>
                    <h2 class="s-title">Everything You<br>Need to Write<br>a Great Book</h2>
                    <p class="s-sub">From your first idea to a complete manuscript — our AI handles every step while you stay creative director.</p>
                </div>
                <div class="feature-list">
                    <div class="feature-item">
                        <div class="feature-icon">✍️</div>
                        <div>
                            <div class="feature-title">AI Book Structure Builder</div>
                            <div class="feature-desc">Generates a detailed chapter outline from your topic in seconds — no planning needed.</div>
                        </div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🎭</div>
                        <div>
                            <div class="feature-title">10 Genres, 6 Writing Styles</div>
                            <div class="feature-desc">Fiction, non-fiction, technical, biography, business, science — each with tailored AI prompting.</div>
                        </div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">📊</div>
                        <div>
                            <div class="feature-title">Target Pages Control</div>
                            <div class="feature-desc">Set your target from 50 to 500 pages — the AI automatically adjusts depth per chapter.</div>
                        </div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">⬇️</div>
                        <div>
                            <div class="feature-title">One-Click Export</div>
                            <div class="feature-desc">Download as styled PDF or Markdown the moment your book is complete. No extra steps.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- SAVE TIME SECTION -->
    <div class="section-full" style="background:#0D0D10;padding:90px 48px">
        <div style="max-width:1200px;margin:0 auto">
            <div class="features-split">
                <!-- Stats visual -->
                <div class="stats-visual">
                    <div style="color:#6B7280;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;margin-bottom:20px">Generation Speed</div>
                    <div><span class="speed-num">5</span><span class="speed-unit">× Faster</span></div>
                    <div style="color:#6B7280;font-size:13px;margin:8px 0 24px">vs. sequential generation</div>
                    <div style="color:#9CA3AF;font-size:12px;font-weight:600;margin-bottom:6px">Chapter Progress</div>
                    <div class="mini-bar"><div class="mini-bar-fill" style="width:85%"></div></div>
                    <div class="mini-bar"><div class="mini-bar-fill" style="width:70%"></div></div>
                    <div class="mini-bar"><div class="mini-bar-fill" style="width:92%"></div></div>
                    <div style="display:flex;gap:10px;margin-top:20px;flex-wrap:wrap">
                        <div style="background:rgba(168,255,75,0.1);border:1px solid rgba(168,255,75,0.3);border-radius:8px;padding:8px 14px;font-size:12px;color:#A8FF4B;font-weight:700">✓ Groq Free</div>
                        <div style="background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.3);border-radius:8px;padding:8px 14px;font-size:12px;color:#A78BFA;font-weight:700">✓ OpenAI GPT-4o</div>
                        <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:8px 14px;font-size:12px;color:#9CA3AF;font-weight:700">✓ PDF Export</div>
                    </div>
                </div>
                <div>
                    <div class="chip">Save Time & Money</div>
                    <h2 class="s-title">Write Faster.<br>Write Smarter.<br>Publish Sooner.</h2>
                    <p class="s-sub">Our parallel AI engine generates multiple chapters at once — what would take days of writing takes minutes. Focus on your ideas, not the typing.</p>
                    <div style="margin-top:28px;display:flex;flex-direction:column;gap:12px">
                        <div style="display:flex;align-items:center;gap:10px;font-size:14px;color:#D1D5DB">
                            <span style="color:#A8FF4B;font-weight:700">✓</span> No writing skills required
                        </div>
                        <div style="display:flex;align-items:center;gap:10px;font-size:14px;color:#D1D5DB">
                            <span style="color:#A8FF4B;font-weight:700">✓</span> Full book in under 10 minutes
                        </div>
                        <div style="display:flex;align-items:center;gap:10px;font-size:14px;color:#D1D5DB">
                            <span style="color:#A8FF4B;font-weight:700">✓</span> Export-ready PDF instantly
                        </div>
                        <div style="display:flex;align-items:center;gap:10px;font-size:14px;color:#D1D5DB">
                            <span style="color:#A8FF4B;font-weight:700">✓</span> Free with Groq API key
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- HOW IT WORKS -->
    <div class="section" style="text-align:center">
        <div class="chip">Simple Process</div>
        <h2 class="s-title" style="max-width:600px;margin:0 auto 14px">From Idea to Book<br>in 4 Simple Steps</h2>
        <p class="s-sub" style="margin:0 auto">No technical knowledge needed. Just describe your book and let AI do the rest.</p>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin-top:50px;text-align:left">
            <div style="background:#111113;border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:28px;position:relative;overflow:hidden">
                <div style="font-size:48px;font-weight:900;color:rgba(168,255,75,0.12);position:absolute;top:12px;right:18px;line-height:1">1</div>
                <div style="font-size:26px;margin-bottom:14px">💡</div>
                <div style="font-size:16px;font-weight:700;color:#E5E7EB;margin-bottom:8px">Describe Your Book</div>
                <div style="font-size:13px;color:#6B7280;line-height:1.65">Enter your topic, choose genre, writing style, language, and how many pages you want.</div>
            </div>
            <div style="background:#111113;border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:28px;position:relative;overflow:hidden">
                <div style="font-size:48px;font-weight:900;color:rgba(168,255,75,0.12);position:absolute;top:12px;right:18px;line-height:1">2</div>
                <div style="font-size:26px;margin-bottom:14px">🏗️</div>
                <div style="font-size:16px;font-weight:700;color:#E5E7EB;margin-bottom:8px">AI Builds Structure</div>
                <div style="font-size:13px;color:#6B7280;line-height:1.65">A detailed chapter-by-chapter outline is generated and tailored to your topic instantly.</div>
            </div>
            <div style="background:#111113;border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:28px;position:relative;overflow:hidden">
                <div style="font-size:48px;font-weight:900;color:rgba(168,255,75,0.12);position:absolute;top:12px;right:18px;line-height:1">3</div>
                <div style="font-size:26px;margin-bottom:14px">⚡</div>
                <div style="font-size:16px;font-weight:700;color:#E5E7EB;margin-bottom:8px">Parallel AI Writing</div>
                <div style="font-size:13px;color:#6B7280;line-height:1.65">Multiple AI workers write chapters simultaneously — your full book is done in minutes.</div>
            </div>
            <div style="background:#111113;border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:28px;position:relative;overflow:hidden">
                <div style="font-size:48px;font-weight:900;color:rgba(168,255,75,0.12);position:absolute;top:12px;right:18px;line-height:1">4</div>
                <div style="font-size:26px;margin-bottom:14px">📥</div>
                <div style="font-size:16px;font-weight:700;color:#E5E7EB;margin-bottom:8px">Download & Publish</div>
                <div style="font-size:13px;color:#6B7280;line-height:1.65">Export your completed book as a beautifully styled PDF or Markdown file — ready to share.</div>
            </div>
        </div>
    </div>

    <!-- TESTIMONIALS -->
    <div class="testimonials-section" style="text-align:center">
        <div class="chip">What They Say</div>
        <h2 class="s-title">Loved by Authors<br>Everywhere</h2>
        <div class="testimonial-card">
            <div class="test-stars">★★★★★</div>
            <p class="test-quote">"I wrote my first business book in under 20 minutes. The chapter structure was spot-on, the writing was professional, and the PDF looked incredible. This tool is genuinely magical."</p>
            <div class="test-author">
                <div class="test-avatar">👨‍💼</div>
                <div>
                    <div class="test-name">Sarah Johnson</div>
                    <div class="test-role">Entrepreneur · Dubai, UAE</div>
                </div>
            </div>
        </div>
        <div class="testimonial-card" style="margin-top:16px">
            <div class="test-stars">★★★★★</div>
            <p class="test-quote">"The Arabic language support is exceptional. I generated a 200-page technical guide in Arabic and the quality was outstanding. Inspired Technology really delivered something special."</p>
            <div class="test-author">
                <div class="test-avatar">👨‍🔬</div>
                <div>
                    <div class="test-name">Ahmed Al-Rashid</div>
                    <div class="test-role">Technical Writer · Abu Dhabi, UAE</div>
                </div>
            </div>
        </div>
    </div>

    <!-- FINAL CTA -->
    <div class="cta-section">
        <div style="position:relative;z-index:1">
            <h2 class="cta-title">Harness the Limitless<br>Potential of AI Writing</h2>
            <p class="cta-sub">Join the future of creative writing — powered by Inspired Technology's AI solutions.</p>
            <a href="#" onclick="window.top.location.href=window.top.location.pathname+'?start=1'; return false;" class="btn-green" id="ctaBtn">Start Writing for Free</a>
            <div style="margin-top:20px;font-size:13px;color:rgba(255,255,255,0.45)">No credit card required · Free with Groq API key</div>
        </div>
    </div>

    <!-- FOOTER -->
    <div class="footer">
        <div class="footer-grid">
            <div>
                <div style="display:flex;align-items:center;gap:8px">
                    <div style="width:32px;height:32px;border-radius:7px;background:linear-gradient(135deg,#7C3AED,#A855F7);display:flex;align-items:center;justify-content:center;font-size:16px">📚</div>
                    <span style="font-size:16px;font-weight:800;color:#fff">AI Book<span style="color:#A8FF4B">Gen</span></span>
                </div>
                <p class="footer-brand-desc">An Inspired Technology product. We blend technology, art, and strategy to turn your ideas into real impact.</p>
                <a href="https://inspiredtechnology.ae" target="_blank" style="color:#A78BFA;font-size:13px;text-decoration:none;margin-top:14px;display:inline-block">🌐 inspiredtechnology.ae ↗</a>
            </div>
            <div class="footer-col">
                <h4>Product</h4>
                <a href="#">Features</a>
                <a href="#">How it Works</a>
                <a href="#">Pricing</a>
                <a href="https://github.com/alanbarret/AI-Book-Gen" target="_blank">GitHub</a>
            </div>
            <div class="footer-col">
                <h4>Company</h4>
                <a href="https://inspiredtechnology.ae" target="_blank">About Us</a>
                <a href="https://inspiredtechnology.ae" target="_blank">Services</a>
                <a href="https://inspiredtechnology.ae" target="_blank">Blog</a>
                <a href="https://inspiredtechnology.ae" target="_blank">Contact</a>
            </div>
            <div class="footer-col">
                <h4>Get Started</h4>
                <a href="https://console.groq.com" target="_blank">Groq API Key (Free)</a>
                <a href="https://platform.openai.com" target="_blank">OpenAI API Key</a>
                <a href="https://github.com/alanbarret/AI-Book-Gen" target="_blank">Documentation</a>
            </div>
        </div>
        <div class="footer-bottom">
            <span>© 2026 Inspired Technology · Making Technology Work for You!</span>
            <span>Built with ❤️ by <a href="https://inspiredtechnology.ae" target="_blank">Inspired Technology</a></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
