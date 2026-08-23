from app.domain.models import Invoice, BankTransaction, MatchCandidate

def find_candidate_matches(invoices: list[Invoice], transactions: list[BankTransaction], *, maximum_date_difference_days: int = 14) -> list[MatchCandidate]:
    candidates = []

    for transaction in transactions:
        for invoice in invoices:
            date_difference = (
                transaction.transaction_date - invoice.invoice_date
            ).days
            amount_matches = abs(transaction.amount) == invoice.amount
            currency_matches = transaction.currency == invoice.currency
            date_matches = (
                0 <= date_difference <= maximum_date_difference_days
            )

            if amount_matches and currency_matches and date_matches:
                candidate = MatchCandidate(
                    invoice_id=invoice.id,
                    transaction_id=transaction.id,
                    amount_matches=True,
                    currency_matches=True,
                    date_difference_days=date_difference,
                    reasons=[
                        "Absolute amounts are equal",
                        "Currencies are equal",
                        f"Transaction occurred {date_difference} days after invoice",
                    ]
                )

                candidates.append(candidate)
                
    return candidates

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

    assert len(result) == 1
