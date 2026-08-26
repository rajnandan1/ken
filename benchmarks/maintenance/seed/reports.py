"""Rendered reports for ledgerd. Money is always shown via format_money."""
from accounts import balances
from money import format_money


def account_summary():
    """One line per account: 'alice: $10.50'."""
    lines = [f"{acct}: {format_money(cents)}" for acct, cents in sorted(balances.items())]
    return "\n".join(lines)
