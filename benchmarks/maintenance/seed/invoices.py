"""Invoice store for ledgerd. In-memory; the CLI wires persistence."""
from parsing import parse_amount

_invoices = {}  # id -> {"title": str, "items": [(name, amount_str, qty)], "seconds": int}


def add_invoice(inv_id, title):
    _invoices[inv_id] = {"title": title, "items": [], "seconds": 0}


def add_item(inv_id, name, amount_str, qty=1):
    _invoices[inv_id]["items"].append((name, amount_str, qty))


def log_seconds(inv_id, seconds):
    _invoices[inv_id]["seconds"] += seconds


def get_invoice(inv_id):
    return _invoices[inv_id]


def all_invoices():
    return dict(_invoices)


def invoice_total(inv_id):
    """Total of an invoice in cents."""
    return sum(parse_amount(a) * q for _, a, q in _invoices[inv_id]["items"])


def clear():
    _invoices.clear()
