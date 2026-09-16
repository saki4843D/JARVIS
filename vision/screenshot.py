import pyautogui
import pygetwindow as gw
from PIL import Image


def capture_screen():

    try:

        # Get the currently active window
        window = gw.getActiveWindow()

        if window is None:
            raise Exception("No active window")

        left = window.left
        top = window.top
        width = window.width
        height = window.height

        print(f"Active Window : {window.title}")
        print(f"Size : {width} x {height}")

        image = pyautogui.screenshot(
            region=(left, top, width, height)
        )

    except Exception:

        print("Falling back to full screen...")

        image = pyautogui.screenshot()

    # Resize for faster inference
    image = image.resize((800, 450), Image.Resampling.LANCZOS)

    filename = "temp/vision_screen.jpg"

    image.save(filename, quality=60)

    print("Captured:", filename)

    return filename