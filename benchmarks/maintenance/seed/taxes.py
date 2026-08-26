"""Tax calculation for ledgerd."""
from parsing import parse_amount


def tax_due(amount_str, rate=0.10):
    """Tax owed on a single dollar string, in cents."""
    return int(round(parse_amount(amount_str) * rate))
