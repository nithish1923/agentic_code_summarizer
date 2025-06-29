import openai
import os

# Ensure the OpenAI API key is available
openai.api_key = os.getenv("OPENAI_API_KEY")

# Language-specific descriptions for prompting
LANGUAGE_DESCRIPTIONS = {
    "python": "Python",
    "py": "Python",
    "js": "JavaScript",
    "ts": "TypeScript",
    "java": "Java",
    "cpp": "C++",
    "c": "C",
    "cs": "C#",
    "rb": "Ruby",
    "go": "Go",
    "rs": "Rust",
    "php": "PHP",
    "swift": "Swift",
    "kt": "Kotlin"
}

def detect_language(file_name: str) -> str:
    ext = file_name.split(".")[-1].lower()
    return LANGUAGE_DESCRIPTIONS.get(ext, "Unknown")

def prompt_summary(code: str, language: str = "Python") -> str:
    return f"""
You are an expert code reviewer and technical writer.

Please summarize the following {language} code with the following details:

1. Purpose of the code  
2. Parameters used  
3. Return values (if any)  
4. Usage notes  
5. Suggest a realistic usage example  
6. Rate the confidence level of this summary from 0 to 100 with a short justification.

--- BEGIN CODE ---

{code}

--- END CODE ---
"""

def ask_gpt(prompt: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional code reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def generate_all_summaries(temp_dir: str):
    summaries = []
    for root, _, files in os.walk(temp_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            ext = os.path.splitext(file_name)[1].lower()
            if ext not in LANGUAGE_DESCRIPTIONS:
                continue  # skip non-code files
            try:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        code = f.read()

                language = detect_language(file_name)
                prompt = prompt_summary(code, language)
                summary = ask_gpt(prompt)

                summaries.append((file_name, language, summary))
            except Exception as e:
                summaries.append((file_name, "Unknown", f"⚠️ Error reading or summarizing this file: {e}"))
    return summaries

def save_summary_as_html(summaries, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("<html><body>")
        for file_name, language, summary in summaries:
            f.write(f"<h2>{file_name} ({language})</h2><p>{summary}</p><hr>")
        f.write("</body></html>")

def save_summary_as_markdown(summaries, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for file_name, language, summary in summaries:
            f.write(f"### {file_name} ({language})\n\n{summary}\n\n---\n")
