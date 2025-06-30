# app/services/feedback_service.py

def save_feedback(feedback: str) -> bool:
    """
    Append user feedback to a local file for review.
    Could be expanded to store in a DB later.
    """
    try:
        with open("feedback.txt", "a", encoding="utf-8") as f:
            f.write(feedback.strip() + "\n\n")
        return True
    except Exception:
        return False
