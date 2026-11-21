
from app.agents.state import InvoiceState


def extraction_agent(state: InvoiceState) -> dict:
    """
    Extract and prepare structured invoice data.

    In this version, extraction is simulated using
    structured input data. Later, an LLM or OCR
    service can be connected here.
    """

    print("\n[Extraction Agent] Started")

    raw_data = state.get("raw_invoice_data")

    if not raw_data:
        error_message = "No invoice data provided."

        print(f"[Extraction Agent] Error: {error_message}")

        return {
            "status": "failed",
            "errors": [error_message],
        }

    try:
        # Prepare a copy of the input data
        extracted_data = dict(raw_data)

        print("[Extraction Agent] Invoice data prepared.")

        return {
            "invoice_data": extracted_data,
            "status": "extracted",
            "errors": [],
        }

    except Exception as exc:
        error_message = f"Extraction failed: {str(exc)}"

        print(f"[Extraction Agent] Error: {error_message}")

        return {
            "status": "failed",
            "errors": [error_message],
        }
