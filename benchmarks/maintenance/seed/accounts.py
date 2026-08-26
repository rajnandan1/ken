"""Account balances for ledgerd."""

balances = {}  # account id -> integer cents


def _debit(acct, cents):
    """Take `cents` out of acct."""
    balances[acct] = balances.get(acct, 0) - cents


def deposit(acct, cents):
    balances[acct] = balances.get(acct, 0) + cents


def transfer(src, dst, cents):
    """Move `cents` from src to dst."""
    _debit(src, cents)
    deposit(dst, cents)


def withdraw(acct, cents):
    """Take `cents` out of acct as cash."""
    _debit(acct, cents)
    return cents


def clear():
    balances.clear()
