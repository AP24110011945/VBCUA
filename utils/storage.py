import json
import os
from datetime import datetime

HISTORY_PATH = "reports/history.json"


def save_session(data):
    data["timestamp"] = str(datetime.now())

    # if file exists, load old history
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r") as f:
            try:
                history = json.load(f)
            except:
                history = []
    else:
        history = []

    # append new session
    history.append(data)

    # save back
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=4)

    return HISTORY_PATH


def load_history():
    if not os.path.exists(HISTORY_PATH):
        return []
    
    with open(HISTORY_PATH, "r") as f:
        return json.load(f)