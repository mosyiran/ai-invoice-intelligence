
from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class InvoiceData(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    invoice_number: str | None = Field(
        default=None,
        description="Invoice identification number"
    )

    invoice_date: date | None = Field(
        default=None
    )

    due_date: date | None = Field(
        default=None
    )

    supplier_name: str | None = Field(
        default=None
    )

    supplier_tax_id: str | None = Field(
        default=None
    )

    customer_name: str | None = Field(
        default=None
    )

    currency: str | None = Field(
        default=None
    )

    subtotal: float | None = Field(
        default=None,
        ge=0
    )

    vat: float | None = Field(
        default=None,
        ge=0
    )

    total: float | None = Field(
        default=None,
        ge=0
    )
