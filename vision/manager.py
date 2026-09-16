from vision.screenshot import capture_screen
from vision.vision_ai import analyze_image
from vision.cropper import (
    crop_code,
    crop_browser,
    crop_document,
)
from vision.ocr import extract_text
from vision.reader import ask_from_screen

from vision.prompts import (
    CODE,
    DOCUMENT,
    WEBPAGE,
    DESCRIBE,
)


def process_vision(command):

    command = command.lower().strip()

    print("\n========== JARVIS VISION ==========")

    print("Capturing screen...")

    image = capture_screen()

    # =====================================================
    # CODE
    # =====================================================

    if any(word in command for word in [
        "code",
        "bug",
        "error",
        "fix",
        "traceback",
        "exception",
        "program",
        "script",
    ]):

        print("Mode : CODE")

        image = crop_code(image)

        print("Running OCR...")

        text = extract_text(image)

        if len(text.strip()) > 100:

            print("OCR Successful")

            return ask_from_screen(
                text,
                command
            )

        print("OCR insufficient.")
        print("Switching to Vision...")

        return analyze_image(
            image,
            CODE + "\n\nUser Request:\n" + command
        )

    # =====================================================
    # DOCUMENT
    # =====================================================

    elif any(word in command for word in [
        "document",
        "pdf",
        "notes",
        "read",
        "file",
        "article",
    ]):

        print("Mode : DOCUMENT")

        image = crop_document(image)

        print("Running OCR...")

        text = extract_text(image)

        if len(text.strip()) > 100:

            print("OCR Successful")

            return ask_from_screen(
                text,
                command
            )

        print("OCR insufficient.")
        print("Switching to Vision...")

        return analyze_image(
            image,
            DOCUMENT + "\n\nUser Request:\n" + command
        )

    # =====================================================
    # WEBSITE
    # =====================================================

    elif any(word in command for word in [
        "website",
        "webpage",
        "browser",
        "chrome",
        "page",
        "summarize",
        "summarise",
    ]):

        print("Mode : WEBSITE")

        image = crop_browser(image)

        print("Running OCR...")

        text = extract_text(image)

        if len(text.strip()) > 100:

            print("OCR Successful")

            return ask_from_screen(
                text,
                command
            )

        print("OCR insufficient.")
        print("Switching to Vision...")

        return analyze_image(
            image,
            WEBPAGE + "\n\nUser Request:\n" + command
        )

    # =====================================================
    # OCR
    # =====================================================

    elif any(word in command for word in [
        "extract text",
        "read text",
        "copy text",
        "ocr",
    ]):

        print("Mode : OCR")

        text = extract_text(image)

        if text.strip():

            return ask_from_screen(
                text,
                command
            )

        return "Sorry Sathwik, I couldn't detect any readable text."

    # =====================================================
    # GENERAL VISION
    # =====================================================

    else:

        print("Mode : GENERAL")

        return analyze_image(
            image,
            DESCRIBE + "\n\nUser Request:\n" + command
        )