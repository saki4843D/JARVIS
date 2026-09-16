"""Ollama vision integration for JARVIS."""

import base64
import time
import requests

from config import OLLAMA_URL
from models import VISION_MODEL


def analyze_image(image_path, prompt):
    """Analyze a screenshot using the local Ollama vision model."""

    print("\n========== OLLAMA VISION ==========")
    print(f"Model : {VISION_MODEL}")
    print(f"Image : {image_path}")

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        if not image_bytes:
            return "Vision Error: The screenshot is empty."

        image = base64.b64encode(image_bytes).decode("utf-8")

        print(f"Image size : {len(image_bytes) / 1024:.1f} KB")
        print("Image encoded successfully.")

    except FileNotFoundError:
        return f"Vision Error: Image not found: {image_path}"

    except OSError as exc:
        return f"Vision Error: Could not read image: {exc}"

    # Keep the vision prompt focused so Gemma does not waste
    # time generating an unnecessarily long response.
    vision_prompt = f"""
You are JARVIS, a laptop screen-analysis assistant.

Analyze the supplied screenshot.

User request:
{prompt}

Give a concise, factual answer.
Describe only what is actually visible.
Do not ask follow-up questions unless absolutely necessary.
Keep the answer under 80 words.
"""

    payload = {
        "model": VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": vision_prompt,
                "images": [image],
            }
        ],
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 120,
        },
    }

    url = f"{OLLAMA_URL}/api/chat"

    print(f"Ollama URL : {url}")
    print("Sending vision request...")

    try:
        start = time.time()

        response = requests.post(
            url,
            json=payload,
            timeout=180,
        )

        elapsed = time.time() - start

        print(f"Response time : {elapsed:.2f} sec")
        print(f"Status code   : {response.status_code}")

        if response.status_code != 200:
            print("\n========== OLLAMA ERROR ==========")
            print(response.text)
            print("==================================\n")

            try:
                data = response.json()
                error = data.get("error")

                if error:
                    return f"Vision Error: {error}"

            except ValueError:
                pass

            return f"Vision Error: Ollama returned HTTP {response.status_code}."

        try:
            data = response.json()
        except ValueError:
            return "Vision Error: Ollama returned invalid JSON."

        message = data.get("message", {})

        if not isinstance(message, dict):
            return "Vision Error: Invalid Ollama response."

        content = message.get("content", "").strip()

        if not content:
            return "Vision Error: Vision model returned an empty response."

        print("Vision completed successfully.")
        print(f"Vision answer: {content}")
        print("==================================\n")

        return content

    except requests.exceptions.Timeout:
        return "Vision Error: Vision analysis timed out."

    except requests.exceptions.ConnectionError:
        return (
            "Vision Error: Cannot connect to Ollama. "
            "Make sure Ollama is running."
        )

    except requests.exceptions.RequestException as exc:
        return f"Vision Error: {exc}"

    except Exception as exc:
        return f"Vision Error: {exc}"