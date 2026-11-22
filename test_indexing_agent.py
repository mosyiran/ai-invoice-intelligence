from datetime import date
from uuid import uuid4
from app.services.qdrant_store import close_qdrant

from sqlalchemy import select
from qdrant_client import models

from app.agents.indexing_agent import indexing_agent
from app.db.database import SessionLocal
from app.models.invoice import Invoice
from app.services.qdrant_store import (
    client,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    initialize_collection,
)


def test_successful_indexing():
    print("\nTesting successful invoice indexing...")

    unique_number = f"INV-INDEX-{uuid4().hex[:10].upper()}"

    db = SessionLocal()

    try:
        # Step 1: Create a test invoice in SQLite

        invoice = Invoice(
            invoice_number=unique_number,
            invoice_date=date(2026, 11, 22),
            supplier_name="Indexing Test Company",
            supplier_tax_id=f"IDX-{uuid4().hex[:10].upper()}",
            customer_name="Test Customer",
            currency="USD",
            subtotal=1000,
            vat=200,
            total=1200,
        )

        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        invoice_id = invoice.id

        print("Test invoice created.")
        print("Invoice ID:", invoice_id)

    finally:
        db.close()

    # Step 2: Run Indexing Agent
    state = {
        "invoice_id": invoice_id,
        "status": "stored",
    }

    result = indexing_agent(state)

    print("\nIndexing Result:")
    print(result)

    assert result["indexed"] is True
    assert result["status"] == "indexed"

    # Step 3: Verify that the invoice exists in Qdrant
    initialize_collection()

    response = client.retrieve(
        collection_name=COLLECTION_NAME,
        ids=[invoice_id],
        with_payload=True,
        with_vectors=False,
    )

    assert len(response) == 1

    payload = response[0].payload or {}

    assert payload.get("invoice_id") == invoice_id
    assert payload.get("invoice_number") == unique_number

    print("\nQdrant verification passed!")
    print("Indexed invoice ID:", payload["invoice_id"])
    print("Invoice number:", payload["invoice_number"])

    # Step 4: Test semantic search
    search_response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=models.Document(
            text="Indexing Test Company invoice",
            model=EMBEDDING_MODEL,
        ),
        limit=10,
        with_payload=True,
    )

    found = any(
        (point.payload or {}).get("invoice_id") == invoice_id
        for point in search_response.points
    )

    assert found, "Invoice was not found in semantic search."

    print("Semantic search verification passed!")

    # Step 5: Clean up test data
    db = SessionLocal()

    try:
        test_invoice = db.get(Invoice, invoice_id)

        if test_invoice is not None:
            db.delete(test_invoice)
            db.commit()

    finally:
        db.close()

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=models.PointIdsList(
            points=[invoice_id]
        ),
        wait=True,
    )

    print("Test records cleaned up.")
    print("Successful indexing test passed!")


if __name__ == "__main__":
    try:
        print("Testing Indexing Agent...")

        test_successful_indexing()

        print("\nAll Indexing Agent tests passed!")

    finally:
        close_qdrant()
        print("Qdrant client closed successfully.")
