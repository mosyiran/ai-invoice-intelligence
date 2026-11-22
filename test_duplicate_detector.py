
from datetime import date
from decimal import Decimal
from uuid import uuid4

from app.db.database import SessionLocal
from app.models.invoice import Invoice
from app.services.duplicate_detector import detect_duplicate


def create_invoice(
    invoice_number,
    supplier_name,
    supplier_tax_id,
    invoice_date,
    total,
    currency="USD",
):
    return Invoice(
        invoice_number=invoice_number,
        supplier_name=supplier_name,
        supplier_tax_id=supplier_tax_id,
        invoice_date=invoice_date,
        currency=currency,
        subtotal=Decimal("1000.00"),
        vat=Decimal("200.00"),
        total=Decimal(str(total)),
    )


def run_test(
    test_name,
    existing_invoice,
    new_invoice,
    expected_type,
):
    db = SessionLocal()
    existing_id = None

    try:
        # Store the existing invoice in SQLite.
        db.add(existing_invoice)
        db.commit()
        db.refresh(existing_invoice)

        existing_id = existing_invoice.id

        # Detect duplicate against the existing invoice.
        result = detect_duplicate(
            db=db,
            invoice=new_invoice,
        )

        actual_type = result["duplicate_type"]

        print(f"\n{test_name}")
        print("Expected:", expected_type)
        print("Actual:", actual_type)
        print("Result:", result)

        assert actual_type == expected_type, (
            f"{test_name} failed: "
            f"expected {expected_type}, got {actual_type}"
        )

        print(f"{test_name} passed!")

    finally:
        # Remove only the test invoice.
        if existing_id is not None:
            db.query(Invoice).filter(
                Invoice.id == existing_id
            ).delete(synchronize_session=False)

            db.commit()

        db.close()


def test_exact_duplicate():
    suffix = uuid4().hex[:10].upper()

    existing = create_invoice(
        invoice_number=f"INV-EXACT-{suffix}",
        supplier_name="Exact Test Company",
        supplier_tax_id=f"TAX-{suffix}",
        invoice_date=date(2026, 11, 22),
        total="1200.00",
    )

    new = create_invoice(
        invoice_number=f"INV-EXACT-{suffix}",
        supplier_name="Another Company",
        supplier_tax_id=f"TAX-{suffix}",
        invoice_date=date(2026, 11, 23),
        total="1500.00",
    )

    run_test(
        "Exact Duplicate Test",
        existing,
        new,
        "exact",
    )


def test_normalized_duplicate():
    suffix = uuid4().hex[:10].upper()

    existing = create_invoice(
        invoice_number=f"INV-NORM-{suffix}",
        supplier_name="Normalized Test Company",
        supplier_tax_id=f"TAX-A-{suffix}",
        invoice_date=date(2026, 11, 22),
        total="1200.00",
    )

    new = create_invoice(
        invoice_number=f" INV / NORM - {suffix} ",
        supplier_name="  NORMALIZED   TEST COMPANY ",
        supplier_tax_id=f"TAX-B-{suffix}",
        invoice_date=date(2026, 11, 23),
        total="1500.00",
    )

    run_test(
        "Normalized Duplicate Test",
        existing,
        new,
        "normalized",
    )


def test_potential_duplicate():
    suffix = uuid4().hex[:10].upper()

    existing = create_invoice(
        invoice_number=f"INV-POTENTIAL-A-{suffix}",
        supplier_name="Potential Test Company",
        supplier_tax_id=f"TAX-A-{suffix}",
        invoice_date=date(2026, 11, 22),
        total="1200.00",
    )

    new = create_invoice(
        invoice_number=f"INV-POTENTIAL-B-{suffix}",
        supplier_name=" potential test company ",
        supplier_tax_id=f"TAX-B-{suffix}",
        invoice_date=date(2026, 11, 22),
        total="1200.00",
    )

    run_test(
        "Potential Duplicate Test",
        existing,
        new,
        "potential",
    )


def test_unique_invoice():
    suffix = uuid4().hex[:10].upper()

    existing = create_invoice(
        invoice_number=f"INV-UNIQUE-A-{suffix}",
        supplier_name="Unique Company A",
        supplier_tax_id=f"TAX-A-{suffix}",
        invoice_date=date(2026, 11, 22),
        total="1200.00",
    )

    new = create_invoice(
        invoice_number=f"INV-UNIQUE-B-{suffix}",
        supplier_name="Unique Company B",
        supplier_tax_id=f"TAX-B-{suffix}",
        invoice_date=date(2026, 11, 23),
        total="2500.00",
    )

    run_test(
        "Unique Invoice Test",
        existing,
        new,
        None,
    )


if __name__ == "__main__":
    print("Testing Duplicate Detection Service...")

    test_exact_duplicate()
    test_normalized_duplicate()
    test_potential_duplicate()
    test_unique_invoice()

    print("\nAll Duplicate Detection tests passed!")
