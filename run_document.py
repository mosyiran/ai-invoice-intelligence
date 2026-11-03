from app.services.document_processor import process_document

import json


file_path = "sample_data/invoices/invoice_01.pdf"


result = process_document(file_path)


print("\n========== DOCUMENT PROCESSING RESULT ==========\n")

print(json.dumps(
    result,
    indent=4,
    ensure_ascii=False
))

print("\n=================================================")