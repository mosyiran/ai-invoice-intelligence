
from app.db.database import SessionLocal
from app.schemas.invoice import InvoiceData

from app.repositories.invoice_repository import (
    create_invoice,
    get_invoice,
    get_all_invoices,
)


sample_invoice = InvoiceData(
    invoice_number="INV-2026-001",
    invoice_date="2026-11-20",
    due_date="2026-12-20",
    supplier_name="ABC Technology Ltd",
    supplier_tax_id="GB123456789",
    customer_name="XYZ Company",
    currency="GBP",
    subtotal=1000,
    vat=200,
    total=1200,
)


def test_database():

    db = SessionLocal()

    try:

        # Create invoice
        invoice = create_invoice(
            db,
            sample_invoice
        )

        print("\nInvoice created:")
        print("ID:", invoice.id)
        print("Number:", invoice.invoice_number)
        print("Supplier:", invoice.supplier_name)
        print("Total:", invoice.total)

        # Get invoice
        saved_invoice = get_invoice(
            db,
            invoice.id
        )

        print("\nRetrieved invoice:")
        print(saved_invoice.invoice_number)

        # Get all invoices
        invoices = get_all_invoices(db)

        print("\nAll invoices:")

        for item in invoices:
            print(
                item.id,
                item.invoice_number,
                item.total
            )

    finally:
        db.close()


if __name__ == "__main__":
    test_database()
