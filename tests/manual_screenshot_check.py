"""Manual screenshot check. Run directly; it captures the active screen."""
from vision.screenshot import capture_screen


if __name__ == "__main__":
    print(capture_screen())
