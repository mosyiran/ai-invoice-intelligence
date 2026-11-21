
from app.agents.state import InvoiceState
from app.schemas.invoice import InvoiceData
from app.services.financial_validator import validate_invoice


def validation_agent(state: InvoiceState) -> dict:
    """
    Validate invoice structure and financial calculations.
    """

    print("\n[Validation Agent] Started")

    invoice_data = state.get("invoice_data")

    if not invoice_data:
        error_message = "No extracted invoice data available."

        return {
            "status": "failed",
            "validation_result": {
                "is_valid": False,
                "errors": [error_message],
                "warnings": [],
            },
            "errors": [error_message],
        }

    try:
        # Step 1: Pydantic validation
        invoice = InvoiceData.model_validate(invoice_data)

        # Step 2: Financial validation
        validation = validate_invoice(invoice)

        # Convert Pydantic result to dictionary
        validation_result = validation.model_dump(mode="json")

        print("[Validation Agent] Validation completed.")
        print("Valid:", validation.is_valid)

        if validation.errors:
            print("Errors:", validation.errors)

        if validation.warnings:
            print("Warnings:", validation.warnings)

        return {
            "invoice_data": invoice.model_dump(mode="json"),
            "validation_result": validation_result,
            "status": (
                "validated"
                if validation.is_valid
                else "invalid"
            ),
            "errors": validation.errors,
        }

    except Exception as exc:

        error_message = f"Validation failed: {str(exc)}"

        print("[Validation Agent] Error:", error_message)

        return {
            "status": "failed",
            "validation_result": {
                "is_valid": False,
                "errors": [error_message],
                "warnings": [],
            },
            "errors": [error_message],
        }
