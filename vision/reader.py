import requests
from config import OLLAMA_URL
from models import CHAT_MODEL


SYSTEM_PROMPT = """
You are Jarvis, Sathwik's personal AI assistant.

The following text was extracted from the user's screen using OCR.

Your job is to answer ONLY the user's request.

Rules:
- Don't mention OCR.
- Don't mention screenshots.
- Don't mention extracted text.
- Speak naturally.
- If the user asked to summarize, summarize.
- If they asked to explain, explain.
- If they asked to read, give the important content.
- Keep spoken responses concise.
"""


def ask_from_screen(screen_text, user_request):

    prompt = f"""
Screen Content:

{screen_text}

User Request:

{user_request}

Answer:
"""

    data = {
        "model": CHAT_MODEL,
        "system": SYSTEM_PROMPT,
        "prompt": prompt,
        "stream": False
    }

    try:

        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=data,
            timeout=300
        )

        if response.status_code == 200:
            return response.json()["response"].strip()

        return "Sorry Sathwik, I couldn't understand the screen."

    except Exception:
        return "Sorry Sathwik, my AI brain is unavailable."
