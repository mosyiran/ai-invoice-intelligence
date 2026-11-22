
from uuid import uuid4

from app.agents.workflow import invoice_workflow
from app.db.database import SessionLocal
from app.models.invoice import Invoice
from app.services.qdrant_store import (
    client,
    COLLECTION_NAME,
    close_qdrant,
)


def test_successful_invoice_workflow():
    print("\nTesting complete Invoice Workflow...")

    # Generate unique identifiers to avoid duplicate test data.
    unique_id = uuid4().hex[:10].upper()

    invoice_data = {
        "invoice_number": f"INV-WORKFLOW-{unique_id}",
        "invoice_date": "2026-11-22",
        "due_date": "2026-12-22",
        "supplier_name": "Workflow Test Company",
        "supplier_tax_id": f"WT-{unique_id}",
        "customer_name": "Test Customer",
        "currency": "USD",
        "subtotal": 1000,
        "vat": 200,
        "total": 1200,
    }

    invoice_id = None

    try:
        # Initial state passed to LangGraph.
        initial_state = {
            "raw_invoice_data": invoice_data,
            "errors": [],
        }

        print("\nStarting LangGraph workflow...")

        # Execute the complete workflow.
        final_state = invoice_workflow.invoke(initial_state)

        print("\nFinal Workflow State:")
        print(final_state)

        # Verify final workflow status.
        assert final_state.get("status") == "indexed", (
            f"Unexpected workflow status: {final_state.get('status')}"
        )

        assert final_state.get("indexed") is True

        invoice_id = final_state.get("invoice_id")
        assert invoice_id is not None, "Invoice ID was not returned."

        print("\nWorkflow execution passed!")
        print("Invoice ID:", invoice_id)

        # Verify invoice was stored in SQLite.
        db = SessionLocal()

        try:
            stored_invoice = db.get(Invoice, invoice_id)

            assert stored_invoice is not None
            assert stored_invoice.invoice_number == invoice_data["invoice_number"]

            print("SQLite verification passed!")

        finally:
            db.close()

        # Verify invoice was indexed in Qdrant.
        points = client.retrieve(
            collection_name=COLLECTION_NAME,
            ids=[invoice_id],
            with_payload=True,
            with_vectors=False,
        )

        assert len(points) == 1, "Invoice was not found in Qdrant."

        assert points[0].payload["invoice_number"] == invoice_data["invoice_number"]

        print("Qdrant verification passed!")
        print("\nAll workflow tests passed!")

    finally:
        # Remove test invoice from SQLite.
        if invoice_id is not None:
            db = SessionLocal()

            try:
                test_invoice = db.get(Invoice, invoice_id)

                if test_invoice is not None:
                    db.delete(test_invoice)
                    db.commit()
                    print("\nTest invoice removed from SQLite.")

            finally:
                db.close()

            # Remove test point from Qdrant.
            if client.collection_exists(COLLECTION_NAME):
                client.delete(
                    collection_name=COLLECTION_NAME,
                    points_selector=[invoice_id],
                )
                print("Test point removed from Qdrant.")

        close_qdrant()
        print("Qdrant client closed.")


if __name__ == "__main__":
    test_successful_invoice_workflow()
