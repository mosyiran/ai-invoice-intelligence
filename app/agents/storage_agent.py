
from app.agents.state import InvoiceState
from app.db.database import SessionLocal
from app.schemas.invoice import InvoiceData
from app.repositories.invoice_repository import create_invoice


def storage_agent(state: InvoiceState) -> dict:
    print("\n[Storage Agent] Started")

    # Step 1: Check financial validation
    validation_result = state.get("validation_result", {})

    if not validation_result.get("is_valid", False):
        error_message = "Cannot store an invoice that failed validation."

        print("[Storage Agent] Rejected:", error_message)

        return {
            "status": "invalid",
            "errors": [error_message],
        }

    # Step 2: Check duplicate detection result
    duplicate_result = state.get("duplicate_result", {})
    duplicate_type = duplicate_result.get("duplicate_type")

    if duplicate_type in ("exact", "normalized"):
        error_message = "Cannot store a confirmed duplicate invoice."

        print("[Storage Agent] Rejected:", error_message)

        return {
            "status": "duplicate",
            "errors": [error_message],
        }

    if duplicate_type == "potential":
        error_message = "Potential duplicate requires manual review."

        print("[Storage Agent] Rejected:", error_message)

        return {
            "status": "manual_review",
            "errors": [error_message],
        }

    if not duplicate_result or duplicate_result.get("is_duplicate", False):
        error_message = "Duplicate detection must be completed before storage."

        print("[Storage Agent] Rejected:", error_message)

        return {
            "status": "failed",
            "errors": [error_message],
        }

    # Step 3: Get extracted invoice data
    raw_invoice_data = state.get("invoice_data")

    if not raw_invoice_data:
        error_message = "No invoice data available for storage."

        print("[Storage Agent] Error:", error_message)

        return {
            "status": "failed",
            "errors": [error_message],
        }

    db = SessionLocal()

    try:
        # Step 4: Validate data using Pydantic
        invoice_data = InvoiceData.model_validate(raw_invoice_data)

        # Step 5: Store invoice in SQLite
        saved_invoice = create_invoice(
            db=db,
            invoice_data=invoice_data,
        )

        invoice_id = saved_invoice.id

        print("[Storage Agent] Invoice stored successfully.")
        print("Invoice ID:", invoice_id)

        return {
            "invoice_id": invoice_id,
            "status": "stored",
            "errors": [],
        }

    except Exception as exc:
        db.rollback()

        error_message = f"Invoice storage failed: {str(exc)}"

        print("[Storage Agent] Error:", error_message)

        return {
            "status": "failed",
            "errors": [error_message],
        }

    finally:
        db.close()
