"""Application launching and window-focus helpers for JARVIS."""

import subprocess
import time

import pyautogui


APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "command prompt": "cmd.exe",
    "terminal": "wt.exe",
    "windows terminal": "wt.exe",
    "visual studio code": "code",
    "vscode": "code",
    "explorer": "explorer.exe",
}


def _focus_window(title_keywords, timeout=5):
    """Try to bring a matching application window to the foreground."""

    try:
        import pygetwindow as gw
    except ImportError:
        print("[APPS] pygetwindow is not installed.")
        return False

    deadline = time.time() + timeout

    while time.time() < deadline:

        try:
            windows = gw.getAllWindows()

            for window in windows:

                title = (window.title or "").lower()

                if not title:
                    continue

                if any(
                    keyword.lower() in title
                    for keyword in title_keywords
                ):

                    try:
                        if window.isMinimized:
                            window.restore()

                        window.activate()

                        time.sleep(0.3)

                        print(
                            f"[APPS] Focused window: "
                            f"{window.title!r}"
                        )

                        return True

                    except Exception as exc:
                        print(
                            f"[APPS] Could not activate "
                            f"{window.title!r}: {exc}"
                        )

        except Exception as exc:
            print(
                f"[APPS] Window detection error: {exc}"
            )

        time.sleep(0.2)

    return False


def open_app(app_name):
    """Launch an application and attempt to focus its window."""

    app_name = app_name.lower().strip()

    if app_name not in APPS:
        return False

    try:
        print(
            f"[APPS] Opening application: "
            f"{app_name}"
        )

        subprocess.Popen(
            APPS[app_name],
            shell=False,
        )

    except OSError as exc:
        print(
            f"[APPS] Failed to launch "
            f"{app_name}: {exc}"
        )
        return False

    # Give Windows a moment to create the window.
    time.sleep(0.7)

    # Window titles vary by application.
    focus_keywords = {
        "notepad": ["notepad"],
        "calculator": ["calculator"],
        "paint": ["paint"],
        "command prompt": [
            "command prompt",
            "cmd",
        ],
        "terminal": [
            "terminal",
            "windows terminal",
        ],
        "windows terminal": [
            "terminal",
            "windows terminal",
        ],
        "visual studio code": [
            "visual studio code",
        ],
        "vscode": [
            "visual studio code",
        ],
        "explorer": [
            "file explorer",
        ],
    }

    keywords = focus_keywords.get(
        app_name,
        [app_name],
    )

    focused = _focus_window(
        keywords,
        timeout=5,
    )

    if not focused:
        print(
            f"[APPS] Application opened, but "
            f"JARVIS could not confirm the window focus: "
            f"{app_name}"
        )

    return True