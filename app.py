import streamlit as st
import zipfile
import tempfile
import os
from io import BytesIO
# Assuming engine_openai.py exists in the same directory or is importable
# It should contain generate_all_summaries, save_summary_as_html, save_summary_as_markdown
from engine_openai import generate_all_summaries, save_summary_as_html, save_summary_as_markdown
from markdown2 import markdown
from xhtml2pdf import pisa

# Set Streamlit page configuration for a wide layout and title
st.set_page_config(page_title="Agentic GenAI – Code Summary Assistant", layout="wide")

# Header with a central alignment and emoji for visual appeal
st.markdown("""
<h1 style='text-align:center;'>🧠 Agentic GenAI – Code Summary Assistant</h1>
""", unsafe_allow_html=True)

# Create a two-column layout for file upload and introductory text
left_col, right_col = st.columns([1, 2])

# Left column for file upload
with left_col:
    # File uploader widget, accepting only .zip files
    uploaded_file = st.file_uploader("📥 Upload .zip of Python files", type=["zip"])

# Right column for "About" and "How it Works" sections
with right_col:
    # Markdown for About and How it Works sections, styled with HTML for better presentation
    st.markdown("""
    <div style='padding: 10px 20px; background-color: #f9f9f9; border-radius: 10px;'>
        <h4>📘 About the Assistant</h4>
        <ul style='margin-top:-10px;'>
            <li>Generates smart, human-readable summaries from your Python code using GPT-4o</li>
            <li>Includes function descriptions, usage examples, and self-evaluated confidence</li>
        </ul>

        <h4 style='margin-top:20px;'>⚙️ How It Works</h4>
        <ol style='margin-top:-10px;'>
            <li>Upload a <code>.zip</code> containing your <code>.py</code> files</li>
            <li>AI reads and summarizes each module, class, and function</li>
            <li>View results and export as HTML / Markdown / PDF</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Logic to process the uploaded file once it's available
if uploaded_file:
    # Use a temporary directory to extract and process the zip file contents
    with tempfile.TemporaryDirectory() as temp_dir:
        # Construct the full path for the uploaded zip file within the temporary directory
        zip_path = os.path.join(temp_dir, uploaded_file.name)
        # Write the uploaded file's buffer to the temporary zip file
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract all contents of the zip file into the temporary directory
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Display success message after file upload and extraction
        st.success("✅ Code uploaded and processing...")
        
        # Generate summaries using the imported function from engine_openai
        # This function will iterate through Python files in temp_dir and call the OpenAI API
        summaries = generate_all_summaries(temp_dir)
        
        # Inform the user that summaries have been generated
        st.info("✅ Summaries generated below")

        # Display each generated summary section in the Streamlit app
        for section in summaries:
            st.markdown(section, unsafe_allow_html=True)

        # Section for exporting the generated summaries
        st.markdown("#### 📤 Export Summary")
        
        # Create three columns for download buttons (HTML, Markdown, PDF)
        export1, export2, export3 = st.columns(3)

        # HTML Export Button
        with export1:
            # Define the path for the HTML output file
            html_path = os.path.join(temp_dir, "summary_output.html")
            # Save the summaries as an HTML file using the imported function
            save_summary_as_html(summaries, html_path)
            # Provide a download button for the generated HTML file
            with open(html_path, "rb") as f:
                st.download_button("💾 HTML", f, file_name="code_summary.html", mime="text/html")

        # Markdown Export Button
        with export2:
            # Define the path for the Markdown output file
            md_path = os.path.join(temp_dir, "summary_output.md")
            # Save the summaries as a Markdown file using the imported function
            save_summary_as_markdown(summaries, md_path)
            # Provide a download button for the generated Markdown file
            with open(md_path, "rb") as f:
                st.download_button("📝 Markdown", f, file_name="code_summary.md", mime="text/markdown")

        # PDF Export Button
        with export3:
            # Convert the list of Markdown summaries to a single HTML string for PDF conversion
            html_string = markdown("".join(summaries))
            # Create an in-memory binary stream to store the PDF content
            pdf_file = BytesIO()
            # Use xhtml2pdf to create the PDF from the HTML string
            pisa_status = pisa.CreatePDF(src=html_string, dest=pdf_file)
            
            # Check if PDF generation was successful
            if not pisa_status.err:
                # Seek to the beginning of the BytesIO object before offering it for download
                pdf_file.seek(0)
                # Provide a download button for the generated PDF file
                st.download_button("📄 PDF", pdf_file, file_name="code_summary.pdf", mime="application/pdf")
            else:
                # Display an error message if PDF generation fails
                st.error("❌ PDF generation failed.")

# Footer section with copyright information
st.markdown("""
<hr style='margin-top:20px;'>
<div style='text-align:center; font-size:0.85em; color:gray;'>ⓒ 2025 Nithish Kondapaka™ – All rights reserved</div>
""", unsafe_allow_html=True)
