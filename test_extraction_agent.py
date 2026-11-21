
from app.agents.state import InvoiceState
from app.agents.extraction_agent import extraction_agent


def main():

    test_invoice = {
        "invoice_number": "INV-1001",
        "invoice_date": "2026-11-20",
        "supplier_name": "ABC Technology Ltd",
        "supplier_tax_id": "GB123456789",
        "customer_name": "XYZ Company",
        "currency": "GBP",
        "subtotal": 1000,
        "vat": 200,
        "total": 1200,
    }

    initial_state: InvoiceState = {
        "raw_invoice_data": test_invoice,
        "errors": [],
    }

    print("\nInitial State:")
    print(initial_state)

    result = extraction_agent(initial_state)

    print("\nAgent Result:")
    print(result)

    assert result["status"] == "extracted"
    assert result["invoice_data"]["invoice_number"] == "INV-1001"
    assert result["invoice_data"]["total"] == 1200

    print("\nExtraction Agent test passed!")


if __name__ == "__main__":
    main()
