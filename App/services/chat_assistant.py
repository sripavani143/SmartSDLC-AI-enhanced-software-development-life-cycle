from app.services.watsonx_service import query_watsonx

def chat_with_assistant(message: str) -> str:
    prompt = (
        "You are a concise AI assistant for developers. "
        "Answer the question below in a single paragraph. "
        "Do NOT include any conversation history, extra instructions, or additional examples. "
        "ONLY provide the direct answer, and end with a period.\n\n"
        f"Question:\n{message}\n\n"
        "Answer:"
    )

    response = query_watsonx(prompt)

    # Clean up: remove any trailing newlines or extra space
    if isinstance(response, str):
        cleaned = response.strip()

        # If the answer does not end with a period, add it
        if not cleaned.endswith("."):
            cleaned += "."

        return cleaned

    return response
