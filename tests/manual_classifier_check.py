"""Manual intent-classifier check. Run directly; it is not part of pytest."""
from intent.classifier import classify


if __name__ == "__main__":
    while True:
        command = input("You: ").strip()
        if command.lower() in {"exit", "quit"}:
            break
        print(classify(command))
