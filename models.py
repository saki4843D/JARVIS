"""Model names can be changed without editing code."""
import os

CHAT_MODEL = os.getenv("JARVIS_CHAT_MODEL", "llama3.2")
VISION_MODEL = os.getenv("JARVIS_VISION_MODEL", "gemma4:12b")
CODE_MODEL = CHAT_MODEL
PLANNER_MODEL = CHAT_MODEL
OCR_MODEL = CHAT_MODEL
