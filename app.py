
import streamlit as st
import zipfile
import tempfile
import os
from code_summary_engine import generate_summaries, save_summary_as_html, save_summary_as_markdown

st.set_page_config(page_title="Agentic Code Summarizer", layout="centered")

# Custom Styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.5em;
    }
    footer {
        text-align: center;
        font-size: 0.9em;
        color: #777;
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("📘 Agentic GenAI – Code Summary Assistant")
st.markdown("Generate AI-powered summaries, usage examples, and review scores for your Python codebase.")

st.markdown("---")

uploaded_file = st.file_uploader("📦 Upload your codebase (.zip containing .py files):", type=["zip"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, uploaded_file.name)
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        st.info("⏳ Analyzing uploaded code... This may take a few seconds.")
        summaries = generate_summaries(temp_dir)

        st.success("✅ Summary generation complete! Browse below:")

        for section in summaries:
            st.markdown(section, unsafe_allow_html=True)

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Export as HTML"):
                output_path = os.path.join(temp_dir, "summary_output.html")
                save_summary_as_html(summaries, output_path)
                with open(output_path, "rb") as f:
                    st.download_button("Download HTML", f, file_name="code_summary.html", mime="text/html")

        with col2:
            if st.button("📝 Export as Markdown"):
                md_path = os.path.join(temp_dir, "summary_output.md")
                save_summary_as_markdown(summaries, md_path)
                with open(md_path, "rb") as f:
                    st.download_button("Download Markdown", f, file_name="code_summary.md", mime="text/markdown")

        st.markdown("""
        <footer>
            ⓒ 2025 Nithish Kondapaka™ – All rights reserved
        </footer>
        """, unsafe_allow_html=True)
