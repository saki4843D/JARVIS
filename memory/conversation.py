import json
from pathlib import Path


HISTORY_FILE = Path(__file__).with_name("conversation.json")
conversation_history = []

MAX_HISTORY = 10


def _load_history():
    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


conversation_history = _load_history()[-MAX_HISTORY:]


def _save_history():
    temporary = HISTORY_FILE.with_suffix(".tmp")
    try:
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(conversation_history[-MAX_HISTORY:], file, indent=2)
        temporary.replace(HISTORY_FILE)
    except OSError:
        pass


def add_message(role, content):
    global conversation_history

    conversation_history.append({
        "role": role,
        "content": content
    })

    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)
    _save_history()


def get_history():
    return conversation_history


def clear_history():
    global conversation_history
    conversation_history = []
    _save_history()