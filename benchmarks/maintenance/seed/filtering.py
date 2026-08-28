"""Filter operators for ledgerd queries.

The one place operator names live: the CLI's `filter` command and any future
query surface share these tables, so a new operator lands everywhere at once.
Text matching is case-insensitive by design ("exact" included) — exports and
user input disagree on casing constantly.
"""

COMPARE_OPS = {
    "eq": lambda a, b: a == b,
    "ne": lambda a, b: a != b,
    "lt": lambda a, b: a < b,
    "lte": lambda a, b: a <= b,
    "gt": lambda a, b: a > b,
    "gte": lambda a, b: a >= b,
}

TEXT_OPS = {
    "contains": lambda a, b: b.lower() in a.lower(),
    "startswith": lambda a, b: a.lower().startswith(b.lower()),
    "exact": lambda a, b: a.lower() == b.lower(),
}


def apply_op(op, left, right):
    """Apply a supported operator to two values; unknown op raises ValueError."""
    if op in COMPARE_OPS:
        return COMPARE_OPS[op](left, right)
    if op in TEXT_OPS:
        return TEXT_OPS[op](str(left), str(right))
    raise ValueError(f"unsupported op: {op}")
