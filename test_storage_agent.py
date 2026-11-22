
from uuid import uuid4

from sqlalchemy import select

from app.agents.storage_agent import storage_agent
from app.db.database import SessionLocal
from app.models.invoice import Invoice


def test_successful_storage():
    print("\nTesting successful invoice storage...")

    unique_number = f"INV-STORAGE-{uuid4().hex[:10].upper()}"

    state = {
        "invoice_data": {
            "invoice_number": unique_number,
            "invoice_date": "2026-11-22",
            "due_date": "2026-12-22",
            "supplier_name": "Storage Test Company",
            "supplier_tax_id": f"ST-{uuid4().hex[:10].upper()}",
            "customer_name": "Test Customer",
            "currency": "USD",
            "subtotal": 1000,
            "vat": 200,
            "total": 1200,
        },
        "validation_result": {
            "is_valid": True,
            "errors": [],
            "warnings": [],
        },
        "duplicate_result": {
            "is_duplicate": False,
            "duplicate_type": None,
            "matched_invoice_id": None,
            "message": "No duplicate detected.",
        },
        "status": "unique",
    }

    result = storage_agent(state)

    print("\nStorage Result:")
    print(result)

    assert result["status"] == "stored"
    assert result["invoice_id"] is not None

    # Verify that the invoice really exists in SQLite
    db = SessionLocal()

    try:
        saved_invoice = db.scalar(
            select(Invoice).where(
                Invoice.id == result["invoice_id"]
            )
        )

        assert saved_invoice is not None
        assert saved_invoice.invoice_number == unique_number
        assert saved_invoice.supplier_name == "Storage Test Company"

        print("\nDatabase verification passed!")
        print("Saved invoice ID:", saved_invoice.id)
        print("Invoice number:", saved_invoice.invoice_number)

        # Clean up the test record
        db.delete(saved_invoice)
        db.commit()

        print("Test record cleaned up.")

    finally:
        db.close()

    print("Successful storage test passed!")


def test_duplicate_rejection():
    print("\nTesting duplicate rejection...")

    state = {
        "invoice_data": {
            "invoice_number": "INV-DUPLICATE-TEST",
        },
        "validation_result": {
            "is_valid": True,
        },
        "duplicate_result": {
            "is_duplicate": True,
            "duplicate_type": "exact",
            "matched_invoice_id": 1,
            "message": "Exact duplicate detected.",
        },
    }

    result = storage_agent(state)

    print("Result:", result)

    assert result["status"] == "duplicate"

    print("Duplicate rejection test passed!")


def test_manual_review_rejection():
    print("\nTesting potential duplicate rejection...")

    state = {
        "invoice_data": {
            "invoice_number": "INV-POTENTIAL-TEST",
        },
        "validation_result": {
            "is_valid": True,
        },
        "duplicate_result": {
            "is_duplicate": False,
            "duplicate_type": "potential",
            "matched_invoice_id": 10,
            "message": "Potential duplicate detected.",
        },
    }

    result = storage_agent(state)

    print("Result:", result)

    assert result["status"] == "manual_review"

    print("Manual review test passed!")


if __name__ == "__main__":
    print("Testing Storage Agent...")

    test_successful_storage()
    test_duplicate_rejection()
    test_manual_review_rejection()

    print("\nAll Storage Agent tests passed!")
