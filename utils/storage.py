import json
import os
from datetime import datetime

# Create reports folder automatically if it doesn't exist
os.makedirs("reports", exist_ok=True)

HISTORY_PATH = "reports/history.json"


def save_session(data):
    data["timestamp"] = str(datetime.now())

    # Load existing history safely
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, "r") as f:
                history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            history = []
    else:
        history = []

    history.append(data)

    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=4)

    return HISTORY_PATH


def load_history():
    if not os.path.exists(HISTORY_PATH):
        return []

    try:
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []