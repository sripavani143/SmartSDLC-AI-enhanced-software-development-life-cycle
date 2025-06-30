import json
from pathlib import Path

HISTORY_FILE = Path("smart_sdlc_frontend/utils/history.json")

def save_to_history(entry):
    history = load_history()
    history.append(entry)
    HISTORY_FILE.write_text(json.dumps(history, indent=2))

def load_history():
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text())
    return []

def clear_history():
    HISTORY_FILE.write_text("[]")
