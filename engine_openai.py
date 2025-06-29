import os

import openai

import markdown



openai.api_key = os.getenv("OPENAI_API_KEY")



def prompt_summary(code):

    return f"""You are an expert code reviewer. Summarize the following Python code:

1. Purpose

2. Parameters

3. Return values

4. Usage notes



python

{code}

"""



def prompt_example(code):

    return f"""Generate a realistic Python usage example for the following function or class:



python

{code}

"""



def prompt_confidence(code, summary):

    return f"""Evaluate this summary for the code and respond with a confidence score (0 to 100):



Code:

```python

{code}



Summary: {summary} """



def ask_gpt(prompt): response = openai.ChatCompletion.create( model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0 ) return response.choices[0].message.content.strip()



def generate_all_summaries(folder_path): summaries = [] for root, _, files in os.walk(folder_path): for file in files: if file.endswith(".py"): with open(os.path.join(root, file), "r", encoding="utf-8") as f: code = f.read() summary = ask_gpt(prompt_summary(code)) example = ask_gpt(prompt_example(code)) confidence = ask_gpt(prompt_confidence(code, summary)) section = f"## {file}\n\n" 

f"### Summary\n{summary}\n\n" 

f"### Usage Example\n{example}\n\n" 

f"### Confidence Score\n{confidence}/100\n\n" summaries.append(section) return summaries



def save_summary_as_html(summaries, output_path): html = markdown.markdown("".join(summaries)) with open(output_path, "w", encoding="utf-8") as f: f.write(html)



def save_summary_as_markdown(summaries, output_path): with open(output_path, "w", encoding="utf-8") as f: f.write("".join(summaries))
