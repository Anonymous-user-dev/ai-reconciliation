from app.domain.models import Invoice, BankTransaction
from app.matching.baseline import supplier_similarity

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

    date_score = max(
        0.0,
        1 - (date_difference / maximum_date_difference_days)
    )
    supplier_score = supplier_similarity(invoice.supplier_name, transaction.description)



    score = (
        amount_score * 0.40 + currency_score * 0.15 + date_score * 0.25 + supplier_score * 0.20
    )

    return score