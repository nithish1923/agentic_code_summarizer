
# 🤖 CodeWhisperer – AI-Powered Code Summarizer Assistant

**CodeWhisperer** is an intelligent Streamlit-based AI assistant that analyzes and summarizes source code using OpenAI's GPT-4o. It supports multiple programming languages, provides smart summaries, usage examples, and lets you export results in PDF, HTML, and Markdown formats.

---

## 🚀 Features

- 🧠 AI-powered code summarization using **GPT-4o**
- 📥 Accepts input via:
  - Direct code paste
  - `.zip` uploads for full codebases
- 🌐 Supports multiple languages:
  - Python
  - JavaScript
  - Java
  - C++
  - And more
- 📄 Generates summaries with:
  - Code purpose
  - Function/class descriptions
  - Parameters and return values
  - Usage notes
  - Realistic usage examples
  - Confidence score
- 📤 Export results as:
  - PDF
  - HTML
  - Markdown
- 🧩 Modular design:
  - `app.py`: UI logic (Streamlit)
  - `engine_openai.py`: AI prompt handling and summarization engine

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/codewhisperer.git
cd codewhisperer
2. Create a Virtual Environment (Recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set Your OpenAI API Key
For Local Use:
Create a file at .streamlit/secrets.toml with this content:

toml
Copy
Edit
OPENAI_API_KEY = "your-openai-key-here"
For Streamlit Cloud:
Go to Settings → Secrets, and add your API key there.

🧪 Run the App Locally
bash
Copy
Edit
streamlit run app.py
📁 Folder Structure
bash
Copy
Edit
codewhisperer/
├── app.py                  # Streamlit UI
├── engine_openai.py        # GPT logic & summarization
├── requirements.txt        # Dependencies
└── .streamlit/
    └── secrets.toml        # (Optional) Local API key
📷 Demo
(Add screenshots or a Streamlit Cloud demo link here if available)

💡 Use Cases
CodeWhisperer is ideal for:

Understanding unfamiliar or legacy codebases

Auto-generating documentation

Teaching code behavior and best practices

Saving time on manual summaries

✨ Contributions
Pull requests are welcome! For significant changes, open an issue to discuss your ideas first.

📝 License
© 2025 Nithish Kondapaka. All rights reserved.

yaml
Copy
Edit

---

Let me know if you want me to:
- Add badges (e.g. Python version, Streamlit link)
- Insert example screenshots
- Generate a logo or favicon for branding

You're good to publish this on GitHub or Streamlit Cloud now 🚀







You said:
https://agenticcodesummarizer-rtfvo2mzhnhtypuoavniju.streamlit.app/Add Streamlight link here.


ChatGPT said:
Great! Here's your updated README.md with the Streamlit Cloud live app link added in two ideal spots:

✅ Final README.md – with Live Demo Badge + Link
markdown
Copy
Edit
# 🤖 CodeWhisperer – AI-Powered Code Summarizer Assistant

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agenticcodesummarizer-rtfvo2mzhnhtypuoavniju.streamlit.app/)

**CodeWhisperer** is an intelligent Streamlit-based AI assistant that analyzes and summarizes source code using OpenAI's GPT-4o. It supports multiple programming languages, provides smart summaries, usage examples, and lets you export results in PDF, HTML, and Markdown formats.

---

## 🚀 Features

- 🧠 AI-powered code summarization using **GPT-4o**
- 📥 Accepts input via:
  - Direct code paste
  - `.zip` uploads for full codebases
- 🌐 Supports multiple languages:
  - Python
  - JavaScript
  - Java
  - C++
  - And more
- 📄 Generates summaries with:
  - Code purpose
  - Function/class descriptions
  - Parameters and return values
  - Usage notes
  - Realistic usage examples
  - Confidence score
- 📤 Export results as:
  - PDF
  - HTML
  - Markdown
- 🧩 Modular design:
  - `app.py`: UI logic (Streamlit)
  - `engine_openai.py`: AI prompt handling and summarization engine

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/codewhisperer.git
cd codewhisperer
2. Create a Virtual Environment (Recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set Your OpenAI API Key
For Local Use:
Create a file at .streamlit/secrets.toml with this content:

toml
Copy
Edit
OPENAI_API_KEY = "your-openai-key-here"
For Streamlit Cloud:
Go to Settings → Secrets, and add your API key there.

🧪 Run the App Locally
bash
Copy
Edit
streamlit run app.py
📁 Folder Structure
bash
Copy
Edit
codewhisperer/
├── app.py                  # Streamlit UI
├── engine_openai.py        # GPT logic & summarization
├── requirements.txt        # Dependencies
└── .streamlit/
    └── secrets.toml        # (Optional) Local API key
📷 Live Demo
🔗 Try it live on Streamlit Cloud:
👉 CodeWhisperer Demo

💡 Use Cases
CodeWhisperer is ideal for:

Understanding unfamiliar or legacy codebases

Auto-generating documentation

Teaching code behavior and best practices

Saving time on manual summaries

✨ Contributions
Pull requests are welcome! For significant changes, open an issue to discuss your ideas first.

📝 License
© 2025 Nithish Kondapaka. All rights reserved.
