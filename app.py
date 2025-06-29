# streamlit_app.py

import streamlit as st
import zipfile
import tempfile
import os
from io import BytesIO
# Import functions from our custom engines
from engine_openai import generate_all_summaries, save_summary_as_html, save_summary_as_markdown
from language_prompt_engine import detect_language # Only need detect_language here, generate_prompt_for_type is used internally by engine_openai
from markdown2 import markdown # Used for converting markdown to HTML for PDF generation
from xhtml2pdf import pisa # Used for converting HTML to PDF

# Set Streamlit page configuration for title and wide layout
st.set_page_config(page_title="Agentic Code Summary Assistant", layout="wide")

# Title of the application, centered with an emoji for visual appeal
st.markdown("""
<h1 style='text-align:center;'>🧠 Agentic Code Summary Assistant</h1>
""", unsafe_allow_html=True)

# Create two columns for layout: explanations on the left, inputs on the right
left, right = st.columns([2, 3])

# LEFT SIDE: Explanations about the tool
with left:
    st.markdown("### 📘 What is Agentic Code Summary Assistant")
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

# RIGHT SIDE: Input options (paste code or upload files)
with right:
    st.markdown("#### 📥 Paste your code here")
    # Text area for pasting code snippets. Placeholder guides the user.
    pasted_code = st.text_area("", height=200, placeholder="Paste any supported code snippet here (Python, Java, JS, C++)")

    st.markdown("#### 📁 Or upload files")
    # File uploader for zip archives. Specifies accepted types.
    uploaded_file = st.file_uploader("Upload .zip file with .py, .js, .java, or .cpp files", type=["zip"])

    # Initialize summaries list. This will hold the generated summaries.
    summaries = []

    # Logic for processing pasted code when a file is NOT uploaded
    if pasted_code and not uploaded_file:
        with st.spinner("Processing pasted code..."):
            # Call generate_all_summaries with the pasted code and flag for single snippet
            summaries = generate_all_summaries(pasted_code, is_single_snippet=True)
            for section in summaries:
                # Display each generated summary section directly in Markdown format
                st.markdown(section, unsafe_allow_html=True)

    # Logic for processing uploaded zip file when code is NOT pasted
    elif uploaded_file:
        # Use a temporary directory to handle zip extraction and processing
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, uploaded_file.name)
            # Write the uploaded file's buffer to the temporary zip file
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract all contents of the zip file into the temporary directory
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            with st.spinner("Processing uploaded zip..."):
                # Call generate_all_summaries with the temporary directory path
                summaries = generate_all_summaries(temp_dir)
                for section in summaries:
                    # Display each generated summary section directly in Markdown format
                    st.markdown(section, unsafe_allow_html=True)

# Export options, displayed only if any summaries have been generated (either by pasting or uploading)
if (pasted_code or uploaded_file) and summaries:
    st.markdown("#### 📤 Export Summary")
    # Create three columns for download buttons (HTML, Markdown, PDF)
    c1, c2, c3 = st.columns(3)

    # All export operations should happen within a single temporary directory
    # to ensure paths are valid for download buttons and cleanup
    with tempfile.TemporaryDirectory() as export_temp_dir:
        # HTML Export Button
        with c1:
            html_path = os.path.join(export_temp_dir, "code_summary.html")
            # Save the summaries as an HTML file using the imported function
            save_summary_as_html(summaries, html_path)
            # Provide a download button for the generated HTML file
            with open(html_path, "rb") as f:
                st.download_button("💾 HTML", f, file_name="code_summary.html", mime="text/html")

        # Markdown Export Button
        with c2:
            md_path = os.path.join(export_temp_dir, "code_summary.md")
            # Save the summaries as a Markdown file using the imported function
            save_summary_as_markdown(summaries, md_path)
            # Provide a download button for the generated Markdown file
            with open(md_path, "rb") as f:
                st.download_button("📝 Markdown", f, file_name="code_summary.md", mime="text/markdown")

        # PDF Export Button
        with c3:
            # Convert the list of Markdown summaries to a single HTML string for PDF conversion
            html_string = markdown("".join(summaries))
            pdf_file = BytesIO() # Create an in-memory binary stream to store the PDF content
            # Use xhtml2pdf to create the PDF from the HTML string
            pisa_status = pisa.CreatePDF(src=html_string, dest=pdf_file)
            
            # Check if PDF generation was successful
            if not pisa_status.err:
                pdf_file.seek(0) # Rewind buffer to the beginning before offering for download
                # Provide a download button for the generated PDF file
                st.download_button("📄 PDF", pdf_file, file_name="code_summary.pdf", mime="application/pdf")
            else:
                # Display an error message if PDF generation fails
                st.error("❌ PDF generation failed.")

# Footer of the application with copyright information
st.markdown("""
<hr style='margin-top:20px;'>
<div style='text-align:center; font-size:0.85em; color:gray;'>ⓒ 2025 Nithish Kondapaka™ – All rights reserved</div>
""", unsafe_allow_html=True)
