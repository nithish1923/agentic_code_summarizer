import os
from openai import OpenAI
import markdown

# Assume the provided code is saved as code_summarizer.py
# and the functions are imported or available in the same scope.

# For demonstration, let's create a dummy Python file
# In a real scenario, you would point to a folder with your actual Python code.
dummy_code_dir = "temp_code_to_summarize"
os.makedirs(dummy_code_dir, exist_ok=True)

with open(os.path.join(dummy_code_dir, "my_utility.py"), "w", encoding="utf-8") as f:
    f.write("""
def factorial(n):
    \"\"\"Calculates the factorial of a non-negative integer.\"\"\"
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

def is_prime(num):
    \"\"\"Checks if a number is prime.\"\"\"
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
""")

# IMPORTANT: Replace with your actual OpenAI API key (or set as environment variable)
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# For a runnable example in this context, we will simulate the ask_gpt function
# In a real run, uncomment the above line and ensure API_KEY is set.

# Dummy implementation for demonstration purposes,
# as actual API calls cannot be made in this sandbox.
def ask_gpt_mock(prompt):
    if "Summarize the following Python code" in prompt:
        return """Purpose: This code defines two functions: `factorial` to compute factorials and `is_prime` to check for primality.
Parameters: `factorial` takes an integer `n`; `is_prime` takes an integer `num`.
Return values: `factorial` returns an integer; `is_prime` returns a boolean.
Usage notes: Both functions handle basic cases and are suitable for mathematical operations."""
    elif "Generate a realistic Python usage example" in prompt:
        return """print(factorial(5)) # Output: 120
print(is_prime(7))  # Output: True
print(is_prime(10)) # Output: False"""
    elif "confidence score" in prompt:
        return "95"
    return "Mock response"

# Override the actual ask_gpt with the mock for demonstration
# In a real scenario, you would use the actual ask_gpt provided in your code.
def ask_gpt(prompt):
    return ask_gpt_mock(prompt)

# Use the functions from the provided script
try:
    # Ensure client is initialized if running outside this mock
    # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    all_summaries = generate_all_summaries(dummy_code_dir)

    # Save as Markdown
    markdown_output_path = "code_summaries.md"
    save_summary_as_markdown(all_summaries, markdown_output_path)
    print(f"Summaries saved to {markdown_output_path}")

    # Save as HTML
    html_output_path = "code_summaries.html"
    save_summary_as_html(all_summaries, html_output_path)
    print(f"Summaries saved to {html_output_path}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Clean up dummy directory and file
    if os.path.exists(os.path.join(dummy_code_dir, "my_utility.py")):
        os.remove(os.path.join(dummy_code_dir, "my_utility.py"))
    if os.path.exists(dummy_code_dir):
        os.rmdir(dummy_code_dir)
