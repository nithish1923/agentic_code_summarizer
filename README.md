# 🤖 CodeWhisperer – AI-Powered Code Summarizer Assistant

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agenticcodesummarizer-rtfvo2mzhnhtypuoavniju.streamlit.app/)

**CodeWhisperer** is an intelligent Streamlit-based AI assistant that analyzes and summarizes source code using OpenAI's GPT-4o. It supports multiple programming languages, provides smart summaries, usage examples, and lets you export results in PDF, HTML, and Markdown formats.

---

## 🚀 Features

- 🧠 AI-powered code summarization using **GPT-4o**
- 📥 Accepts input via:
  - Direct code paste
  - `.zip` uploads for full codebases
- 🌐 Supports multiple languages:
  - Python
  - JavaScript
  - Java
  - C++
  - And more
- 📄 Generates summaries with:
  - Code purpose
  - Function/class descriptions
  - Parameters and return values
  - Usage notes
  - Realistic usage examples
  - Confidence score
- 📤 Export results as:
  - PDF
  - HTML
  - Markdown
- 🧩 Modular design:
  - `app.py`: UI logic (Streamlit)
  - `engine_openai.py`: AI prompt handling and summarization engine

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/codewhisperer.git
cd codewhisperer
