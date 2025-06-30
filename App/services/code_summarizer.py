from app.services.watsonx_service import query_watsonx

def summarize_code(code_snippet: str) -> str:
    prompt = (
        "You are a helpful AI code assistant.\n"
        "Summarize the following Python code in one short, clear paragraph.\n"
        "Do not repeat the code, do not include headings or labels.\n"
        "Return exactly one paragraph.\n"
        "End with a period.\n\n"
        f"{code_snippet}\n\n"
    )

    response = query_watsonx(prompt)

    if isinstance(response, str):
        cleaned = response.strip()

        # Remove any known labels at start
        for prefix in [
            "Explanation:", "Summary:", "Answer:", "Description:", "Details:", "Output:"
        ]:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()

        # Split by double line breaks (paragraphs) and keep only the first paragraph
        first_paragraph = cleaned.split("\n\n")[0].strip()

        # Remove any trailing incomplete sentence fragments
        if first_paragraph.endswith(":") or first_paragraph.endswith(","):
            first_paragraph = first_paragraph.rstrip(":,")

        # Make sure ends with a single period
        if not first_paragraph.endswith((".", "!", "?")):
            first_paragraph += "."

        return first_paragraph

    return response
