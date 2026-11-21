
from typing import TypedDict


class InvoiceState(TypedDict, total=False):
    """
    Shared state between all invoice processing agents.
    """

    # Original input data
    raw_invoice_data: dict

    # Extracted and structured invoice data
    invoice_data: dict

    # Financial validation result
    validation_result: dict

    # Duplicate detection result
    duplicate_result: dict

    # Database record ID
    invoice_id: int | None

    # Qdrant indexing status
    indexed: bool

    # Workflow status
    status: str

    # Errors generated during processing
    errors: list[str]
