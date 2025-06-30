import json
import re
from app.services.watsonx_service import query_watsonx


def classify_sdlc_phases(text: str) -> str:
    prompt = (
        "Classify the following text into SDLC phases.\n\n"
        "The SDLC phases are:\n"
        "- Requirement\n"
        "- Design\n"
        "- Development\n"
        "- Testing\n"
        "- Deployment\n"
        "- Maintenance\n\n"
        "For each phase, list the sentences that belong there.\n\n"
        "Return the output as plain text using this format:\n\n"
        "Requirement:\n"
        "- Sentence 1\n"
        "- Sentence 2\n\n"
        "Design:\n"
        "- Sentence 3\n\n"
        "Development:\n"
        "- Sentence 4\n\n"
        "Testing:\n"
        "- Sentence 5\n\n"
        "Deployment:\n"
        "- Sentence 6\n\n"
        "Maintenance:\n"
        "- Sentence 7\n\n"
        "If any phase has no sentences, just write the phase name and leave it empty.\n\n"
        f"Text:\n{text}\n\n"
    )


    response = query_watsonx(prompt)

    return response.strip()+"."
