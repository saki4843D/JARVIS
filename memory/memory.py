import json
import os
from pathlib import Path

MEMORY_FILE = Path(__file__).with_name("memory.json")


def load_memory():

    if not MEMORY_FILE.exists():
        return {}

    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}



def save_memory(data):

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = MEMORY_FILE.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    temporary.replace(MEMORY_FILE)



def remember(key, value):

    memory = load_memory()

    key = key.replace("my ", "").strip()

    memory[key.lower()] = value.strip()

    save_memory(memory)



def recall(key):

    memory = load_memory()

    key = key.replace("my ", "").strip()

    return memory.get(key.lower(), None)
