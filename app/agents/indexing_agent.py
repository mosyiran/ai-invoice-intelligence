
from app.agents.state import InvoiceState
from app.db.database import SessionLocal
from app.models.invoice import Invoice
from app.services.invoice_rag import index_all_invoices
from app.services.qdrant_store import initialize_collection


def indexing_agent(state: InvoiceState) -> dict:
    print("\n[Indexing Agent] Started")

    # Step 1: Check storage result
    invoice_id = state.get("invoice_id")

    if not invoice_id:
        error_message = "No stored invoice ID available for indexing."

        print("[Indexing Agent] Error:", error_message)

        return {
            "indexed": False,
            "status": "indexing_failed",
            "errors": [error_message],
        }

    # Step 2: Verify invoice exists in SQLite
    db = SessionLocal()

    try:
        invoice = db.get(Invoice, invoice_id)

        if invoice is None:
            error_message = (
                f"Invoice with ID {invoice_id} "
                "does not exist in SQLite."
            )

            print("[Indexing Agent] Error:", error_message)

            return {
                "indexed": False,
                "status": "indexing_failed",
                "errors": [error_message],
            }

    except Exception as exc:
        error_message = f"Database verification failed: {str(exc)}"

        print("[Indexing Agent] Error:", error_message)

        return {
            "indexed": False,
            "status": "indexing_failed",
            "errors": [error_message],
        }

    finally:
        db.close()

    # Step 3: Initialize Qdrant collection
    try:
        initialize_collection()

        # Step 4: Index invoices into Qdrant
        indexed_count = index_all_invoices()

        print("[Indexing Agent] Indexing completed.")
        print("Indexed invoices:", indexed_count)

        return {
            "indexed": True,
            "status": "indexed",
            "errors": [],
        }

    except Exception as exc:
        error_message = f"Qdrant indexing failed: {str(exc)}"

        print("[Indexing Agent] Error:", error_message)

        return {
            "indexed": False,
            "status": "indexing_failed",
            "errors": [error_message],
        }
