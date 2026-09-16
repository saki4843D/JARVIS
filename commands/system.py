import pyautogui
import psutil
import os
import requests
from pathlib import Path

from config import ASSISTANT_NAME, OLLAMA_URL
from listen import get_listener_status


def take_screenshot():

    image = pyautogui.screenshot()
    output = Path(__file__).resolve().parent.parent / "screenshot.png"
    image.save(output)

    return "Screenshot taken."


def battery():

    battery = psutil.sensors_battery()

    if battery:
        return f"Battery is {battery.percent} percent."

    return "Battery information unavailable."


def shutdown():

    os.system("shutdown /s /t 1")

    return "Shutting down your computer."


def restart():

    os.system("shutdown /r /t 1")

    return "Restarting your computer."


def lock():

    os.system("rundll32.exe user32.dll,LockWorkStation")

    return "Locking your computer."


def cancel_shutdown():
    """Cancel a shutdown/restart countdown if Windows has one pending."""
    os.system("shutdown /a")
    return "Any pending shutdown has been cancelled."


def system_status():
    """Return a concise readiness report without changing system state."""
    memory = psutil.virtual_memory()
    battery_info = psutil.sensors_battery()
    battery = f"{battery_info.percent:.0f}%" if battery_info else "unavailable"
    microphone = get_listener_status()
    try:
        requests.get(f"{OLLAMA_URL}/api/tags", timeout=0.4)
        ollama = "online"
    except requests.RequestException:
        ollama = "offline"
    return (
        f"{ASSISTANT_NAME} is online. CPU load is {psutil.cpu_percent(interval=0.1):.0f}%, "
        f"memory usage is {memory.percent:.0f}%, battery is {battery}. "
        f"Microphone is {microphone['state']} ({microphone['detail']}); "
        f"local AI is {ollama}. Typed commands and desktop controls are enabled."
    )
