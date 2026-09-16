"""Guarded, deterministic desktop controls for JARVIS.

This module handles safe, explicit computer-control actions.
AI-generated text is never executed directly as arbitrary Python code.
"""

import re
import time

import pyautogui


# ------------------------------------------------------------
# PYAutoGUI configuration
# ------------------------------------------------------------

pyautogui.PAUSE = 0.12

# Move the mouse to the top-left corner to immediately stop
# an active PyAutoGUI operation.
pyautogui.FAILSAFE = True


# ------------------------------------------------------------
# Allowed keyboard keys
# ------------------------------------------------------------

SAFE_KEYS = {
    "enter",
    "tab",
    "escape",
    "space",
    "home",
    "end",
    "pageup",
    "pagedown",
    "up",
    "down",
    "left",
    "right",
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "f10",
    "f11",
    "f12",
}

SAFE_KEYS.update(
    chr(code)
    for code in range(ord("a"), ord("z") + 1)
)

SAFE_KEYS.update(
    str(number)
    for number in range(10)
)


# ------------------------------------------------------------
# Keyboard shortcuts
# ------------------------------------------------------------

SHORTCUTS = {
    "copy": ("ctrl", "c"),
    "paste": ("ctrl", "v"),
    "cut": ("ctrl", "x"),
    "select all": ("ctrl", "a"),
    "save": ("ctrl", "s"),
    "undo": ("ctrl", "z"),
    "redo": ("ctrl", "y"),

    "new tab": ("ctrl", "t"),
    "next tab": ("ctrl", "tab"),
    "previous tab": ("ctrl", "shift", "tab"),

    "switch window": ("alt", "tab"),

    "show desktop": ("win", "d"),
    "show the desktop": ("win", "d"),
    "show my desktop": ("win", "d"),
    "desktop": ("win", "d"),
    "minimize all windows": ("win", "d"),
    "show desktop please": ("win", "d"),

    "minimize window": ("win", "down"),
    "maximize window": ("win", "up"),
}


# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------

def _clean_command(command: str) -> str:
    """Normalize common conversational prefixes."""

    command = command.lower().strip()

    # Remove conversational prefixes.
    command = re.sub(
        r"^(?:ok|okay|please|can you|could you)\s+",
        "",
        command,
    ).strip()

    return command


def _coordinates(command):
    """Extract screen coordinates from a spoken command."""

    match = re.search(
        r"(?:at|to)\s+"
        r"(\d{1,5})"
        r"\s*(?:,|x|by|\s)\s*"
        r"(\d{1,5})\b",
        command,
    )

    if not match:
        return None

    x = int(match.group(1))
    y = int(match.group(2))

    width, height = pyautogui.size()

    if 0 <= x < width and 0 <= y < height:
        return (x, y)

    return False


def _perform(action):
    """Safely execute a desktop action."""

    try:
        return action()

    except pyautogui.FailSafeException:
        return (
            "Desktop control stopped by the emergency "
            "mouse failsafe."
        )

    except OSError:
        return "I couldn't complete that desktop action."

    except Exception as exc:
        print(f"[DESKTOP ERROR] {type(exc).__name__}: {exc}")
        return "I couldn't complete that desktop action."


def _outcome(action, success_message):
    """Execute an action and return a spoken response."""

    result = _perform(action)

    if isinstance(result, str):
        return result

    return success_message


# ------------------------------------------------------------
# Text typing
# ------------------------------------------------------------

def _type_text(text: str):
    """Type text into the currently focused application."""

    if not text:
        return "Tell me the text you want typed."

    # Small delay gives the target application time to receive
    # focus after an open/launch operation.
    time.sleep(0.25)

    print(f"[DESKTOP] Typing: {text!r}")

    try:
        pyautogui.write(
            text,
            interval=0.04,
        )

        print("[DESKTOP] Typing completed.")

        return f'Text entered: "{text}".'

    except pyautogui.FailSafeException:
        return (
            "Desktop control stopped by the emergency "
            "mouse failsafe."
        )

    except Exception as exc:
        print(
            f"[DESKTOP ERROR] Typing failed: "
            f"{type(exc).__name__}: {exc}"
        )
        return "I couldn't type that text."


# ------------------------------------------------------------
# Main desktop command handler
# ------------------------------------------------------------

