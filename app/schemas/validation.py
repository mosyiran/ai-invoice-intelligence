
from pydantic import BaseModel


class FinancialValidationResult(BaseModel):

    is_valid: bool

    errors: list[str] = []

    warnings: list[str] = []

    calculated_total: str | None = None

    difference: str | None = None
