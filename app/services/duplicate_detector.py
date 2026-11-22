
import re
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.invoice import Invoice


def normalize_text(value: str | None) -> str:
    """Normalize text for duplicate comparison."""

    if not value:
        return ""

    value = value.strip().casefold()
    value = re.sub(r"\s+", " ", value)

    return value


def normalize_invoice_number(
    invoice_number: str | None
) -> str:
    """Normalize invoice number by removing separators."""

    if not invoice_number:
        return ""

    value = invoice_number.strip().casefold()
    value = re.sub(r"[\s\-_./]", "", value)

    return value


def normalize_tax_id(tax_id: str | None) -> str:
    """Normalize supplier tax ID."""

    if not tax_id:
        return ""

    return re.sub(r"[^a-zA-Z0-9]", "", tax_id).casefold()


def to_decimal(value) -> Decimal | None:
    if value is None:
        return None

    return Decimal(str(value))


def get_candidate_statement(invoice: Invoice):
    """
    Return existing invoices, excluding the current invoice
    when it already has a database ID.
    """

    statement = select(Invoice)

    if invoice.id is not None:
        statement = statement.where(
            Invoice.id != invoice.id
        )

    return statement


def find_exact_duplicate(
    db: Session,
    invoice: Invoice
):
    """
    Find duplicate using normalized invoice number
    and supplier tax ID.
    """

    invoice_number = normalize_invoice_number(
        invoice.invoice_number
    )

    tax_id = normalize_tax_id(
        invoice.supplier_tax_id
    )

    if not invoice_number or not tax_id:
        return None

    statement = get_candidate_statement(invoice).where(
        Invoice.supplier_tax_id.is_not(None),
        Invoice.invoice_number.is_not(None),
    )

    candidates = db.scalars(statement).all()

    for candidate in candidates:
        candidate_number = normalize_invoice_number(
            candidate.invoice_number
        )

        candidate_tax_id = normalize_tax_id(
            candidate.supplier_tax_id
        )

        if (
            invoice_number == candidate_number
            and tax_id == candidate_tax_id
        ):
            return candidate

    return None


def find_normalized_duplicate(
    db: Session,
    invoice: Invoice
):
    """
    Find duplicate using normalized supplier name
    and normalized invoice number.
    """

    invoice_number = normalize_invoice_number(
        invoice.invoice_number
    )

    supplier_name = normalize_text(
        invoice.supplier_name
    )

    if not invoice_number or not supplier_name:
        return None

    statement = get_candidate_statement(invoice)

    candidates = db.scalars(statement).all()

    for candidate in candidates:
        candidate_number = normalize_invoice_number(
            candidate.invoice_number
        )

        candidate_supplier = normalize_text(
            candidate.supplier_name
        )

        if (
            invoice_number == candidate_number
            and supplier_name == candidate_supplier
        ):
            return candidate

    return None


def find_potential_duplicate(
    db: Session,
    invoice: Invoice
):
    """
    Find possible duplicate using:
    supplier + invoice date + total + currency.
    """

    if (
        not invoice.supplier_name
        or not invoice.invoice_date
        or invoice.total is None
        or not invoice.currency
    ):
        return None

    supplier_name = normalize_text(
        invoice.supplier_name
    )

    total = to_decimal(invoice.total)

    currency = invoice.currency.strip().upper()

    statement = get_candidate_statement(invoice).where(
        Invoice.invoice_date == invoice.invoice_date,
        Invoice.currency == currency,
    )

    candidates = db.scalars(statement).all()

    for candidate in candidates:
        candidate_supplier = normalize_text(
            candidate.supplier_name
        )

        candidate_total = to_decimal(
            candidate.total
        )

        if (
            supplier_name == candidate_supplier
            and total == candidate_total
        ):
            return candidate

    return None


def detect_duplicate(
    db: Session,
    invoice: Invoice
) -> dict:
    """
    Detect exact, normalized, or potential duplicates.
    """

    exact = find_exact_duplicate(db, invoice)

    if exact:
        return {
            "is_duplicate": True,
            "duplicate_type": "exact",
            "matched_invoice_id": exact.id,
            "message": "Exact duplicate invoice detected."
        }

    normalized = find_normalized_duplicate(
        db,
        invoice
    )

    if normalized:
        return {
            "is_duplicate": True,
            "duplicate_type": "normalized",
            "matched_invoice_id": normalized.id,
            "message": "Normalized duplicate invoice detected."
        }

    potential = find_potential_duplicate(
        db,
        invoice
    )

    if potential:
        return {
            "is_duplicate": False,
            "duplicate_type": "potential",
            "matched_invoice_id": potential.id,
            "message": "Potential duplicate requires manual review."
        }

    return {
        "is_duplicate": False,
        "duplicate_type": None,
        "matched_invoice_id": None,
        "message": "No duplicate detected."
    }
