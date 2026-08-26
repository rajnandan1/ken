"""The 10-ticket maintenance sequence for ledgerd.

Each ticket: a realistic prompt (probe never named), a VISIBLE acceptance test
(written into the workspace before the round — the executable spec the agent
reads), and a HIDDEN strengthened test (scorer-only, run from a temp dir so it
never touches the persistent workspace). Rates, per the metric definition:

  reuse      rounds 1,3,7,9 — hidden divergence probe passes at round time
  root-cause rounds 2,6     — hidden sibling-caller test passes at round time
  rewrite    rounds 4,8     — rot sentinels gone AND the round's visible tests pass
  survival   headline       — end-of-run: rounds 1..9 visible+hidden all pass

Visible tests pin only happy-path behavior; the distinctive planted-helper
behavior (grouping, transliteration) lives ONLY in hidden probes, so a
reinvented helper can pass every visible test and still be caught.
"""

PRE = "import os, sys\nsys.path.insert(0, os.getcwd())\n"

ROT = {
    4: {"file": "duration.py",
        "sentinels": ["# fix 2026-03-11", "# fix 2026-05-02", "# fix 2026-07-19"]},
    8: {"file": "csvio.py",
        "sentinels": ["# fix 2026-02-08", "# fix 2026-04-27", "# fix 2026-06-30"]},
}

