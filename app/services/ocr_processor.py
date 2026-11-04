from pathlib import Path
from paddleocr import PaddleOCR


# Initialize OCR engine once
ocr_engine = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    engine="paddle"
)


def extract_text_from_image(image_path: str):

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    # Run OCR
    results = ocr_engine.predict(str(image_path))

    extracted_lines = []

    for result in results:

        # Get structured result
        data = result.json

        if isinstance(data, dict):
            data = data.get("res", data)

        # Extract recognized text
        texts = data.get("rec_texts", [])

        # Extract confidence scores
        scores = data.get("rec_scores", [])

        for index, text in enumerate(texts):

            score = (
                float(scores[index])
                if index < len(scores)
                else None
            )

            extracted_lines.append({
                "text": text,
                "confidence": score
            })

    full_text = "\n".join(
        item["text"]
        for item in extracted_lines
    )

    return {
        "image": str(image_path),
        "text": full_text,
        "lines": extracted_lines
    }