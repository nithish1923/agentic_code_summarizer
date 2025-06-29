
import os
import markdown
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Define prompts for summary, usage example, and confidence review
summary_prompt = """
You are an expert software assistant. Given the following code block, generate a detailed summary including:
1. Purpose of the function/class/module.
2. Input parameters and their types.
3. Return values.
4. Any usage notes.

Code:
```python
{code}
```
"""

example_prompt = """
You are an expert software assistant. Given the following Python function or class, generate a usage example showing how to call it with realistic data.

Code:
```python
{code}
```
"""

confidence_prompt = """
You are a software review agent. Given the following summary and code, provide a confidence score (0-100) indicating how accurate and complete the summary is. Just respond with a number.

Code:
```python
{code}
```

Summary:
{summary}
"""

# Initialize chains
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

summary_chain = LLMChain(
    llm=llm, prompt=PromptTemplate(input_variables=["code"], template=summary_prompt)
)

example_chain = LLMChain(
    llm=llm, prompt=PromptTemplate(input_variables=["code"], template=example_prompt)
)

confidence_chain = LLMChain(
    llm=llm, prompt=PromptTemplate(input_variables=["code", "summary"], template=confidence_prompt)
)

def generate_summaries(folder_path):
    summaries = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()
                    summary = summary_chain.run(code=code)
                    example = example_chain.run(code=code)
                    confidence = confidence_chain.run(code=code, summary=summary)

                    section = f"## {file}\n\n" \
                              f"### Summary\n{summary}\n\n" \
                              f"### Usage Example\n{example}\n\n" \
                              f"### Confidence Score\n{confidence}/100\n\n"
                    summaries.append(section)
    return summaries

def save_summary_as_html(summaries, output_path):
    html_output = markdown.markdown("".join(summaries))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

def save_summary_as_markdown(summaries, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(summaries))
