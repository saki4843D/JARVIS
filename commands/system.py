import pyautogui
import psutil
import os


def take_screenshot():

    image = pyautogui.screenshot()
    image.save("screenshot.png")

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