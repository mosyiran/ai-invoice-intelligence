
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    String,
    Date,
    DateTime,
    Numeric,
    func,
)

from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Invoice(Base):

    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    invoice_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    invoice_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    supplier_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    supplier_tax_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    customer_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    currency: Mapped[str | None] = mapped_column(
        String(3),
        nullable=True
    )

    subtotal: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2),
        nullable=True
    )

    vat: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2),
        nullable=True
    )

    total: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
