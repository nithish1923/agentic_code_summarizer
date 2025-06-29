import streamlit as st
import zipfile
import tempfile
import os
from engine_openai import generate_all_summaries, save_summary_as_html, save_summary_as_markdown

st.set_page_config(page_title="Agentic GenAI – Code Summary Assistant", layout="centered")

st.title("📘 Agentic GenAI – Code Summary Assistant")
st.markdown("Generate OpenAI-powered summaries, usage examples, and confidence scores for your Python codebase.")

st.markdown("---")

uploaded_file = st.file_uploader("📦 Upload your codebase (.zip containing .py files):", type=["zip"])

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
        col1, col2 = st.columns(2)

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

        st.markdown("<footer style='text-align:center; padding-top:2rem;'>ⓒ 2025 Nithish Kondapaka™ – All rights reserved</footer>", unsafe_allow_html=True)
