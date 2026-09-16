from vision.screenshot import capture_screen
from vision.vision_ai import analyze_image
from vision.prompts import VISION_PROMPTS


def describe_screen(command):

    command = command.lower()

    # Default prompt
    prompt = VISION_PROMPTS["describe"]

    # ---------- Programming ----------
    if any(word in command for word in [
        "code",
        "program",
        "python",
        "java",
        "bug",
        "debug"
    ]):
        prompt = VISION_PROMPTS["code"]

    # ---------- Errors ----------
    elif any(word in command for word in [
        "error",
        "issue",
        "problem",
        "exception",
        "traceback",
        "failed"
    ]):
        prompt = VISION_PROMPTS["error"]

    # ---------- Websites ----------
    elif any(word in command for word in [
        "website",
        "webpage",
        "page",
        "browser"
    ]):
        prompt = VISION_PROMPTS["website"]

    # ---------- Documents ----------
    elif any(word in command for word in [
        "document",
        "pdf",
        "notes",
        "article"
    ]):
        prompt = VISION_PROMPTS["document"]

    # ---------- Charts ----------
    elif any(word in command for word in [
        "chart",
        "graph",
        "plot",
        "statistics"
    ]):
        prompt = VISION_PROMPTS["chart"]

    # ---------- OCR ----------
    elif any(word in command for word in [
        "read",
        "text",
        "ocr",
        "extract"
    ]):
        prompt = VISION_PROMPTS["ocr"]

    print("\n========== JARVIS VISION ==========")
    print("Prompt:", prompt)
    print("Capturing screen...")

    image = capture_screen()

    print("Analyzing...")

    result = analyze_image(image, prompt)

    print("Done.\n")

    return result