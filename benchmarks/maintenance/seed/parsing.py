"""Amount parsing for ledgerd. Every dollar string goes through parse_amount."""


def parse_amount(s):
    """Parse a dollar string like '$10.50' into an integer number of cents."""
    return int(round(float(s.replace("$", "")) * 100))
