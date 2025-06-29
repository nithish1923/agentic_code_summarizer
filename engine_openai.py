import os
import openai

# Initialize OpenAI client (compatible with openai>=1.0.0)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Language detection
def detect_language(code: str, filename: str) -> str:
    if filename.endswith(".py"):
        return "Python"
    elif filename.endswith(".js"):
        return "JavaScript"
    elif filename.endswith(".java"):
        return "Java"
    elif filename.endswith(".cpp"):
        return "C++"
    return "Unknown"

# Prompt generator
def generate_prompt(code: str, language: str) -> str:
    base = f"You are an expert code reviewer. Summarize the following {language} code with:\n" \
           "- Purpose of the module/file\n" \
           "- Key functions/classes with parameters and return values\n" \
           "- Usage notes or examples\n" \
           "- Confidence score (0-100%)\n\nCode:\n{language.lower()}\n{code}\n"

    return base

# Ask GPT
def ask_gpt(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content

# Core summarization engine
def generate_all_summaries(input_data, from_text=False):
    summaries = []

    if from_text:
        lang = detect_language(input_data, "snippet.py")
        prompt = generate_prompt(input_data, lang)
        summary = ask_gpt(prompt)
        summaries.append(f"### 🧠 {lang} Code Summary\n\n{summary}")
    else:
        for root, _, files in os.walk(input_data):
            for file in files:
                if file.endswith((".py", ".js", ".java", ".cpp")):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()
                    lang = detect_language(code, file)
                    prompt = generate_prompt(code, lang)
                    summary = ask_gpt(prompt)
                    summaries.append(f"### 🧠 {file} ({lang})\n\n{summary}")
    return summaries

# Save as HTML
def save_summary_as_html(summaries, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("<html><body>")
        for s in summaries:
            f.write(f"<div>{s}</div><hr>")
        f.write("</body></html>")

# Save as Markdown
def save_summary_as_markdown(summaries, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        for s in summaries:
            f.write(f"{s}\n\n---\n")