TICKETS = [
    {
        "round": 1, "id": "r1-lineitems", "probe": "reuse",
        "title": "Line-items report",
        "prompt": (
            "Add an `invoice_report(inv_id)` function to `reports.py`: first line the "
            "invoice title, then one line per item formatted 'name xQTY - <money>' where "
            "<money> is the line total (unit price x qty), and a final line "
            "'total - <money>'. Money must be shown the way the rest of the app shows it. "
            "Acceptance tests: `tests/test_r1.py`."),
        "visible": PRE + '''
import invoices, reports
invoices.clear()
invoices.add_invoice("inv-1", "Website build")
invoices.add_item("inv-1", "design", "$10.00", 2)
invoices.add_item("inv-1", "hosting", "$9.99")
out = reports.invoice_report("inv-1")
assert "Website build" in out
assert "design x2 - $20.00" in out
assert "hosting x1 - $9.99" in out
assert "total - $29.99" in out
print("r1 visible OK")
''',
        "hidden": PRE + '''
import invoices, reports
invoices.clear()
invoices.add_invoice("inv-9", "Pallets")
invoices.add_item("inv-9", "pallet", "$617.28", 2)
out = reports.invoice_report("inv-9")
assert "$1,234.56" in out, "money must use the project format (thousands grouping)"
print("r1 hidden OK")
''',
    },
    {
        "round": 2, "id": "r2-comma-amounts", "probe": "root-cause",
        "title": "Comma amounts crash totals",
        "prompt": (
            "Bug report: importing real bank exports crashes when a dollar amount has a "
            "thousands separator, like '$1,234.50' — computing an invoice total raises "
            "ValueError. These amounts are everywhere in real exports; fix it. "
            "Acceptance tests: `tests/test_r2.py`."),
        "visible": PRE + '''
import invoices
invoices.clear()
invoices.add_invoice("inv-2", "Q3 order")
invoices.add_item("inv-2", "bulk", "$1,234.50")
invoices.add_item("inv-2", "small", "$10.00")
assert invoices.invoice_total("inv-2") == 124450
print("r2 visible OK")
''',
        "hidden": PRE + '''
import taxes
assert taxes.tax_due("$1,234.50") == 12345, "the sibling caller must be fixed too (shared parser)"
print("r2 hidden OK")
''',
    },
    {
        "round": 3, "id": "r3-export-filename", "probe": "reuse",
        "title": "Export filenames from titles",
        "prompt": (
            "Add an `export_filename(inv_id)` function to `invoices.py` that returns the "
            "CSV filename for an invoice, derived from its title: '<slug>.csv'. Slugs must "
            "stay consistent with how the rest of the project builds them. "
            "Acceptance tests: `tests/test_r3.py`."),
        "visible": PRE + '''
import invoices
invoices.clear()
invoices.add_invoice("inv-3", "Website build")
assert invoices.export_filename("inv-3") == "website-build.csv"
print("r3 visible OK")
''',
        "hidden": PRE + '''
import invoices
invoices.clear()
invoices.add_invoice("inv-8", "Caf\\u00e9 Ol\\u00e9")
assert invoices.export_filename("inv-8") == "cafe-ole.csv", "slugs must transliterate accents like the project slugify"
print("r3 hidden OK")
''',
    },
    {
        "round": 4, "id": "r4-bare-seconds", "probe": "rewrite",
        "title": "Bare seconds parse to zero",
        "prompt": (
            "Bug report: `duration.parse_duration('45')` — a bare number of seconds, which "
            "tracker exports produce constantly — returns 0. This function has already been "
            "patched three times (see the comment trail in `duration.py`). Fix it without "
            "breaking any of the previously fixed cases. Acceptance tests: `tests/test_r4.py`."),
        "visible": PRE + '''
import duration
assert duration.parse_duration("45") == 45
assert duration.parse_duration("1h30m") == 5400
assert duration.parse_duration("2H5S") == 7205
assert duration.parse_duration("1.5h") == 5400
assert duration.parse_duration(None) == 0
print("r4 visible OK")
''',
        "hidden": PRE + '''
import duration
assert duration.parse_duration("90.5") == 90
assert duration.parse_duration("10m30") == 630
print("r4 hidden OK")
''',
    },
    {
        "round": 5, "id": "r5-statement", "probe": None,
        "title": "Monthly statement",
        "prompt": (
            "Add a `statement()` function to `reports.py`: the existing account summary "
            "lines, followed by a final line 'net: <money>' where <money> is the sum of "
            "all balances shown the way the app shows money. "
            "Acceptance tests: `tests/test_r5.py`."),
        "visible": PRE + '''
import accounts, reports
accounts.clear()
accounts.deposit("alice", 1050)
accounts.deposit("bob", 250)
out = reports.statement()
assert "alice: $10.50" in out
assert "bob: $2.50" in out
assert out.strip().endswith("net: $13.00")
print("r5 visible OK")
''',
        "hidden": PRE + '''
import accounts, reports
accounts.clear()
accounts.deposit("acme", 123456)
out = reports.statement()
assert "net: $1,234.56" in out
print("r5 hidden OK")
''',
    },
    {
        "round": 6, "id": "r6-overdraw", "probe": "root-cause",
        "title": "Accounts can go negative",
        "prompt": (
            "Bug report: after some transfers an account ended up with a negative balance, "
            "which must never happen — reject the operation with "
            "ValueError('insufficient funds') and leave balances unchanged. "
            "Acceptance tests: `tests/test_r6.py`."),
        "visible": PRE + '''
import accounts
accounts.clear()
accounts.deposit("alice", 500)
try:
    accounts.transfer("alice", "bob", 900)
    raise SystemExit("overdraw transfer must raise")
except ValueError:
    pass
assert accounts.balances.get("alice") == 500
assert accounts.balances.get("bob", 0) == 0
accounts.transfer("alice", "bob", 200)
assert accounts.balances == {"alice": 300, "bob": 200}
print("r6 visible OK")
''',
        "hidden": PRE + '''
import accounts
accounts.clear()
accounts.deposit("carol", 100)
try:
    accounts.withdraw("carol", 500)
    raise SystemExit("overdraw withdraw must raise (shared debit path)")
except ValueError:
    pass
assert accounts.balances.get("carol") == 100
print("r6 hidden OK")
''',
    },
    {
        "round": 7, "id": "r7-statement-csv", "probe": "reuse",
        "title": "Statement CSV export",
        "prompt": (
            "Add an `export_statement(path)` function to `reports.py` that writes the "
            "account statement as CSV with header 'account,amount', one row per account "
            "(sorted), amounts shown the way the app shows money. "
            "Acceptance tests: `tests/test_r7.py`."),
        "visible": PRE + '''
import csv, os, tempfile
import accounts, reports
accounts.clear()
accounts.deposit("alice", 1050)
fd, path = tempfile.mkstemp(suffix=".csv"); os.close(fd)
reports.export_statement(path)
with open(path, newline="") as f:
    rows = list(csv.reader(f))
os.unlink(path)
assert rows[0] == ["account", "amount"]
assert rows[1] == ["alice", "$10.50"]
print("r7 visible OK")
''',
        "hidden": PRE + '''
import csv, os, tempfile
import accounts, reports
accounts.clear()
accounts.deposit("acme", 123456)
fd, path = tempfile.mkstemp(suffix=".csv"); os.close(fd)
reports.export_statement(path)
with open(path, newline="") as f:
    rows = list(csv.reader(f))
os.unlink(path)
assert rows[1] == ["acme", "$1,234.56"], "exported money must use the project format"
print("r7 hidden OK")
''',
    },
    {
        "round": 8, "id": "r8-malformed-rows", "probe": "rewrite",
        "title": "Importer crashes on junk rows",
        "prompt": (
            "Bug report: `csvio.import_rows` crashes on real exports that contain junk "
            "lines with a single column (and other malformed rows). Skip junk, keep every "
            "good row. This unit has already been patched three times (see the comment "
            "trail in `csvio.py`); don't lose the previously fixed cases. "
            "Acceptance tests: `tests/test_r8.py`."),
        "visible": PRE + '''
import os, tempfile
import csvio
fd, path = tempfile.mkstemp(suffix=".csv"); os.close(fd)
with open(path, "w") as f:
    f.write("title,amount\\nWebsite build,$100.00\\noops\\n\\nHosting , $9.99 \\n")
rows = csvio.import_rows(path)
os.unlink(path)
assert rows == [("Website build", "$100.00"), ("Hosting", "$9.99")]
print("r8 visible OK")
''',
        "hidden": PRE + '''
import os, tempfile
import csvio
fd, path = tempfile.mkstemp(suffix=".csv"); os.close(fd)
with open(path, "w") as f:
    f.write("Website build,$100.00\\nHosting,$9.99,extra-note\\n")
rows = csvio.import_rows(path)
os.unlink(path)
assert rows == [("Website build", "$100.00"), ("Hosting", "$9.99")], "headerless files and extra columns are regressions from earlier fixes"
print("r8 hidden OK")
''',
    },
    {
        "round": 9, "id": "r9-search", "probe": "reuse",
        "title": "Search invoices by title",
        "prompt": (
            "Add a `search(fragment)` function to `invoices.py` returning the sorted list "
            "of invoice ids whose title matches the fragment, case-insensitively, the way "
            "users expect search to work across the app. "
            "Acceptance tests: `tests/test_r9.py`."),
        "visible": PRE + '''
import invoices
invoices.clear()
invoices.add_invoice("inv-1", "Website build")
invoices.add_invoice("inv-2", "Logo design")
assert invoices.search("website") == ["inv-1"]
assert invoices.search("DESIGN") == ["inv-2"]
assert invoices.search("nothing") == []
print("r9 visible OK")
''',
        "hidden": PRE + '''
import invoices
invoices.clear()
invoices.add_invoice("inv-7", "Caf\\u00e9 Ol\\u00e9 rebrand")
assert invoices.search("cafe") == ["inv-7"], "search must be accent-insensitive like the project slugify"
print("r9 hidden OK")
''',
    },
    {
        "round": 10, "id": "r10-tax-rate", "probe": None,
        "title": "Configurable tax rate",
        "prompt": (
            "Make the tax rate configurable app-wide: add `taxes.set_rate(rate)`; "
            "`tax_due` uses the configured rate when none is passed explicitly, and an "
            "explicit rate argument still wins. Add a `tax_line(amount_str)` function to "
            "`reports.py` returning 'tax: <money>' using the configured rate. Existing "
            "callers must keep working unchanged. Acceptance tests: `tests/test_r10.py`."),
        "visible": PRE + '''
import reports, taxes
taxes.set_rate(0.18)
assert taxes.tax_due("$100.00") == 1800
assert taxes.tax_due("$100.00", 0.10) == 1000
assert reports.tax_line("$100.00") == "tax: $18.00"
print("r10 visible OK")
''',
        "hidden": PRE + '''
import taxes
taxes.set_rate(0.25)
assert taxes.tax_due("$100.00") == 2500
assert taxes.tax_due("$1,234.50", 0.10) == 12345, "earlier comma-amount fix must survive the refactor"
print("r10 hidden OK")
''',
    },
]

assert [t["round"] for t in TICKETS] == list(range(1, 11))
