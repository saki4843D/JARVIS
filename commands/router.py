from datetime import datetime

from commands.apps import open_app
from commands.browser import open_chrome, open_youtube, search_google
from commands.system import (
    battery,
    take_screenshot,
    lock,
    shutdown,
    restart,
)
from memory.memory import remember, recall
from ai import ask_ai


def handle(command):

    command = command.lower().strip()

    # -------------------------
    # Greetings
    # -------------------------
    if command == "hello" or command == "hi" or command.startswith("hi "):
        return "Hello Sathwik. How are you today?", False

    elif command == "how are you":
        return "I am doing great. Thank you for asking.", False

    elif "your name" in command:
        return "My name is Jarvis.", False

    # -------------------------
    # Time
    # -------------------------
    elif "time" in command:

        current_time = datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}", False

    # -------------------------
    # Open Applications
    # -------------------------
    elif command.startswith("open "):

        app = command.replace("open ", "").strip()

        if app == "chrome":
            return open_chrome(), False

        elif app == "youtube":
            return open_youtube(), False

        elif open_app(app):
            return f"Opening {app}", False

        else:
            return f"Sorry, I couldn't find {app}.", False

    # -------------------------
    # Google Search
    # -------------------------
    elif command.startswith("search "):

        query = command.replace("search", "").strip()

        return search_google(query), False

    # -------------------------
    # Battery
    # -------------------------
    elif "battery" in command:

        return battery(), False

    # -------------------------
    # Screenshot
    # -------------------------
    elif "take screenshot" in command:

        return take_screenshot(), False

    # -------------------------
    # Lock Computer
    # -------------------------
    elif "lock computer" in command:

        return lock(), False

    # -------------------------
    # Shutdown
    # -------------------------
    elif "shutdown computer" in command:

        return shutdown(), False

    # -------------------------
    # Restart
    # -------------------------
    elif "restart computer" in command:

        return restart(), False

    # -------------------------
    # Memory
    # -------------------------
    elif command.startswith("remember"):

        data = command.replace("remember", "").strip()

        if " is " in data:

            key, value = data.split(" is ", 1)

            remember(key, value)

            return f"I will remember that {key} is {value}", False

        else:

            return "Please say: Remember my favourite color is blue.", False

    elif command.startswith("what is my"):

        key = command.replace("what is my", "").strip()

        result = recall(key)

        if result:

            return f"Your {key} is {result}", False

        else:

            return "I don't remember that yet.", False

    # -------------------------
    # Exit
    # -------------------------
    elif "exit" in command or "goodbye" in command:

        return "Goodbye Sathwik.", True

    # -------------------------
    # AI
    # -------------------------
    else:

        answer = ask_ai(command)

        return answer, False