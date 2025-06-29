import streamlit as st
import zipfile
import tempfile
import os
from io import BytesIO
from engine_openai import generate_all_summaries, save_summary_as_html, save_summary_as_markdown
from markdown2 import markdown
from xhtml2pdf import pisa

st.set_page_config(page_title="Code Summary Assistant", layout="wide")
st.markdown("<h2 style='text-align:center;'>📘 Code Summary Assistant</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### 🤖 About")
    st.markdown("- Generate intelligent summaries from Python code using GPT-4o")
    st.markdown("- Includes usage examples and self-review scores")
    st.markdown("- Export summaries as PDF, Markdown, or HTML")

    with st.expander("📘 How it works", expanded=False):
        st.markdown("""
        1. Upload a .zip of .py files  
        2. GPT-4o analyzes each file  
        3. Generates:
           - Summary  
           - Usage Example  
           - Confidence Score  
        """)

with col2:
    uploaded_file = st.file_uploader("📥 Upload .zip of Python files", type=["zip"])

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

st.markdown("<hr style='margin-top:20px;'>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; font-size:0.85em; color:gray;'>ⓒ 2025 Nithish Kondapaka™ – All rights reserved</div>", unsafe_allow_html=True)
