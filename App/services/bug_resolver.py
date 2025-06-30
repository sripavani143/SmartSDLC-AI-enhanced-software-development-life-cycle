from app.services.watsonx_service import query_watsonx

def fix_code_bugs(buggy_code: str) -> str:
    prompt = (
        "Fix the syntax errors in this Python code. "
        "Return only the corrected code.\n\n"
        f"{buggy_code}\n"
    )

    response = query_watsonx(prompt)

    if isinstance(response, str):
        cleaned = response.strip()

        # Remove all markdown code fences
        cleaned = cleaned.replace("```python", "").replace("```", "").strip()

        # Keep only lines that start with 'def', 'class', or valid Python code
        allowed_lines = []
        for line in cleaned.splitlines():
            # If you expect one-liner expressions like "print()", adjust this filter
            if line.strip().startswith(("def ", "class ", "return", "if ", "elif ", "else", "for ", "while ", "try:", "except", "with ", "import ", "from ")):
                allowed_lines.append(line)
            elif line.strip() == "":
                allowed_lines.append(line)
            elif line.strip().startswith("@"):  # decorator
                allowed_lines.append(line)
            else:
                # Stop processing further lines if unrelated text appears
                break

        cleaned = "\n".join(allowed_lines).strip()

        # Defensive validation
        if not cleaned:
            return "# Unable to generate corrected code. Please check your input and try again."
        if "def " not in cleaned:
            return "# The model returned unrelated or invalid code. Please try again."

        return cleaned
