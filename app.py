
import streamlit as st
import zipfile
import tempfile
import os
from io import BytesIO
from engine_openai import (
    generate_all_summaries,
    save_summary_as_html,
    save_summary_as_markdown,
    prompt_summary,
    detect_language,
    ask_gpt
)
from markdown2 import markdown
from xhtml2pdf import pisa

st.set_page_config(page_title="Agentic Code Summary Assistant", layout="wide")

# --- Custom CSS for fixed sidebar layout ---
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            min-width: 425px;
            max-width: 425px;
            width: 320px;
        }
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
        textarea, .stTextInput, .stFileUploader {
            width: 100% !important;
        }
        button[kind="download"] {
            width: 100%;
        }
        .block-container > div {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Info ---
with st.sidebar:
    st.markdown("## 🧠 Agentic Code Summary Assistant")
    st.markdown("### 📘 What is it?")
    st.write("An intelligent summarization tool powered by GPT-4o to analyze and explain source code from various languages like Python, Java, JavaScript, and C++.")

    st.markdown("### 🤖 Why this Tool")
    st.write("Manual documentation is time-consuming. This assistant automates summarization, usage examples, and confidence scoring — reducing engineering overhead.")

    st.markdown("### ⚙️ How it Works")
    st.markdown("""
    1. Paste code or upload source files (.py, .js, .java, .cpp) or a zip archive.  
    2. The assistant detects language and uses a language-specific GPT-4o prompt.  
    3. It generates summaries, usage examples, and confidence scores.  
    4. Download the result in PDF, HTML, or Markdown.
    """)

# --- Main Panel ---
st.markdown("<h1 style='text-align:center;'>🧠 Agentic Code Summary Assistant</h1>", unsafe_allow_html=True)

st.markdown("#### 📥 Paste your code here")
pasted_code = st.text_area("", height=200, placeholder="Paste any supported code snippet here (Python, Java, JS, C++)")

st.markdown("#### 📁 Or upload files")
uploaded_file = st.file_uploader("Upload .zip file with .py, .js, .java, or .cpp files", type=["zip"])

summaries = []

if pasted_code and not uploaded_file:
    with st.spinner("Processing pasted code..."):
        lang = detect_language("snippet.py")
        prompt = prompt_summary(pasted_code, lang)
        summary = ask_gpt(prompt)
        summaries.append(("snippet.py", lang, summary))
        for file_name, lang, summary in summaries:
            st.markdown(f"### 🧠 {file_name} ({lang})\n\n{summary}", unsafe_allow_html=True)

elif uploaded_file:
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, uploaded_file.name)
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        except zipfile.BadZipFile:
            st.error("❌ Uploaded file is not a valid ZIP archive.")
            st.stop()
        except EOFError:
            st.error("❌ ZIP file is corrupted or incomplete. Please re-upload a valid .zip file.")
            st.stop()

        with st.spinner("Processing uploaded zip..."):
            summaries = generate_all_summaries(temp_dir)
            for file_name, lang, summary in summaries:
                st.markdown(f"### 🧠 {file_name} ({lang})\n\n{summary}", unsafe_allow_html=True)

if (pasted_code or uploaded_file) and summaries:
    st.markdown("#### 📤 Export Summary")
    c1, c2, c3 = st.columns(3)

    with tempfile.TemporaryDirectory() as temp_dir:
        with c1:
            html_path = os.path.join(temp_dir, "summary_output.html")
            save_summary_as_html(summaries, html_path)
            with open(html_path, "rb") as f:
                st.download_button("💾 HTML", f, file_name="code_summary.html", mime="text/html")

        with c2:
            md_path = os.path.join(temp_dir, "summary_output.md")
            save_summary_as_markdown(summaries, md_path)
            with open(md_path, "rb") as f:
                st.download_button("📝 Markdown", f, file_name="code_summary.md", mime="text/markdown")

        with c3:
            html_string = markdown("".join([f"## {file}\n\n{summary}" for file, _, summary in summaries]))
            pdf_file = BytesIO()
            pisa_status = pisa.CreatePDF(src=html_string, dest=pdf_file)
            if not pisa_status.err:
                pdf_file.seek(0)
                st.download_button("📄 PDF", pdf_file, file_name="code_summary.pdf", mime="application/pdf")
            else:
                st.error("❌ PDF generation failed.")

st.markdown("""
<hr style='margin-top:20px;'>
<div style='text-align:center; font-size:0.85em; color:gray;'>ⓒ 2025 Nithish Kondapaka™ – All rights reserved</div>
""", unsafe_allow_html=True)
