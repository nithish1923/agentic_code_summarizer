import streamlit as st
import zipfile
import tempfile
import os
from io import BytesIO
from engine_openai import generate_all_summaries, save_summary_as_html, save_summary_as_markdown
from markdown2 import markdown
from xhtml2pdf import pisa

st.set_page_config(page_title="📘 Agentic GenAI – Code Summary Assistant", layout="wide")
st.title("📘 Agentic GenAI – Code Summary Assistant")

col_left, col_right = st.columns([1.3, 1])

with col_left:
    st.markdown("""
    ### 🤖 What is Agentic GenAI?
    Agentic GenAI refers to autonomous generative AI that can reason, decide, and act on inputs.  
    In this app, it reads your codebase and produces intelligent summaries using *GPT-4o*.

    ---

    ### 🛠️ What This Tool Solves:
    Developers waste hours interpreting messy or undocumented code.

    This assistant automates:
    - 🧠 Code summaries
    - 💡 Usage examples
    - 📊 Confidence scoring (self-review)

    ---

    ### ⚙️ How It Works:
    1. Upload a .zip of your .py files.
    2. GPT-4o analyzes each file and generates:
        - Summary  
        - Example  
        - Score
    3. You can export the results in HTML, Markdown, or PDF.
    """)

with col_right:
    uploaded_file = st.file_uploader("📦 Upload your Python Codebase (.zip):", type=["zip"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, uploaded_file.name)
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        st.info("⏳ Analyzing uploaded code...")
        summaries = generate_all_summaries(temp_dir)
        st.success("✅ Summary generation complete!")

        for section in summaries:
            st.markdown(section, unsafe_allow_html=True)

        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💾 Export as HTML"):
                html_path = os.path.join(temp_dir, "summary_output.html")
                save_summary_as_html(summaries, html_path)
                with open(html_path, "rb") as f:
                    st.download_button("Download HTML", f, file_name="code_summary.html", mime="text/html")

        with col2:
            if st.button("📝 Export as Markdown"):
                md_path = os.path.join(temp_dir, "summary_output.md")
                save_summary_as_markdown(summaries, md_path)
                with open(md_path, "rb") as f:
                    st.download_button("Download Markdown", f, file_name="code_summary.md", mime="text/markdown")

        with col3:
            if st.button("📄 Export as PDF"):
                html_string = markdown("".join(summaries))
                pdf_file = BytesIO()
                pisa_status = pisa.CreatePDF(src=html_string, dest=pdf_file)
                if not pisa_status.err:
                    pdf_file.seek(0)
                    st.download_button("Download PDF", pdf_file, file_name="code_summary.pdf", mime="application/pdf")
                else:
                    st.error("❌ PDF generation failed.")

        st.markdown("""
        <footer style='text-align:center; padding-top:2rem; font-size:0.85em; color:gray;'>
            ⓒ 2025 Nithish Kondapaka™ – All rights reserved
        </footer>
        """, unsafe_allow_html=True)
