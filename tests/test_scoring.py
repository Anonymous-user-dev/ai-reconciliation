import pytest

from datetime import date 
from decimal import Decimal
from uuid import uuid4

from app.domain.models import Invoice, BankTransaction
from app.matching.scoring import calculate_match_score
from app.matching.baseline import supplier_similarity

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
        description="ABC",
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
        description="ABC",
        amount=Decimal("-1250.00"),
        currency="TJS",
    )

    score = calculate_match_score(
        invoice=invoice,
        transaction=transaction,
    )

    assert score == pytest.approx(0.875)

def test_identical_supplier_name_similarity_one():
    score = supplier_similarity("Somon Trade LLC",
                                "Somon Trade LLC")
    assert score == pytest.approx(1.0)

def test_different_supplier_name_has_lower_similarity():
    score = supplier_similarity(
        "Somon Trade LLC",
        "Microsoft Corporation",
    )

    assert score < 0.5

def test_supplier_match():
    invoice = Invoice(
        id=uuid4(),
        supplier_name="Somon Trade LLC",
        invoice_number="INV-1",
        invoice_date=date(2026, 7, 1),
        amount=Decimal("1250.00"),
        currency="TJS"
        )

    good_transaction = BankTransaction(
        id=uuid4(),
        transaction_date=date(2026, 7, 1),
        description="Somon Trade LLC",
        amount=Decimal("-1250.00"),
        currency="TJS"
        )
    
    bad_transaction = BankTransaction(
        id=uuid4(),
        transaction_date=date(2026, 7, 1),
        description="Microsoft Corporation",
        amount=Decimal("-1250.00"),
        currency="TJS"
        )

    good_score = calculate_match_score(
        invoice,
        good_transaction
    )

    bad_score = calculate_match_score(
        invoice,
        bad_transaction
    )

    assert good_score > bad_score