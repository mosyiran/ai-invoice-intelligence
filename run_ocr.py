import json

from app.services.ocr_processor import (
    extract_text_from_image
)


image_path = "sample_data/invoices/invoice_01.png"

result = extract_text_from_image(image_path)

print("\n========== OCR RESULT ==========\n")

print(
    json.dumps(
        result,
        indent=4,
        ensure_ascii=False
    )
)