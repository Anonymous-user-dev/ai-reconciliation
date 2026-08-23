from app.matching.baseline import find_candidate_matches
from datetime import date
from decimal import Decimal
from uuid import uuid4
from app.domain.models import BankTransaction, Invoice

def test_match():
    invoice = Invoice(
        id=uuid4(),
        supplier_name="ABC",
        invoice_number="2e123",
        invoice_date=date(2026, 7, 1),
        amount=Decimal("1250.00"),
        currency="TJS",
    )

    transaction = BankTransaction(
        id=uuid4(),
        transaction_date=date(2026, 7, 4),
        description="Some",
        amount=Decimal("-1250.00"),
        currency="TJS",
    )

    result = find_candidate_matches(
        invoices=[invoice],
        transactions=[transaction],
    )

    candidate = result [0]

    assert candidate.invoice_id == invoice.id
    assert candidate.transaction_id == transaction.id
    assert candidate.amount_matches is True
    assert candidate.currency_matches is True
    assert candidate.date_difference_days == 3

def test_amount_mismatch_returns_no_candidate():
    invoice = Invoice(
        id=uuid4(),
        supplier_name="ABC",
        invoice_number="2e123",
        invoice_date=date(2026, 7, 1),
        amount=Decimal("1250.00"),
        currency="TJS",
    )

    transaction = BankTransaction(
        id=uuid4(),
        transaction_date=date(2026, 7, 4),
        description="Some",
        amount=Decimal("-1200.00"),
        currency="TJS",
    )

    result = find_candidate_matches(
        invoices=[invoice],
        transactions=[transaction]
    )

    assert len(result) == 0