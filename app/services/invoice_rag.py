
from sqlalchemy import select

from qdrant_client import models

from app.db.database import SessionLocal
from app.models.invoice import Invoice

from app.services.qdrant_store import (
    client,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    initialize_collection,
)


def invoice_to_document(invoice: Invoice) -> str:

    return f"""
    Invoice number: {invoice.invoice_number or "Unknown"}.
    Invoice date: {invoice.invoice_date or "Unknown"}.
    Due date: {invoice.due_date or "Unknown"}.
    Supplier: {invoice.supplier_name or "Unknown"}.
    Supplier tax ID: {invoice.supplier_tax_id or "Unknown"}.
    Customer: {invoice.customer_name or "Unknown"}.
    Currency: {invoice.currency or "Unknown"}.
    Subtotal: {invoice.subtotal if invoice.subtotal is not None else "Unknown"}.
    VAT: {invoice.vat if invoice.vat is not None else "Unknown"}.
    Total: {invoice.total if invoice.total is not None else "Unknown"}.
    """


def index_all_invoices():

    """
    Read invoices from SQLite and index them in Qdrant.
    """

    initialize_collection()

    db = SessionLocal()

    try:

        statement = select(Invoice).order_by(Invoice.id)

        invoices = db.scalars(statement).all()

        if not invoices:
            print("No invoices found in SQLite.")
            return 0

        documents = []
        payloads = []
        ids = []

        for invoice in invoices:

            document = invoice_to_document(invoice)

            documents.append(
                models.Document(
                    text=document,
                    model=EMBEDDING_MODEL,
                )
            )

            payloads.append({
                "document": document,
                "invoice_id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "supplier_name": invoice.supplier_name,
                "supplier_tax_id": invoice.supplier_tax_id,
                "currency": invoice.currency,
                "total": (
                    str(invoice.total)
                    if invoice.total is not None
                    else None
                ),
            })

            ids.append(invoice.id)

        # Upload documents and generate embeddings
        client.upload_collection(
            collection_name=COLLECTION_NAME,
            vectors=documents,
            payload=payloads,
            ids=ids,
        )

        print(f"Indexed {len(invoices)} invoices.")

        return len(invoices)

    finally:
        db.close()


def search_invoices(
    query: str,
    limit: int = 5,
):

    """
    Search invoices using semantic similarity.
    """

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if limit < 1:
        raise ValueError("Limit must be at least 1.")

    initialize_collection()

    response = client.query_points(
        collection_name=COLLECTION_NAME,

        query=models.Document(
            text=query,
            model=EMBEDDING_MODEL,
        ),

        limit=limit,

        with_payload=True,
    )

    search_results = []

    for point in response.points:

        payload = point.payload or {}

        search_results.append({

            "score": point.score,

            "document": payload.get("document"),

            "metadata": {
                "invoice_id": payload.get("invoice_id"),
                "invoice_number": payload.get("invoice_number"),
                "supplier_name": payload.get("supplier_name"),
                "supplier_tax_id": payload.get("supplier_tax_id"),
                "currency": payload.get("currency"),
                "total": payload.get("total"),
            },

        })

    return search_results
