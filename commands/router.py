"""Intent routing for JARVIS.

Deterministic desktop actions live here. General questions fall back to the
local model, so an AI response can never directly operate the computer.
"""
from datetime import datetime
import re

from ai import ask_ai
from commands.apps import open_app
from commands.browser import open_chrome, open_youtube, search_google
from commands.desktop import handle as desktop_handle
from commands.files import delete_path, handle as file_handle
from commands.plugin_manager import handle as plugin_handle
from commands.system import battery, cancel_shutdown, lock, restart, shutdown, system_status, take_screenshot
from commands.weather import get_weather
from config import ASSISTANT_NAME, USER_NAME
from memory.memory import recall, remember
from vision.detector import needs_vision

_pending_power_action = None
_pending_file_delete = None

HELP_TEXT = (
    "I can open apps and websites, search the web, manage files, tell time, weather, and battery, "
    "remember preferences, inspect your screen, and answer questions locally. "
    "I can also report system status and respond to typed commands. "
    "Try: open notepad, system status, remember my favorite color is blue, "
    "or what is on my screen. Say list files to inspect the current folder."
)


def _normalise(command: str) -> str:
    return " ".join(command.lower().strip().split())


def _confirm_power_action(command: str):
    global _pending_power_action
    if _pending_power_action is None:
        return None
    if command in {"yes", "confirm", "do it", "proceed"}:
        action, _pending_power_action = _pending_power_action, None
        return (shutdown() if action == "shutdown" else restart()), False
    if command in {"no", "cancel", "never mind", "stop"}:
        _pending_power_action = None
        return "Cancelled. Your computer will stay on.", False
    return "Please say yes to confirm, or cancel to keep your computer on.", False


def _confirm_file_delete(command: str):
    global _pending_file_delete
    if _pending_file_delete is None:
        return None
    if command in {"yes", "confirm", "do it", "proceed"}:
        path, _pending_file_delete = _pending_file_delete, None
        return delete_path(path), False
    if command in {"no", "cancel", "never mind", "stop"}:
        _pending_file_delete = None
        return "Cancelled. The file was not deleted.", False
    return "Please say yes to confirm deletion, or cancel to keep the file.", False


def handle(command: str):
    """Return ``(spoken_response, should_exit)`` for a user command."""
    global _pending_power_action, _pending_file_delete
    command = _normalise(command)
    if not command:
        return "I didn't catch that. Please try again.", False

    confirmation = _confirm_power_action(command)
    if confirmation is not None:
        return confirmation
    confirmation = _confirm_file_delete(command)
    if confirmation is not None:
        return confirmation

    if " and " in command and not command.startswith(("remember ", "what is ", "what's ")):
        steps = [part.strip() for part in command.split(" and ") if part.strip()]
        if 1 < len(steps) <= 3:
            results = []
            for step in steps:
                response, should_exit = handle(step)
                results.append(response)
                if should_exit:
                    return " ".join(results), True
            return " ".join(results), False

    result = plugin_handle(command)
    if result is not None:
        return result

    if command in {"help", "what can you do", "capabilities"}:
        return HELP_TEXT, False
    if command in {"status", "system status", "are you online", "diagnostics"}:
        return system_status(), False
    if command in {"who are you", "what is your name"}:
        return f"I am {ASSISTANT_NAME}, your personal desktop assistant.", False
    if re.search(r"\b(time|date)\b", command):
        return f"It is {datetime.now().strftime('%A, %d %B, %I:%M %p')}.", False

    if command in {"cancel shutdown", "abort shutdown"}:
        return cancel_shutdown(), False
    if command in {"lock", "lock computer", "lock my computer"}:
        return lock(), False
    if command in {"take a screenshot", "take screenshot", "screenshot"}:
        return take_screenshot(), False
    if "battery" in command:
        return battery(), False
    if command in {"shutdown", "shutdown computer", "turn off computer"}:
        _pending_power_action = "shutdown"
        return "Shutdown is ready. Say yes to confirm, or cancel to keep your computer on.", False
    if command in {"restart", "restart computer", "reboot computer"}:
        _pending_power_action = "restart"
        return "Restart is ready. Say yes to confirm, or cancel to keep your computer on.", False

    desktop_response = desktop_handle(command)
    if desktop_response is not None:
        return desktop_response, False

    file_response = file_handle(command)
    if file_response is not None:
        if file_response.startswith("DELETE_CONFIRM:"):
            _pending_file_delete = file_response.removeprefix("DELETE_CONFIRM:")
            return "That action will permanently delete a file. Say yes to confirm, or cancel.", False
        return file_response, False

    if command.startswith(("open ", "launch ", "start ")):
        app = re.sub(r"^(open|launch|start)\s+", "", command).strip()
        if app in {"chrome", "google"}:
            return open_chrome(), False
        if app in {"youtube", "you tube"}:
            return open_youtube(), False
        if open_app(app):
            return f"Opening {app}.", False
        return f"I don't have an app shortcut for {app} yet.", False
    if command.startswith(("search for ", "search ", "google ")):
        query = re.sub(r"^(search for |search |google )", "", command).strip()
        return search_google(query), False

    if "weather" in command or "temperature" in command:
        match = re.search(r"\b(?:weather|temperature)\s+in\s+(.+)", command)
        return get_weather(match.group(1) if match else None), False

    if command.startswith("remember "):
        data = command.removeprefix("remember ").strip()
        if " is " not in data:
            return "Say it like: remember my favorite color is blue.", False
        key, value = data.split(" is ", 1)
        remember(key, value)
        return f"I will remember that {key} is {value}.", False
    if command.startswith("what is my ") or command.startswith("what's my "):
        key = re.sub(r"^what(?: is|'s) my ", "", command).strip(" ?")
        value = recall(key)
        return (f"Your {key} is {value}." if value else "I don't remember that yet."), False

    if needs_vision(command):
        # Vision dependencies are optional; import only when the feature is used.
        from vision.manager import process_vision
        return process_vision(command), False
    if command in {"exit", "quit", "goodbye", "close jarvis"}:
        return f"Goodbye {USER_NAME}.", True
    return ask_ai(command), False
