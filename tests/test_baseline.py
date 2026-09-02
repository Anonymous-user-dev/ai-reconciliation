from app.matching.baseline import find_candidate_matches
from datetime import date
from decimal import Decimal
from uuid import uuid4
from app.domain.models import BankTransaction, Invoice
import pytest

@pytest.fixture
def invoice():
    return Invoice(
        id=uuid4(),
        supplier_name="ABC",
        invoice_number="2e123",
        invoice_date=date(2026,7,1),
        amount=Decimal("1250.00"),
        currency="TJS"
    )

@pytest.fixture
def transaction():
        return BankTransaction(
        id=uuid4(),
        transaction_date=date(2026, 7, 4),
        description="Some",
        amount=Decimal("-1250.00"),
        currency="TJS"
        )


def test_match(invoice, transaction):


    result = find_candidate_matches(
        invoices=[invoice],
        transactions=[transaction],
    )

    assert len(result) == 1
    candidate = result[0]

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

def test_currency_mismatch_returns_no_candidate():
    invoice = Invoice(
        id=uuid4(),
        supplier_name="ABC",
        invoice_number="2e123",
        invoice_date=date(2026, 7, 1),
        amount=Decimal("1250.00"),
        currency="USD",
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
        transactions=[transaction]
    )

    assert len(result) == 0

def test_transaction_before_invoice_returns_no_candidate():
    invoice = Invoice(
        id=uuid4(),
        supplier_name="ABC",
        invoice_number="2e123",
        invoice_date=date(2026, 7, 1),
        amount=Decimal("1250.00"),
        currency="USD",
    )
    transaction = BankTransaction(
        id=uuid4(),
        transaction_date=date(2026, 5, 4),
        description="Some",
        amount=Decimal("-1250.00"),
        currency="USD",
    )

    result = find_candidate_matches(
        invoices=[invoice],
        transactions=[transaction]
    )

    assert len(result) == 0

def test_multiple_matching_invoices_return_multiple_candidates():
    invoice_1 = Invoice(
        id=uuid4(),
        supplier_name="ABC",
        invoice_number="2e123",
        invoice_date=date(2026, 7, 1),
        amount=Decimal("1250.00"),
        currency="USD",
    )
    invoice_2 = Invoice(    
        id=uuid4(),
        supplier_name="ABCDE",
        invoice_number="2e123d",
        invoice_date=date(2026, 7, 1),
        amount=Decimal("1250.00"),
        currency="USD",
    )

    transaction = BankTransaction(
        id=uuid4(),
        transaction_date=date(2026, 7, 8),
        description="Some",
        amount=Decimal("-1250.00"),
        currency="USD",
    )

    result = find_candidate_matches(
        invoices=[invoice_1, invoice_2],
        transactions=[transaction]
    )

    assert len(result) == 2

def test_transaction_outside_date_window_returns_no_candidate():
    invoice = Invoice(
        id=uuid4(),
        supplier_name="ABC",
        invoice_number="2e123",
        invoice_date=date(2026, 7, 1),
        amount=Decimal("1250.00"),
        currency="USD",
    )

    transaction = BankTransaction(
        id=uuid4(),
        transaction_date=date(2026, 7, 20),
        description="Some",
        amount=Decimal("-1250.00"),
        currency="USD",
    )

    result = find_candidate_matches(
        invoices=[invoice],
        transactions=[transaction]
    )

    assert len(result) == 0

def test_custom_date_window_allows_match():
    invoice = Invoice(
        id=uuid4(),
        supplier_name="ABC",
        invoice_number="2e123",
        invoice_date=date(2026, 7, 1),
        amount=Decimal("1250.00"),
        currency="USD",
    )

    transaction = BankTransaction(
        id=uuid4(),
        transaction_date=date(2026, 7, 20),
        description="Some",
        amount=Decimal("-1250.00"),
        currency="USD",
    )

    result = find_candidate_matches(
        invoices=[invoice],
        transactions=[transaction],
        maximum_date_difference_days=19
    )

    assert len(result) == 1

