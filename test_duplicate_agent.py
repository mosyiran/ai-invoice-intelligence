
from app.agents.state import InvoiceState
from app.agents.duplicate_agent import duplicate_agent


def main():

    test_invoice = {
        "invoice_number": "INV-AGENT-TEST-100",
        "invoice_date": "2026-11-20",
        "supplier_name": "Unique Test Supplier",
        "supplier_tax_id": "GB998877665",
        "customer_name": "XYZ Company",
        "currency": "GBP",
        "subtotal": 1000,
        "vat": 200,
        "total": 1200,
    }

    state: InvoiceState = {
        "invoice_data": test_invoice,
        "validation_result": {
            "is_valid": True,
            "errors": [],
            "warnings": [],
        },
        "errors": [],
    }

    print("\nTesting Duplicate Detection Agent...")

    result = duplicate_agent(state)

    print("\nDuplicate Detection Result:")
    print(result)

    assert result["status"] in (
        "unique",
        "duplicate",
        "manual_review",
    )

    assert "duplicate_type" in result["duplicate_result"]

    print("\nDuplicate Detection Agent test passed!")


if __name__ == "__main__":
    main()
