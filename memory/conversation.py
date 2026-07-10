conversation_history = []

MAX_HISTORY = 10


def add_message(role, content):
    global conversation_history

    conversation_history.append({
        "role": role,
        "content": content
    })

    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)


def get_history():
    return conversation_history


def clear_history():
    global conversation_history
    conversation_history = []