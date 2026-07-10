from datetime import datetime
import webbrowser

from commands.apps import open_app
from commands.system import (
    battery,
    take_screenshot,
    lock,
    shutdown,
    restart,
)
from memory.memory import remember, recall
from ai import ask_ai


def process_command(command, speak):

    command = command.lower().strip()

    # -----------------------------
    # Greetings
    # -----------------------------
    if command == "hello" or command == "hi" or command.startswith("hi "):
        speak("Hello Sathwik. How are you today?")

    elif command == "how are you":
        speak("I am doing great. Thank you for asking.")

    elif "your name" in command:
        speak("My name is Jarvis.")

    # -----------------------------
    # Time
    # -----------------------------
    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)

    # -----------------------------
    # Open Applications
    # -----------------------------
    elif command.startswith("open "):

        app = command.replace("open ", "").strip()

        if app == "chrome":
            speak("Opening Chrome.")
            webbrowser.open("https://www.google.com")

        elif app == "youtube":
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif open_app(app):
            speak(f"Opening {app}")

        else:
            speak(f"Sorry, I couldn't find {app}.")

    # -----------------------------
    # Google Search
    # -----------------------------
    elif command.startswith("search "):

        query = command.replace("search", "").strip()

        speak(f"Searching for {query}")

        webbrowser.open(f"https://www.google.com/search?q={query}")

    # -----------------------------
    # Battery
    # -----------------------------
    elif "battery" in command:

        speak(battery())

    # -----------------------------
    # Screenshot
    # -----------------------------
    elif "take screenshot" in command:

        speak(take_screenshot())

    # -----------------------------
    # Lock Computer
    # -----------------------------
    elif "lock computer" in command:

        speak(lock())

    # -----------------------------
    # Shutdown
    # -----------------------------
    elif "shutdown computer" in command:

        speak(shutdown())

    # -----------------------------
    # Restart
    # -----------------------------
    elif "restart computer" in command:

        speak(restart())

    # -----------------------------
    # Memory
    # -----------------------------
    elif command.startswith("remember"):

        data = command.replace("remember", "").strip()

        if " is " in data:

            key, value = data.split(" is ", 1)

            remember(key, value)

            speak(f"I will remember that {key} is {value}")

        else:

            speak("Please say it like: Remember my favourite color is blue.")

    elif command.startswith("what is my"):

        key = command.replace("what is my", "").strip()

        result = recall(key)

        if result:

            speak(f"Your {key} is {result}")

        else:

            speak("I don't remember that yet.")

    # -----------------------------
    # Exit
    # -----------------------------
    elif "exit" in command or "goodbye" in command:

        speak("Goodbye Sathwik.")
        return True

    # -----------------------------
    # AI
    # -----------------------------
    else:

        speak("Let me think.")

        answer = ask_ai(command)

        speak(answer)

    return False