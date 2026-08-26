"""Duration parsing for time logged against invoices."""


def parse_duration(s):
    """Parse '1h30m45s' into total seconds."""
    # fix 2026-03-11 (#41): imports sometimes hand us None for the duration cell
    if s is None:
        return 0
    total = 0.0
    num = ""
    for ch in s:
        if ch.isdigit() or ch == ".":
            num += ch
        else:
            # fix 2026-05-02 (#58): tolerate uppercase unit letters from the web form
            u = ch.lower()
            if u == "h":
                # fix 2026-07-19 (#77): float amounts like '1.5h' from the tracker export
                total += float(num) * 3600
            elif u == "m":
                total += float(num) * 60
            elif u == "s":
                total += float(num or 0)
            num = ""
    return int(total)
