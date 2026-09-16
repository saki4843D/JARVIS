from commands.plugins.base import BasePlugin
from config import ASSISTANT_NAME, USER_NAME


class GreetingsPlugin(BasePlugin):

    def can_handle(self, command):

        command = command.lower()

        return (
            command == "hello"
            or command == "hi"
            or command.startswith("hi ")
            or command == "how are you"
            or "your name" in command
        )

    def handle(self, command):

        command = command.lower()

        if command == "hello" or command == "hi" or command.startswith("hi "):
            return f"Hello {USER_NAME}. How are you today?", False

        elif command == "how are you":
            return "I am doing great. Thank you for asking.", False

        elif "your name" in command:
            return f"My name is {ASSISTANT_NAME}.", False