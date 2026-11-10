
from decimal import Decimal, InvalidOperation

from app.schemas.invoice import InvoiceData
from app.schemas.validation import FinancialValidationResult


def to_decimal(value) -> Decimal | None:
    """
    Convert a numeric value to Decimal safely.
    """

    if value is None:
        return None

    try:
        return Decimal(str(value))

    except (InvalidOperation, ValueError, TypeError):
        return None


def validate_invoice(
    invoice: InvoiceData,
    tolerance: Decimal = Decimal("0.01")
) -> FinancialValidationResult:

    errors = []
    warnings = []

    subtotal = to_decimal(invoice.subtotal)
    vat = to_decimal(invoice.vat)
    total = to_decimal(invoice.total)

    # Check missing financial fields
    if subtotal is None:
        warnings.append("Subtotal is missing.")

    if vat is None:
        warnings.append("VAT is missing.")

    if total is None:
        warnings.append("Total is missing.")

    # Cannot calculate total without all values
    if subtotal is None or vat is None or total is None:

        return FinancialValidationResult(
            is_valid=False,
            errors=errors,
            warnings=warnings
        )

    # Check negative values
    if subtotal < 0:
        errors.append("Subtotal cannot be negative.")

    if vat < 0:
        errors.append("VAT cannot be negative.")

    if total < 0:
        errors.append("Total cannot be negative.")

    # Calculate expected total
    calculated_total = subtotal + vat

    # Calculate difference
    difference = abs(calculated_total - total)

    # Check total calculation
    if difference > tolerance:

        errors.append(
            "Invoice total does not match subtotal + VAT."
        )

    return FinancialValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        calculated_total=str(calculated_total),
        difference=str(difference)
    )
