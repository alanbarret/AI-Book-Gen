"""
Landing Page — AI Book Generator by Inspired Technology
"""
import streamlit as st


def show_landing():
    st.markdown("""
    <style>
    /* Reset & base */
    [data-testid="stAppViewContainer"] { background: #0a0a0f; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* Navbar */
    .navbar {
        position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
        background: rgba(10,10,15,0.92); backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255,255,255,0.07);
        padding: 14px 40px; display: flex; align-items: center;
        justify-content: space-between;
    }
    .nav-logo {
        display: flex; align-items: center; gap: 10px;
        font-size: 18px; font-weight: 800; color: #fff; text-decoration: none;
    }
    .nav-logo span { color: #7c6cf8; }
    .nav-links { display: flex; gap: 28px; align-items: center; }
    .nav-links a {
        color: #9ca3af; font-size: 14px; font-weight: 500;
        text-decoration: none; transition: color .2s;
    }
    .nav-links a:hover { color: #fff; }
    .nav-cta {
        background: linear-gradient(135deg, #7c6cf8, #a855f7);
        color: #fff !important; padding: 8px 20px !important;
        border-radius: 8px !important; font-weight: 700 !important;
    }

    /* Hero */
    .hero {
        min-height: 100vh; display: flex; align-items: center; justify-content: center;
        padding: 120px 40px 80px; text-align: center;
        background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(124,108,248,0.25) 0%, transparent 70%),
                    radial-gradient(ellipse 50% 40% at 80% 50%, rgba(168,85,247,0.12) 0%, transparent 60%),
                    #0a0a0f;
        flex-direction: column;
    }
    .hero-badge {
        display: inline-flex; align-items: center; gap: 7px;
        background: rgba(124,108,248,0.12); border: 1px solid rgba(124,108,248,0.3);
        border-radius: 100px; padding: 6px 16px; font-size: 13px; color: #a78bfa;
        font-weight: 600; margin-bottom: 28px;
    }
    .hero-badge::before { content: "✦"; }
    .hero-title {
        font-size: clamp(36px, 6vw, 72px); font-weight: 900; line-height: 1.1;
        color: #fff; margin-bottom: 24px; letter-spacing: -2px;
    }
    .hero-title .grad {
        background: linear-gradient(135deg, #7c6cf8 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        font-size: clamp(16px, 2vw, 20px); color: #6b7280; max-width: 600px;
        margin: 0 auto 40px; line-height: 1.7;
    }
    .hero-btns { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }
    .btn-primary {
        background: linear-gradient(135deg, #7c6cf8, #a855f7);
        color: #fff; border: none; border-radius: 10px; padding: 14px 32px;
        font-size: 16px; font-weight: 700; cursor: pointer;
        box-shadow: 0 4px 24px rgba(124,108,248,0.4);
        transition: all .2s; text-decoration: none; display: inline-block;
    }
    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 32px rgba(124,108,248,0.5); }
    .btn-secondary {
        background: rgba(255,255,255,0.05); color: #e5e7eb;
        border: 1px solid rgba(255,255,255,0.12); border-radius: 10px;
        padding: 14px 32px; font-size: 16px; font-weight: 600; cursor: pointer;
        text-decoration: none; display: inline-block; transition: all .2s;
    }
    .btn-secondary:hover { background: rgba(255,255,255,0.09); }

    /* Stats bar */
    .stats-bar {
        display: flex; justify-content: center; gap: 60px; flex-wrap: wrap;
        padding: 40px; border-top: 1px solid rgba(255,255,255,0.06);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.02);
    }
    .stat-item { text-align: center; }
    .stat-num { font-size: 32px; font-weight: 800; color: #7c6cf8; }
    .stat-lbl { font-size: 13px; color: #6b7280; margin-top: 4px; }

    /* Features */
    .section { padding: 80px 40px; max-width: 1200px; margin: 0 auto; }
    .section-badge {
        display: inline-block; background: rgba(124,108,248,0.1);
        border: 1px solid rgba(124,108,248,0.25); border-radius: 100px;
        padding: 5px 14px; font-size: 12px; color: #a78bfa; font-weight: 600;
        text-transform: uppercase; letter-spacing: .08em; margin-bottom: 16px;
    }
    .section-title {
        font-size: clamp(28px, 4vw, 44px); font-weight: 800; color: #fff;
        margin-bottom: 14px; letter-spacing: -1px; line-height: 1.15;
    }
    .section-sub { font-size: 17px; color: #6b7280; max-width: 560px; line-height: 1.7; }

    .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px,1fr)); gap: 20px; margin-top: 50px; }
    .feature-card {
        background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px; padding: 28px; transition: all .25s;
    }
    .feature-card:hover { background: rgba(124,108,248,0.07); border-color: rgba(124,108,248,0.25); transform: translateY(-3px); }
    .feature-icon { font-size: 28px; margin-bottom: 14px; }
    .feature-title { font-size: 17px; font-weight: 700; color: #e5e7eb; margin-bottom: 8px; }
    .feature-desc { font-size: 14px; color: #6b7280; line-height: 1.7; }

    /* How it works */
    .steps { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap: 24px; margin-top: 50px; }
    .step-card { text-align: center; padding: 32px 20px; }
    .step-num {
        width: 48px; height: 48px; border-radius: 50%;
        background: linear-gradient(135deg, #7c6cf8, #a855f7);
        color: #fff; font-weight: 800; font-size: 18px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 16px;
    }
    .step-title { font-size: 16px; font-weight: 700; color: #e5e7eb; margin-bottom: 8px; }
    .step-desc { font-size: 13px; color: #6b7280; line-height: 1.6; }

    /* CTA section */
    .cta-section {
        margin: 40px; border-radius: 24px; padding: 80px 40px; text-align: center;
        background: linear-gradient(135deg, rgba(124,108,248,0.15), rgba(168,85,247,0.1));
        border: 1px solid rgba(124,108,248,0.2);
    }
    .cta-title { font-size: clamp(28px, 4vw, 42px); font-weight: 800; color: #fff; margin-bottom: 14px; }
    .cta-sub { font-size: 17px; color: #9ca3af; margin-bottom: 36px; }

    /* Footer */
    .footer {
        background: rgba(255,255,255,0.02); border-top: 1px solid rgba(255,255,255,0.06);
        padding: 50px 40px 30px;
    }
    .footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; max-width: 1200px; margin: 0 auto; }
    .footer-brand p { font-size: 14px; color: #6b7280; margin-top: 10px; max-width: 280px; line-height: 1.7; }
    .footer-col h4 { font-size: 13px; font-weight: 700; color: #e5e7eb; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 16px; }
    .footer-col a { display: block; font-size: 14px; color: #6b7280; text-decoration: none; margin-bottom: 8px; transition: color .2s; }
    .footer-col a:hover { color: #a78bfa; }
    .footer-bottom {
        max-width: 1200px; margin: 40px auto 0; padding-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.06);
        display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;
        font-size: 13px; color: #4b5563;
    }
    .footer-bottom a { color: #6b7280; text-decoration: none; }
    .footer-bottom a:hover { color: #a78bfa; }
    </style>

    <!-- Navbar -->
    <div class="navbar">
        <div class="nav-logo">📚 AI Book<span>Gen</span></div>
        <div class="nav-links">
            <a href="#">Features</a>
            <a href="#">How it Works</a>
            <a href="https://inspiredtechnology.ae" target="_blank">Inspired Technology</a>
        </div>
    </div>

    <!-- Hero -->
    <div class="hero">
        <div class="hero-badge">Powered by Inspired Technology · AI & Creative Storytelling</div>
        <h1 class="hero-title">Write Your Book with<br><span class="grad">Artificial Intelligence</span></h1>
        <p class="hero-sub">Transform your ideas into full-length books in minutes. Fiction, non-fiction, technical guides, biographies — powered by cutting-edge AI with parallel generation technology.</p>
        <div class="hero-btns">
            <a href="#" class="btn-primary" id="startBtn">✨ Start Writing Free</a>
            <a href="https://inspiredtechnology.ae" target="_blank" class="btn-secondary">Learn More →</a>
        </div>
    </div>

    <!-- Stats -->
    <div class="stats-bar">
        <div class="stat-item"><div class="stat-num">10+</div><div class="stat-lbl">Book Genres</div></div>
        <div class="stat-item"><div class="stat-num">5x</div><div class="stat-lbl">Faster with Parallel AI</div></div>
        <div class="stat-item"><div class="stat-num">500+</div><div class="stat-lbl">Max Pages</div></div>
        <div class="stat-item"><div class="stat-num">5</div><div class="stat-lbl">Languages</div></div>
        <div class="stat-item"><div class="stat-num">2</div><div class="stat-lbl">AI Providers</div></div>
    </div>

    <!-- Features -->
    <div class="section">
        <div class="section-badge">Features</div>
        <h2 class="section-title">Everything You Need to<br>Write a Great Book</h2>
        <p class="section-sub">From idea to published manuscript — our AI handles the heavy lifting while you stay in control of your vision.</p>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Parallel Generation</div>
                <div class="feature-desc">Generate multiple chapters simultaneously with our ThreadPoolExecutor engine — up to 5x faster than sequential generation.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎭</div>
                <div class="feature-title">10 Book Genres</div>
                <div class="feature-desc">Fiction, Non-fiction, Technical, Biography, Business, Science, History, Philosophy, Children's Books, and Fantasy/Sci-Fi.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔗</div>
                <div class="feature-title">Chapter Continuity</div>
                <div class="feature-desc">Sequential mode passes chapter summaries as context, ensuring your book flows naturally from one chapter to the next.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🌍</div>
                <div class="feature-title">5 Languages</div>
                <div class="feature-desc">Write in English, Arabic, French, Spanish, or German. Full Unicode support for all writing systems.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">Groq & OpenAI</div>
                <div class="feature-desc">Use Groq's blazing-fast Llama models for free, or switch to OpenAI's GPT-4o for maximum quality.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <div class="feature-title">PDF & Markdown Export</div>
                <div class="feature-desc">Download your completed book as a beautifully formatted PDF or Markdown file — ready to publish or share.</div>
            </div>
        </div>
    </div>

    <!-- How it works -->
    <div style="background: rgba(255,255,255,0.015); padding: 80px 40px;">
        <div style="max-width:1200px;margin:0 auto">
            <div class="section-badge">How it Works</div>
            <h2 class="section-title">From Idea to Book in 4 Steps</h2>
            <div class="steps">
                <div class="step-card">
                    <div class="step-num">1</div>
                    <div class="step-title">Describe Your Book</div>
                    <div class="step-desc">Enter your topic, choose genre, writing style, language, and target page count.</div>
                </div>
                <div class="step-card">
                    <div class="step-num">2</div>
                    <div class="step-title">AI Builds Structure</div>
                    <div class="step-desc">Our AI generates a comprehensive chapter-by-chapter outline tailored to your topic.</div>
                </div>
                <div class="step-card">
                    <div class="step-num">3</div>
                    <div class="step-title">Parallel Writing</div>
                    <div class="step-desc">Multiple AI workers write chapters simultaneously — your book is complete in minutes.</div>
                </div>
                <div class="step-card">
                    <div class="step-num">4</div>
                    <div class="step-title">Download & Publish</div>
                    <div class="step-desc">Export as PDF or Markdown and share your finished book with the world.</div>
                </div>
            </div>
        </div>
    </div>

    <!-- CTA -->
    <div class="cta-section">
        <h2 class="cta-title">Ready to Write Your Book?</h2>
        <p class="cta-sub">Join the future of creative writing — powered by Inspired Technology's AI solutions.</p>
        <a href="#" class="btn-primary" id="ctaBtn">✨ Start for Free</a>
    </div>

    <!-- Footer -->
    <div class="footer">
        <div class="footer-grid">
            <div class="footer-brand">
                <div style="font-size:20px;font-weight:800;color:#fff">📚 AI BookGen</div>
                <p>An Inspired Technology product. We blend technology, art, and strategy to turn ideas into real impact.</p>
                <div style="margin-top:16px;display:flex;gap:12px">
                    <a href="https://inspiredtechnology.ae" target="_blank" style="color:#7c6cf8;font-size:13px;text-decoration:none">🌐 inspiredtechnology.ae</a>
                </div>
            </div>
            <div class="footer-col">
                <h4>Product</h4>
                <a href="#">Features</a>
                <a href="#">How it Works</a>
                <a href="#">Pricing</a>
            </div>
            <div class="footer-col">
                <h4>Company</h4>
                <a href="https://inspiredtechnology.ae" target="_blank">About Us</a>
                <a href="https://inspiredtechnology.ae" target="_blank">Services</a>
                <a href="https://inspiredtechnology.ae" target="_blank">Contact</a>
            </div>
            <div class="footer-col">
                <h4>AI Providers</h4>
                <a href="https://console.groq.com" target="_blank">Get Groq Key (Free)</a>
                <a href="https://platform.openai.com" target="_blank">Get OpenAI Key</a>
                <a href="https://github.com/alanbarret/AI-Book-Gen" target="_blank">GitHub</a>
            </div>
        </div>
        <div class="footer-bottom">
            <span>© 2026 Inspired Technology. All rights reserved. Making Technology Work for You!</span>
            <span>Built with ❤️ by <a href="https://inspiredtechnology.ae" target="_blank">Inspired Technology</a></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
