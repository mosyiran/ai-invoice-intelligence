
from app.schemas.invoice import InvoiceData
from app.services.financial_validator import validate_invoice


def run_test(name, data):

    invoice = InvoiceData.model_validate(data)

    result = validate_invoice(invoice)

    print(f"\n========== {name} ==========")

    print("Valid:", result.is_valid)
    print("Calculated Total:", result.calculated_total)
    print("Difference:", result.difference)

    print("Errors:")
    for error in result.errors:
        print("-", error)

    print("Warnings:")
    for warning in result.warnings:
        print("-", warning)


# Test 1: Valid invoice
valid_invoice = {
    "invoice_number": "INV-1001",
    "currency": "GBP",
    "subtotal": 1000,
    "vat": 200,
    "total": 1200
}


# Test 2: Invalid total
invalid_invoice = {
    "invoice_number": "INV-1002",
    "currency": "GBP",
    "subtotal": 1000,
    "vat": 200,
    "total": 1500
}


# Test 3: Missing VAT
incomplete_invoice = {
    "invoice_number": "INV-1003",
    "currency": "GBP",
    "subtotal": 1000,
    "vat": None,
    "total": 1200
}


run_test("VALID INVOICE", valid_invoice)

run_test("INVALID INVOICE", invalid_invoice)

run_test("INCOMPLETE INVOICE", incomplete_invoice)
