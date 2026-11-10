
from app.schemas.invoice import InvoiceData


sample_data = {
    "invoice_number": "INV-1001",
    "invoice_date": "2026-11-01",
    "due_date": "2026-11-30",
    "supplier_name": "ABC Technology Ltd",
    "supplier_tax_id": "GB123456789",
    "customer_name": "XYZ Company",
    "currency": "GBP",
    "subtotal": 1000.0,
    "vat": 200.0,
    "total": 1200.0
}


invoice = InvoiceData.model_validate(sample_data)

print("========== PYDANTIC OBJECT ==========")
print(invoice)

print("\n========== JSON OUTPUT ==========")
print(invoice.model_dump_json(indent=4))

print("\n========== VALIDATION SUCCESSFUL ==========")
