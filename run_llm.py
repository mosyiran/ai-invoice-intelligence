import json

from app.services.llm_extractor import extract_invoice_data


sample_ocr_text = """
INVOICE

Invoice Number: INV-2026-105

Invoice Date: 2026-11-01

Due Date: 2026-11-30

Supplier: ABC Technology Ltd

Supplier Tax ID: GB123456789

Customer: XYZ Company

Subtotal: 1000.00 GBP

VAT: 200.00 GBP

Total: 1200.00 GBP
"""


# Extract invoice information
result = extract_invoice_data(sample_ocr_text)


# Display result
print("\n========== GEMINI EXTRACTION RESULT ==========\n")

print(
    json.dumps(
        result,
        indent=4,
        ensure_ascii=False
    )
)