from app.domain.models import Invoice, BankTransaction

def calculate_match_score(invoice: Invoice, transaction: BankTransaction, *, maximum_date_difference_days: int = 14) -> float:
    date_difference = (
        transaction.transaction_date - invoice.invoice_date).days

    if date_difference < 0:
        return 0.0

    if transaction.currency != invoice.currency:
        return 0.0

    amount_score = (
        1.0 if abs(transaction.amount) == invoice.amount else 0.0
    )

    currency_score = 1.0

    data_score = max(
        0.0,
        1 - (date_difference / maximum_date_difference_days)
    )

    score = (
        amount_score * 0.50 + currency_score * 0.20 + data_score * 0.30
    )

    return score