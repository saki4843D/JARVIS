"""Manual OCR check. Run directly; it captures the active screen."""
from vision.ocr import extract_text
from vision.screenshot import capture_screen


if __name__ == "__main__":
    print(extract_text(capture_screen()) or "No text detected.")
