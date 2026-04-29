# 📚 AI Book Generator

Generate full-length books in minutes using AI — with parallel chapter generation for maximum speed.

## ✨ Features vs Original Research Paper Generator

| Feature | Research Paper Gen | **AI Book Gen** |
|---|---|---|
| Generation | Sequential | **Parallel (3-6x faster)** |
| Content type | Academic papers | **Fiction, Non-fiction, Technical, Biography...** |
| Chapter continuity | None | **Chapter summaries passed as context** |
| Exports | MD + PDF | **MD + PDF (styled)** |
| Languages | EN + AR | **EN, AR, FR, ES, DE** |
| Structure depth | Sections | **Chapters + Subchapters** |
| Writing styles | Fixed | **6 configurable styles** |
| Error handling | Basic | **Retry logic + per-chapter recovery** |

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Run
streamlit run main.py
```

## ⚡ Parallel Generation

The key optimization: instead of generating chapters one-by-one (slow), the app generates multiple chapters simultaneously using `ThreadPoolExecutor`. A 10-chapter book goes from ~10 minutes to ~3 minutes.

```
Sequential:  Ch1 → Ch2 → Ch3 → Ch4 → Ch5  (each waits for previous)
Parallel:    Ch1 ↘
             Ch2 → all finish together
             Ch3 ↗
```

## 🔑 Get Free API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up and create an API key
3. Enter it in the sidebar

## 📋 Requirements

- Python 3.9+
- Groq API key (free tier available)
- `weasyprint` for PDF export (requires system dependencies)
