import streamlit as st
import zipfile
import tempfile
import os
from io import BytesIO
from engine_openai import generate_all_summaries, save_summary_as_html, save_summary_as_markdown
from markdown2 import markdown
from xhtml2pdf import pisa

st.set_page_config(page_title="📘 Code Summary Assistant", layout="centered")

st.markdown("<h1 style='text-align:center;'>📘 Code Summary Assistant</h1>", unsafe_allow_html=True)

st.markdown("""
### 🧠 What is a Code Summary Assistant?
A GPT-4o powered tool that reads Python code and generates intelligent summaries, usage examples, and confidence scores.

---

### 🛠️ Why This Tool?
Developers often struggle with undocumented or legacy code. This assistant helps by auto-documenting your codebase.

---

### ⚙️ How It Works:
1. Upload a .zip of .py files  
2. GPT-4o will:
    - 🔍 Analyze each file  
    - ✍️ Generate summaries & examples  
    - 📊 Add confidence score  
3. Export the output in *PDF / Markdown / HTML*

---
""")

uploaded_file = st.file_uploader("📥 Upload your Python Codebase (.zip)", type=["zip"], label_visibility="visible")

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

        st.markdown("### 📤 Export Options:")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💾 HTML"):
                html_path = os.path.join(temp_dir, "summary_output.html")
                save_summary_as_html(summaries, html_path)
                with open(html_path, "rb") as f:
                    st.download_button("Download HTML", f, file_name="code_summary.html", mime="text/html")

        with col2:
            if st.button("📝 Markdown"):
                md_path = os.path.join(temp_dir, "summary_output.md")
                save_summary_as_markdown(summaries, md_path)
                with open(md_path, "rb") as f:
                    st.download_button("Download Markdown", f, file_name="code_summary.md", mime="text/markdown")

        with col3:
            if st.button("📄 PDF"):
                html_string = markdown("".join(summaries))
                pdf_file = BytesIO()
                pisa_status = pisa.CreatePDF(src=html_string, dest=pdf_file)
                if not pisa_status.err:
                    pdf_file.seek(0)
                    st.download_button("Download PDF", pdf_file, file_name="code_summary.pdf", mime="application/pdf")
                else:
                    st.error("❌ PDF generation failed.")

        st.markdown("""
        <hr>
        <div style='text-align:center; font-size:0.85em; color:gray;'>
            ⓒ 2025 Nithish Kondapaka™ – All rights reserved
        </div>
        """, unsafe_allow_html=True)
