# 🧠 CodeSummarAI – Agentic Code Summarizer Assistant

An intelligent Streamlit-based AI assistant that analyzes and summarizes source code using OpenAI's GPT-4o. Supports multi-language code inputs, smart summaries, usage examples, and exportable outputs in PDF, HTML, and Markdown.

---

## 🚀 Features

- 🧠 AI-powered code summarization using GPT-4o
- 📥 Accepts code via direct paste or `.zip` uploads
- 🌐 Supports multiple languages: Python, JavaScript, Java, C++, etc.
- 📄 Generates summaries with:
  - Purpose of the code
  - Parameters
  - Return values
  - Usage notes
  - Realistic usage example
  - Confidence score
- 📤 Export summaries as:
  - PDF
  - HTML
  - Markdown
- 🎯 Built with modular components (`app.py` for UI, `engine_openai.py` for logic)

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/code-summarai.git
cd code-summarai
2. Create a virtual environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set your OpenAI API key
For local dev, create a .streamlit/secrets.toml file:

toml
Copy
Edit
OPENAI_API_KEY = "your-openai-key-here"
For Streamlit Cloud, add this key in Settings → Secrets.

🧪 Run the app locally
bash
Copy
Edit
streamlit run app.py
📁 Folder Structure
graphql
Copy
Edit
code-summarai/
├── app.py                  # Streamlit UI
├── engine_openai.py        # GPT prompt logic & file processing
├── requirements.txt        # Python dependencies
└── .streamlit/
    └── secrets.toml        # (Optional) API key for local testing
📷 Demo


💡 Use Case
This project demonstrates the capability of Agentic Gen AI to automate code understanding and generate comprehensive, consistent summaries — ideal for teams handling unfamiliar or legacy codebases.

✨ Contributions
Pull requests welcome! For major changes, please open an issue first.

📝 License
© 2025 Nithish Kondapaka. All rights reserved.

