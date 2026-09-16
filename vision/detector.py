VISION_KEYWORDS = [
    "what is on my screen", "what's on my screen", "read my screen",
    "look at my screen", "inspect my screen", "describe my screen",
    "show me the desktop", "show me desktop", "what is on my desktop",
    "what's on my desktop", "tell me what is there on it",
    "tell me what's there on it",
    "read this document", "read this pdf", "extract text from my screen",
    "read the text on my screen", "analyze this code", "analyze this webpage",
    "summarize this page", "what is in this image", "describe this image",
    "analyze this chart", "read this chart", "what does this error mean on screen",
]


def needs_vision(command: str) -> bool:

    command = command.lower()

    return any(keyword in command for keyword in VISION_KEYWORDS)