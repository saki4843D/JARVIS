"""Manual vision check. Run directly; it captures the active screen."""
from vision.screenshot import capture_screen
from vision.vision_ai import analyze_image


if __name__ == "__main__":
    print(analyze_image(capture_screen(), "Describe this screen briefly."))
