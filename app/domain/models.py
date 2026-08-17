from datetime import date
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel

class Invoice(BaseModel):
    id: UUID
    supplier_name: str
    invoice_number: str
    invoice_date: date
    amount: Decimal
    currency: str

class BankTransaction(BaseModel):
    id: UUID
    transaction_date: date
    description: str
    amount: Decimal
    currency: str

class MatchCandidate(BaseModel):
    invoice_id: UUID
    transaction_id: UUID
    amount_matches: bool
    currency_matches: bool
    date_difference_days: int
    reasons: list[str]
    