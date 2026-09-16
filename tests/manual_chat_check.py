"""Manual local-Ollama check. Run directly; it is not part of pytest."""
from ai import ask_ai


if __name__ == "__main__":
    print(ask_ai("Reply with only: Hello"))
