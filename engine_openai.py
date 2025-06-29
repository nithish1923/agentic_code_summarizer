import openai
import os

# Ensure the OpenAI API key is available from environment variables
# The openai library automatically picks up OPENAI_API_KEY if set as an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Language-specific descriptions for prompting and file extension mapping
LANGUAGE_DESCRIPTIONS = {
    "py": "python", "js": "javascript", "ts": "typescript",
    "java": "java", "cpp": "c++", "c": "c", "cs": "c#",
    "rb": "ruby", "go": "go", "rs": "rust", "php": "php",
    "swift": "swift", "kt": "kotlin",
    "h": "c++", "hpp": "c++", "cxx": "c++" # Common C++ header/source extensions
}

def detect_language(content_or_filename: str, is_filename: bool = False) -> str:
    """
    Detects the programming language based on filename extension or code content heuristic.

    Args:
        content_or_filename (str): The code content itself (if is_filename is False)
                                   or the filename (if is_filename is True).
        is_filename (bool): A flag indicating whether the first argument is a filename.

    Returns:
        str: The detected language (e.g., "python", "javascript", "java", "c++", or "unknown").
    """
    if is_filename:
        # Detect language based on file extension
        ext = content_or_filename.split(".")[-1].lower()
        return LANGUAGE_DESCRIPTIONS.get(ext, "unknown")
    else:
        # Detect language based on common keywords in content (for pasted snippets)
        code_content_lower = content_or_filename.lower()
        if "def " in code_content_lower or "import " in code_content_lower or "print(" in code_content_lower or "elif" in code_content_lower:
            return "python"
        if "function " in code_content_lower or "console.log(" in code_content_lower or "var " in code_content_lower or "const " in code_content_lower or "let " in code_content_lower:
            return "javascript"
        if "public class " in code_content_lower or "system.out.println(" in code_content_lower or "import java." in code_content_lower:
            return "java"
        if "#include " in code_content_lower or "int main(" in code_content_lower or "cout << " in code_content_lower or "std::" in code_content_lower:
            return "c++"
        return "unknown"

def prompt_summary(code: str, language: str = "Python") -> str:
    """
    Generates a comprehensive prompt for GPT-4o to summarize code.

    Args:
        code (str): The actual code content to be summarized.
        language (str): The detected programming language (e.g., "Python", "Java").

    Returns:
        str: The formatted prompt string for the LLM.
    """
    return f"""
You are an expert code reviewer and technical writer.

Please summarize the following {language} code with the following details:

1. Purpose of the code
2. Parameters used (if any, specify for functions/methods)
3. Return values (if any, specify for functions/methods)
4. Usage notes (how to run, dependencies, typical scenarios)
5. Suggest a realistic usage example (the code itself, properly formatted with language syntax highlighting)
6. Rate the confidence level of this summary from 0 to 100 with a short justification.

Ensure the output is clearly structured and easy to read.
For the usage example, please provide a complete, runnable snippet using the specified language.

--- BEGIN CODE ---

```text
{code}
```

--- END CODE ---
"""

def ask_gpt(prompt: str) -> str:
    """
    Sends a prompt to the OpenAI GPT-4o model and returns the response.

    Args:
        prompt (str): The text prompt to send to the LLM.

    Returns:
        str: The stripped content of the LLM's response.
    """
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional code reviewer and technical writer. Provide concise and accurate summaries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3 # A slightly higher temperature for more diverse examples, but still consistent
    )
    return response.choices[0].message.content.strip()

def generate_all_summaries(source_input: str, is_pasted_code: bool = False):
    """
    Generates summaries for code, handling both single pasted snippets and files from a directory.

    Args:
        source_input (str): The code content (if is_pasted_code=True)
                            or the path to the temporary directory (if is_pasted_code=False).
        is_pasted_code (bool): True if processing a single pasted code snippet, False for a directory.

    Returns:
        list: A list of Markdown-formatted strings, where each string represents
              a comprehensive summary section for a file or snippet.
    """
    summaries_output = []

    if is_pasted_code:
        code = source_input
        file_name_display = "Pasted Code Snippet"
        language = detect_language(code, is_filename=False) # Content-based detection for pasted code

        if language == "unknown":
            summaries_output.append(
                f"## {file_name_display} (Language Unknown)\n\n"
                f"### Summary\nCould not reliably determine the programming language for this snippet. "
                f"Please ensure it's a supported language (Python, Java, JavaScript, C++) and try again.\n\n"
                f"### Confidence Score\n0/100\n\n"
            )
            return summaries_output

        try:
            prompt = prompt_summary(code, language)
            full_summary_response = ask_gpt(prompt)

            # The LLM's response now contains all required sections as requested by prompt_summary
            section = f"## {file_name_display} ({language.capitalize()})\n\n{full_summary_response}\n\n"
            summaries_output.append(section)
        except Exception as e:
            summaries_output.append(
                f"## {file_name_display} (Error)\n\n"
                f"### Summary\n⚠️ Error summarizing this snippet: {e}\n\n"
                f"### Confidence Score\n0/100\n\n"
            )

    else: # Processing a directory (from zip upload)
        temp_dir = source_input
        for root, _, files in os.walk(temp_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                language = detect_language(file_name, is_filename=True) # File-extension based detection

                if language == "unknown":
                    summaries_output.append(
                        f"## {file_name} (Unsupported File Type or Language Unknown)\n\n"
                        f"### Summary\nThis file type is not supported for summarization or language could not be determined.\n\n"
                        f"### Confidence Score\n0/100\n\n"
                    )
                    continue # Skip to the next file

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()

                    prompt = prompt_summary(code, language)
                    full_summary_response = ask_gpt(prompt)

                    # The LLM's response now contains all required sections
                    section = f"## {file_name} ({language.capitalize()})\n\n{full_summary_response}\n\n"
                    summaries_output.append(section)

                except Exception as e:
                    summaries_output.append(
                        f"## {file_name} (Error)\n\n"
                        f"### Summary\n⚠️ Error reading or summarizing this file: {e}\n\n"
                        f"### Confidence Score\n0/100\n\n"
                    )
    return summaries_output


def save_summary_as_html(summaries: list, output_path: str):
    """
    Converts a list of Markdown summaries into a single HTML file.

    Args:
        summaries (list): A list of Markdown-formatted summary strings.
        output_path (str): The file path where the HTML output will be saved.
    """
    # Join all Markdown sections and convert to HTML
    html = markdown.markdown("".join(summaries))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

def save_summary_as_markdown(summaries: list, output_path: str):
    """
    Saves a list of Markdown summaries into a single Markdown file.

    Args:
        summaries (list): A list of Markdown-formatted summary strings.
        output_path (str): The file path where the Markdown output will be saved.
    """
    # Join all Markdown sections and write to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(summaries))

