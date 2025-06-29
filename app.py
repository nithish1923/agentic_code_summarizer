import streamlit as st
import zipfile
import tempfile
import os
from io import BytesIO
from engine_openai import generate_all_summaries, save_summary_as_html, save_summary_as_markdown
from markdown2 import markdown
from xhtml2pdf import pisa

# Set wide layout
st.set_page_config(page_title="Agentic GenAI – Code Summary Assistant", layout="wide")

# Header
st.markdown("<h1 style='text-align:center;'>🧠 Agentic GenAI – Code Summary Assistant</h1>", unsafe_allow_html=True)

# Two-column layout
left_col, right_col = st.columns([1, 2])

# LEFT: Upload section
with left_col:
    st.markdown("#### 📂 Upload .zip of Python files")
    uploaded_file = st.file_uploader(
        "Drag and drop file here", type=["zip"], label_visibility="collapsed"
    )

# RIGHT: About + How it works
with right_col:
    st.markdown("### 📘 About the Assistant")
    st.write(
        "Generates smart, human-readable summaries from your Python code using GPT-4o.\n"
        "Includes function descriptions, usage examples, and self-evaluated confidence."
    )

    st.markdown("### ⚙️ How It Works")
    st.markdown("""
    1. *Upload* a .zip file containing your .py files  
    2. *GPT-4o* reads and summarizes each module, class, and function  
    3. *Export* results as *HTML, **Markdown, or **PDF*
    """)

# File processing
if uploaded_file:
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, uploaded_file.name)
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        st.success("✅ Code uploaded and processing...")
        summaries = generate_all_summaries(temp_dir)
        st.info("✅ Summaries generated below")

        for section in summaries:
            st.markdown(section, unsafe_allow_html=True)

        st.markdown("#### 📤 Export Summary")
        export1, export2, export3 = st.columns(3)

        with export1:
            html_path = os.path.join(temp_dir, "summary_output.html")
            save_summary_as_html(summaries, html_path)
            with open(html_path, "rb") as f:
                st.download_button("💾 HTML", f, file_name="code_summary.html", mime="text/html")

        with export2:
            md_path = os.path.join(temp_dir, "summary_output.md")
            save_summary_as_markdown(summaries, md_path)
            with open(md_path, "rb") as f:
                st.download_button("📝 Markdown", f, file_name="code_summary.md", mime="text/markdown")

        with export3:
            html_string = markdown("".join(summaries))
            pdf_file = BytesIO()
            pisa_status = pisa.CreatePDF(src=html_string, dest=pdf_file)
            if not pisa_status.err:
                pdf_file.seek(0)
                st.download_button("📄 PDF", pdf_file, file_name="code_summary.pdf", mime="application/pdf")
            else:
                st.error("❌ PDF generation failed.")

# Footer branding
st.markdown("""
<hr style='margin-top:20px;'>
<div style='text-align:center; font-size:0.85em; color:gray;'>ⓒ 2025 Nithish Kondapaka™ – All rights reserved</div>
""", unsafe_allow_html=True)
