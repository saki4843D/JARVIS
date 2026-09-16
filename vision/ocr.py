from rapidocr_onnxruntime import RapidOCR

# Load the OCR engine once
engine = RapidOCR()


def extract_text(image_path):
    """
    Extract text from an image using RapidOCR.
    """

    try:
        result, _ = engine(image_path)

        if not result:
            return ""

        text = "\n".join([line[1] for line in result])

        return text.strip()

    except Exception as e:
        print("OCR Error:", e)
        return ""