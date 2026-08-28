"""Baseline suite: green at seed, and expected to stay green all run."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from filtering import apply_op
from money import format_money
from parsing import parse_amount
from textutils import slugify, truncate
import accounts
import csvio
import duration
import invoices

assert format_money(1050) == "$10.50"
assert format_money(123456) == "$1,234.56"

assert slugify("Hello, World!") == "hello-world"
assert truncate("short") == "short"

assert parse_amount("$10.50") == 1050
assert parse_amount("$0.99") == 99

assert apply_op("gte", 500, 500)
assert apply_op("ne", 3, 4)
assert apply_op("exact", "Website Build", "website build")
try:
    apply_op("regex", "a", "b")
    raise SystemExit("unknown op must raise ValueError")
except ValueError:
    pass

invoices.clear()
invoices.add_invoice("inv-1", "Website build")
invoices.add_item("inv-1", "design", "$100.00", 2)
invoices.add_item("inv-1", "hosting", "$9.99")
assert invoices.invoice_total("inv-1") == 20999

accounts.clear()
accounts.deposit("alice", 1000)
accounts.transfer("alice", "bob", 600)
assert accounts.balances == {"alice": 400, "bob": 600}
assert accounts.withdraw("bob", 100) == 100
assert accounts.balances["bob"] == 500

assert duration.parse_duration("1h30m") == 5400
assert duration.parse_duration("2H5S") == 7205
assert duration.parse_duration("1.5h") == 5400

fd, path = tempfile.mkstemp(suffix=".csv")
os.close(fd)
with open(path, "w") as f:
    f.write("title,amount\nWebsite build,$100.00\nHosting,$9.99\n\n")
rows = csvio.import_rows(path)
os.unlink(path)
assert rows == [("Website build", "$100.00"), ("Hosting", "$9.99")]

print("seed OK")
