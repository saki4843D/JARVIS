import random

from brain import process_command
from speak import speak
from listen import listen


WAKE_WORDS = [
    "jarvis",
    "hey jarvis",
    "hi jarvis",
    "hello jarvis",
    "okay jarvis",
    "ok jarvis",
]

WAKE_RESPONSES = [
    "Yes Sathwik?",
    "I'm listening.",
    "How can I help?",
    "At your service.",
    "Ready.",
    "Go ahead.",
    "What can I do for you?",
]


def main():

    speak("Hello Sathwik. I am Jarvis.")
    speak("Say Hey Jarvis to wake me.")

    while True:

        print("\nWaiting for wake word...")

        wake = listen()

        if wake == "":
            continue

        wake = wake.lower().strip()

        if not any(word in wake for word in WAKE_WORDS):
            continue

        speak(random.choice(WAKE_RESPONSES))

        # Conversation Mode
        while True:

            print("Listening for command...")

            command = listen()

            if command == "":
                continue

            command = command.lower().strip()

            # If user says wake word again, just acknowledge it
            if any(word in command for word in WAKE_WORDS):
                speak(random.choice(WAKE_RESPONSES))
                continue

            # Put Jarvis back to sleep
            if command in [
                "sleep",
                "go to sleep",
                "stop listening",
                "sleep jarvis",
            ]:
                speak("Going back to sleep.")
                break

            # Exit Jarvis completely
            if command in [
                "exit",
                "goodbye",
                "quit",
                "close jarvis",
            ]:
                speak("Goodbye Sathwik.")
                return

            should_exit = process_command(command, speak)

            if should_exit:
                return

            speak("Anything else?")


if __name__ == "__main__":
    main()