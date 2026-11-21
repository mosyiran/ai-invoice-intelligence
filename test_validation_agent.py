
from decimal import Decimal

from app.agents.state import InvoiceState
from app.agents.validation_agent import validation_agent


def main():

    # =====================================
    # Test 1: Valid Invoice
    # =====================================

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
        "invoice_data": test_invoice,
        "errors": [],
    }

    print("\nTesting valid invoice...")

    result = validation_agent(initial_state)

    print("\nValidation Result:")
    print(result)

    assert result["status"] == "validated"

    assert result["validation_result"]["is_valid"] is True

    assert Decimal(
        result["validation_result"]["calculated_total"]
    ) == Decimal("1200")

    assert Decimal(
        result["validation_result"]["difference"]
    ) == Decimal("0")

    print("\nValid invoice test passed!")

    # =====================================
    # Test 2: Invalid Invoice
    # =====================================

    invalid_invoice = test_invoice.copy()

    invalid_invoice["total"] = 1500

    invalid_state: InvoiceState = {
        "invoice_data": invalid_invoice,
        "errors": [],
    }

    print("\nTesting invalid invoice...")

    invalid_result = validation_agent(invalid_state)

    print("\nInvalid Validation Result:")
    print(invalid_result)

    assert invalid_result["status"] == "invalid"

    assert invalid_result["validation_result"]["is_valid"] is False

    assert len(
        invalid_result["validation_result"]["errors"]
    ) > 0

    print("\nInvalid invoice test passed!")


if __name__ == "__main__":
    main()
