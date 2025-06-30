from app.services.watsonx_service import query_watsonx

def generate_test_cases(code_or_requirement: str) -> str:
    prompt = (
        "You are an expert test engineer. Write detailed UNIT TEST CASES ONLY for the following code or requirement.\n"
        "If it's a Python function, use unittest or pytest.\n"
        "DO NOT return the original function. Just return the test code.\n"
        "Return ONLY test code and explanation. DO NOT return the function itself.\n"
        "Wrap the code in triple backticks. Optionally include explanation after the code.\n\n"
        "You are a software testing expert.\n"
        "Given the following code or requirement, write only the unit test cases.\n"
        "Prefer `unittest` for Python or appropriate testing framework for other languages.\n\n"
        "DO NOT repeat the original function.\n"
        "DO NOT add explanations before the code.\n"
        "Wrap code in ```python ... ```\n"
        "Add explanation (optional) only after the code block.\n\n"
        f"{code_or_requirement}\n\n"
    )
    return query_watsonx(prompt)
