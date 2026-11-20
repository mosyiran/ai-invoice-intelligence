
from app.db.database import SessionLocal
from app.schemas.invoice import InvoiceData

from app.repositories.invoice_repository import create_invoice


def make_invoice(
    number,
    supplier,
    tax_id,
    invoice_date,
    total,
):

    return InvoiceData(
        invoice_number=number,
        invoice_date=invoice_date,
        due_date="2026-12-20",
        supplier_name=supplier,
        supplier_tax_id=tax_id,
        customer_name="XYZ Company",
        currency="GBP",
        subtotal=1000,
        vat=200,
        total=total,
    )


def run_tests():

    db = SessionLocal()

    try:

        # Test 1: Create first invoice
        first_invoice = make_invoice(
            "INV-TEST-100",
            "ABC Technology Ltd",
            "GB123456789",
            "2026-11-20",
            1200,
        )

        saved = create_invoice(db, first_invoice)

        print("First invoice saved:", saved.id)

        # Test 2: Same invoice with different formatting
        duplicate_invoice = make_invoice(
            "inv test 100",
            "abc technology ltd",
            "GB-123456789",
            "2026-11-20",
            1200,
        )

        try:

            create_invoice(db, duplicate_invoice)

            print("ERROR: Duplicate was not detected!")

        except ValueError as error:

            print("Duplicate successfully detected:")
            print(error)

        # Test 3: Same amount and date, different number
        potential_invoice = make_invoice(
            "INV-TEST-101",
            "ABC Technology Ltd",
            "GB123456789",
            "2026-11-20",
            1200,
        )

        potential_saved = create_invoice(
            db,
            potential_invoice
        )

        print(
            "Potential duplicate was allowed:",
            potential_saved.id
        )

    finally:
        db.close()


if __name__ == "__main__":
    run_tests()