def handle(command: str):
    """Handle a safe desktop action.

    Returns:
        str: Spoken response when the command is handled.
        None: When the command is not a desktop command.
    """

    if not isinstance(command, str):
        return None

    command = _clean_command(command)

    if not command:
        return None

    print(f"[DESKTOP] Command: {command!r}")

    # --------------------------------------------------------
    # Keyboard shortcuts
    # --------------------------------------------------------

    for phrase, keys in SHORTCUTS.items():

        if command in {
            phrase,
            f"{phrase} please",
        }:

            return _outcome(
                lambda keys=keys: pyautogui.hotkey(*keys),
                f"{phrase.title()} executed.",
            )

    # --------------------------------------------------------
    # Volume
    # --------------------------------------------------------

    if command in {
        "volume up",
        "increase volume",
        "turn volume up",
    }:

        return _outcome(
            lambda: pyautogui.press(
                "volumeup",
                presses=2,
            ),
            "Volume increased.",
        )

    if command in {
        "volume down",
        "decrease volume",
        "turn volume down",
    }:

        return _outcome(
            lambda: pyautogui.press(
                "volumedown",
                presses=2,
            ),
            "Volume decreased.",
        )

    if command in {
        "mute",
        "unmute",
        "toggle mute",
    }:

        return _outcome(
            lambda: pyautogui.press(
                "volumemute",
            ),
            "Mute toggled.",
        )

    # --------------------------------------------------------
    # Media
    # --------------------------------------------------------

    if command in {
        "play",
        "pause",
        "play pause",
        "play or pause",
    }:

        return _outcome(
            lambda: pyautogui.press(
                "playpause",
            ),
            "Media playback toggled.",
        )

    if command == "next track":

        return _outcome(
            lambda: pyautogui.press(
                "nexttrack",
            ),
            "Skipping to the next track.",
        )

    if command == "previous track":

        return _outcome(
            lambda: pyautogui.press(
                "prevtrack",
            ),
            "Going to the previous track.",
        )

    # --------------------------------------------------------
    # Mouse movement
    # --------------------------------------------------------

    if command.startswith(
        (
            "move mouse",
            "move cursor",
        )
    ):

        point = _coordinates(command)

        if point is False:
            return "Those coordinates are outside your screen."

        if point is None:
            return "Say: move mouse to 500, 300."

        return _outcome(
            lambda point=point: pyautogui.moveTo(
                *point,
                duration=0.25,
            ),
            (
                f"Pointer moved to "
                f"{point[0]}, {point[1]}."
            ),
        )

    # --------------------------------------------------------
    # Mouse clicking
    # --------------------------------------------------------

    click_type = None

    if command.startswith("double click"):
        click_type = "double"

    elif command.startswith("right click"):
        click_type = "right"

    elif command.startswith("click"):
        click_type = "single"

    if click_type:

        point = _coordinates(command)

        if point is False:
            return "Those coordinates are outside your screen."

        if point is None:
            return "Say: click at 500, 300."

        if click_type == "double":

            return _outcome(
                lambda point=point: pyautogui.doubleClick(
                    *point,
                    interval=0.12,
                ),
                (
                    f"Double click completed at "
                    f"{point[0]}, {point[1]}."
                ),
            )

        if click_type == "right":

            return _outcome(
                lambda point=point: pyautogui.rightClick(
                    *point,
                ),
                (
                    f"Right click completed at "
                    f"{point[0]}, {point[1]}."
                ),
            )

        return _outcome(
            lambda point=point: pyautogui.click(
                *point,
            ),
            (
                f"Click completed at "
                f"{point[0]}, {point[1]}."
            ),
        )

    # --------------------------------------------------------
    # Scrolling
    # --------------------------------------------------------

    if command.startswith("scroll "):

        match = re.match(
            r"scroll\s+(up|down)"
            r"(?:\s+(\d{1,2}))?$",
            command,
        )

        if not match:
            return "Say: scroll down 3."

        direction, amount = match.groups()

        amount = int(amount or 3)

        if direction == "up":
            amount = abs(amount)
        else:
            amount = -abs(amount)

        return _outcome(
            lambda: pyautogui.scroll(amount),
            f"Scrolled {direction}.",
        )

    # --------------------------------------------------------
    # Type / Write text
    # --------------------------------------------------------

    if command.startswith(
        (
            "type ",
            "write ",
        )
    ):

        text = re.sub(
            r"^(?:type|write)\s+",
            "",
            command,
        ).strip()

        return _type_text(text)

    # --------------------------------------------------------
    # Press a key
    # --------------------------------------------------------

    if command.startswith("press "):

        key = (
            command
            .removeprefix("press ")
            .strip()
            .replace(" key", "")
        )

        if key not in SAFE_KEYS:

            return (
                "I can press letters, numbers, Enter, "
                "Tab, Escape, arrows, Home, End, Page Up, "
                "Page Down, and F keys."
            )

        return _outcome(
            lambda: pyautogui.press(key),
            f"Pressed {key}.",
        )

    # --------------------------------------------------------
    # Not a desktop command
    # --------------------------------------------------------

    return None
