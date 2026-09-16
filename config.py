"""Runtime configuration.

Copy ``.env.example`` to ``.env`` and add only the services you use.  Keeping
secrets out of this file makes it safe to share the project.
"""
import os

from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
DEFAULT_CITY = os.getenv("JARVIS_DEFAULT_CITY", "Hyderabad")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")
USER_NAME = os.getenv("JARVIS_USER_NAME", "Sathwik")
ASSISTANT_NAME = os.getenv("JARVIS_ASSISTANT_NAME", "Jarvis")
