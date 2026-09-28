from decimal import Decimal


FRAUD_AMOUNT_THRESHOLD = Decimal("100000")

def is_fraud_by_rules(amount: Decimal) -> bool:
    return amount > FRAUD_AMOUNT_THRESHOLD




# def scoring_fraud_rate():
