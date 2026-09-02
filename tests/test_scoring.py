import pytest

from datetime import date 
from decimal import Decimal
from uuid import uuid4

from app.domain.models import Invoice, BankTransaction
from app.matching.scoring import calculate_match_score

def test_exact_match_score_is_one():
    invoice = Invoice(
        id=uuid4(),
        supplier_name="ABC",
        invoice_number="INV-1",
        invoice_date=date(2026, 7, 1),
        amount=Decimal("1250.00"),
        currency="TJS",
    )

    transaction = BankTransaction(
        id=uuid4(),
        transaction_date=date(2026, 7, 1),
        description="ABC PAYMENT",
        amount=Decimal("-1250.00"),
        currency="TJS",
    )

    score = calculate_match_score(
        invoice=invoice,
        transaction=transaction,
    )

    assert score == pytest.approx(1.0)

def test_seven_day_difference_reduces_score():
    invoice = Invoice(
        id=uuid4(),
        supplier_name="ABC",
        invoice_number="INV-1",
        invoice_date=date(2026, 7, 1),
        amount=Decimal("1250.00"),
        currency="TJS",
    )

    transaction = BankTransaction(
        id=uuid4(),
        transaction_date=date(2026, 7, 8),
        description="ABC PAYMENT",
        amount=Decimal("-1250.00"),
        currency="TJS",
    )

    score = calculate_match_score(
        invoice=invoice,
        transaction=transaction,
    )

    assert score == pytest.approx(0.85)