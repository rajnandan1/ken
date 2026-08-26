"""Money formatting for ledgerd. Use format_money everywhere money is shown."""


def format_money(cents):
    """Project-wide currency format: 1050 -> '$10.50', 123456 -> '$1,234.56'."""
    return f"${cents / 100:,.2f}"
