

from pydantic import BaseModel, Field


class FinancialValidationResult(BaseModel):

    is_valid: bool

    errors: list[str] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)

    calculated_total: str | None = None

    difference: str | None = None
