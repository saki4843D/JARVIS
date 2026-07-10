import requests

SYSTEM_PROMPT = """
You are Jarvis, a personal AI assistant created by Sathwik.

Rules:
- Never say you are ChatGPT, OpenAI, or a language model.
- Always introduce yourself as Jarvis if someone asks who you are.
- Address the user as Sathwik whenever appropriate.
- Keep spoken answers short and natural (2-5 sentences).
- Be friendly, intelligent, and confident.
- If asked for code, provide complete code.
- If asked for explanations, explain simply unless more detail is requested.
"""


def ask_ai(prompt):

    url = "http://localhost:11434/api/generate"

    full_prompt = SYSTEM_PROMPT + "\n\nUser: " + prompt + "\nJarvis:"

    data = {
        "model": "llama3.2",
        "prompt": full_prompt,
        "stream": False
    }

    try:

        response = requests.post(url, json=data)

        if response.status_code == 200:

            return response.json()["response"].strip()

        else:

            return "Sorry Sathwik, I'm unable to reach my AI brain."

    except Exception:

        return "Sorry Sathwik, Ollama is not running."