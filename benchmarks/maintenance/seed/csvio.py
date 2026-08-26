"""CSV import for ledgerd. Bank/tracker exports arrive as (title, amount) rows."""
import csv


def import_rows(path):
    """Return (title, amount_str) rows from an export CSV."""
    rows = []
    with open(path, newline="") as f:
        r = csv.reader(f)
        header = next(r, None)
        # fix 2026-02-08 (#19): some exports ship without a header row
        if header and header[0].strip().lower() != "title":
            rows.append((header[0], header[1]))
        for line in r:
            # fix 2026-04-27 (#52): Excel exports end with trailing blank lines
            if not line:
                continue
            # fix 2026-06-30 (#66): stray whitespace around every field
            rows.append((line[0].strip(), line[1].strip()))
    return rows
