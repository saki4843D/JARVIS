import requests
from config import ASSISTANT_NAME, OLLAMA_URL, USER_NAME
from memory.conversation import get_history
from models import CHAT_MODEL

SYSTEM_PROMPT = """
You are {ASSISTANT_NAME}, a capable personal AI assistant for {USER_NAME}.

Rules:
- Never say you are ChatGPT, OpenAI, or a language model.
- Always introduce yourself as {ASSISTANT_NAME} if someone asks who you are.
- Address the user as {USER_NAME} whenever appropriate.
- Keep spoken answers short and natural (2-5 sentences).
- Be friendly, intelligent, and confident.
- If asked for code, provide complete code.
- If asked for explanations, explain simply unless more detail is requested.
""".format(ASSISTANT_NAME=ASSISTANT_NAME, USER_NAME=USER_NAME)


def ask_ai(prompt, history=None):
    """Ask the local Ollama model, preserving a short conversational context."""
    url = f"{OLLAMA_URL}/api/chat"
    history = history if history is not None else get_history()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history[-8:])
    # ``brain.process_command`` records the user message before routing it.
    # Avoid sending that same message twice while still supporting direct calls.
    if not history or history[-1] != {"role": "user", "content": prompt}:
        messages.append({"role": "user", "content": prompt})

    data = {
        "model": CHAT_MODEL,
        "messages": messages,
        "stream": False
    }

    try:

        response = requests.post(url, json=data, timeout=90)

        if response.status_code == 200:

            return response.json()["message"]["content"].strip()

        else:

            return f"Sorry {USER_NAME}, my local AI service returned an error."

    except requests.exceptions.ConnectionError:
        return f"Sorry {USER_NAME}, Ollama is not running. Start it, then try again."
    except requests.exceptions.Timeout:
        return f"Sorry {USER_NAME}, my local AI took too long to answer."
    except (KeyError, ValueError, requests.RequestException):
        return f"Sorry {USER_NAME}, I couldn't reach my AI brain."
