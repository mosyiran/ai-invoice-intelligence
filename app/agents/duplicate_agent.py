
from decimal import Decimal

from app.agents.state import InvoiceState
from app.db.database import SessionLocal
from app.models.invoice import Invoice
from app.services.duplicate_detector import detect_duplicate


def duplicate_agent(state: InvoiceState) -> dict:
    """
    Detect exact, normalized and potential duplicate invoices.
    """

    print("\n[Duplicate Detection Agent] Started")

    invoice_data = state.get("invoice_data")

    if not invoice_data:
        error_message = "No invoice data available."

        return {
            "status": "failed",
            "duplicate_result": {
                "is_duplicate": False,
                "duplicate_type": None,
                "matched_invoice_id": None,
                "message": error_message,
            },
            "errors": [error_message],
        }

    validation_result = state.get("validation_result", {})

    if not validation_result.get("is_valid", False):
        error_message = "Invoice failed financial validation."

        return {
            "status": "invalid",
            "duplicate_result": {
                "is_duplicate": False,
                "duplicate_type": None,
                "matched_invoice_id": None,
                "message": error_message,
            },
            "errors": [error_message],
        }

    db = SessionLocal()

    try:
        invoice = Invoice(
            invoice_number=invoice_data.get("invoice_number"),
            invoice_date=invoice_data.get("invoice_date"),
            due_date=invoice_data.get("due_date"),
            supplier_name=invoice_data.get("supplier_name"),
            supplier_tax_id=invoice_data.get("supplier_tax_id"),
            customer_name=invoice_data.get("customer_name"),
            currency=invoice_data.get("currency"),
            subtotal=(
                Decimal(str(invoice_data["subtotal"]))
                if invoice_data.get("subtotal") is not None
                else None
            ),
            vat=(
                Decimal(str(invoice_data["vat"]))
                if invoice_data.get("vat") is not None
                else None
            ),
            total=(
                Decimal(str(invoice_data["total"]))
                if invoice_data.get("total") is not None
                else None
            ),
        )

        duplicate_result = detect_duplicate(
            db=db,
            invoice=invoice,
        )

        duplicate_type = duplicate_result["duplicate_type"]

        if duplicate_type in ("exact", "normalized"):
            status = "duplicate"

        elif duplicate_type == "potential":
            status = "manual_review"

        else:
            status = "unique"

        print("[Duplicate Detection Agent] Completed.")
        print("Duplicate type:", duplicate_type)
        print("Status:", status)

        return {
            "duplicate_result": duplicate_result,
            "status": status,
        }

    except Exception as exc:

        error_message = f"Duplicate detection failed: {str(exc)}"

        print("[Duplicate Detection Agent] Error:", error_message)

        return {
            "status": "failed",
            "duplicate_result": {
                "is_duplicate": False,
                "duplicate_type": None,
                "matched_invoice_id": None,
                "message": error_message,
            },
            "errors": [error_message],
        }

    finally:
        db.close()
