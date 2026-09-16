"""Text-only JARVIS console for development and systems without a microphone."""
from brain import process_command
from config import ASSISTANT_NAME, USER_NAME


def print_response(response: str) -> None:
    print(f"{ASSISTANT_NAME}: {response}")


def main() -> None:
    print(f"{ASSISTANT_NAME} online for {USER_NAME}. Type 'help' for examples, 'exit' to leave.")
    while True:
        try:
            command = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{ASSISTANT_NAME}: Goodbye.")
            return
        if not command:
            continue
        if process_command(command, print_response):
            return


if __name__ == "__main__":
    main()
