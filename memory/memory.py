import json
import os

MEMORY_FILE = "memory/memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r") as file:
        return json.load(file)



def save_memory(data):

    with open(MEMORY_FILE, "w") as file:
        json.dump(data, file, indent=4)



def remember(key, value):

    memory = load_memory()

    key = key.replace("my ", "").strip()

    memory[key] = value

    save_memory(memory)



def recall(key):

    memory = load_memory()

    key = key.replace("my ", "").strip()

    return memory.get(key, None)