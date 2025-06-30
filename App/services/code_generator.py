from app.services.watsonx_service import query_watsonx
import re

def detect_language(task: str) -> str:
    languages = ["python", "java", "c++","cpp", "c", "javascript", "go", "ruby"]
    for lang in languages:
        if re.search(rf"\b{lang}\b", task.lower()):
            return lang
    return "python"

def generate_code(task_description: str) -> str:
    language = detect_language(task_description)

    # Fix common mistake where 'c program' is wrongly detected as C++
    if language == "c++" and "c program" in task_description.lower():
        language = "c"

    prompt = (
        f"Write a complete {language} program for the following task:\n\n"
        f"{task_description.strip()}\n\n"
        f"Requirements:\n"
        f"- Return only valid and complete {language} code in a single code block.\n"
        f"- Do not include comments, explanations, or test cases.\n"
        f"- If the code requires input, take input using standard input syntax.\n"
        f"- Output must be printed to the console.\n"
        f"- Only return code. Nothing else.\n"
    )

    print("📤 Sending Prompt to Watsonx:\n", prompt)  # Debug log

    response = query_watsonx(prompt)

    if not response or not isinstance(response, str):
        raise ValueError("Invalid response from Watsonx. Got empty or non-string.")

    # Auto-extract code block if wrapped in markdown-style code block
    if "```" in response:
        parts = response.split("```")
        for part in parts:
            if any(lang in part.lower() for lang in ["java", "python", "c", "cpp", "javascript"]):
                code = "\n".join(part.splitlines()[1:])  # skip language line
                return code.strip()

    return response.strip()