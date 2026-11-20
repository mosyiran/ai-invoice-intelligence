
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceData

from app.services.duplicate_detector import detect_duplicate


def decimal_or_none(value):

    if value is None:
        return None

    return Decimal(str(value))


def create_invoice(
    db: Session,
    invoice_data: InvoiceData
) -> Invoice:

    # Build invoice object before saving
    invoice = Invoice(
        invoice_number=invoice_data.invoice_number,
        invoice_date=invoice_data.invoice_date,
        due_date=invoice_data.due_date,
        supplier_name=invoice_data.supplier_name,
        supplier_tax_id=invoice_data.supplier_tax_id,
        customer_name=invoice_data.customer_name,
        currency=invoice_data.currency,
        subtotal=decimal_or_none(invoice_data.subtotal),
        vat=decimal_or_none(invoice_data.vat),
        total=decimal_or_none(invoice_data.total),
    )

    # Check for duplicate before inserting
    duplicate_result = detect_duplicate(db, invoice)

    if duplicate_result["is_duplicate"]:
        raise ValueError(
            f"Duplicate invoice detected. "
            f"Type: {duplicate_result['duplicate_type']}, "
            f"Existing invoice ID: "
            f"{duplicate_result['matched_invoice_id']}"
        )

    # Save invoice
    try:
        db.add(invoice)
        db.commit()
        db.refresh(invoice)

    except Exception:
        db.rollback()
        raise

    return invoice
