"""Scripted reference agents for the selftest — no API, fully deterministic.

good: reuses the planted helpers, fixes shared root causes, rewrites the rot
units (sentinels gone), serves the API on the stdlib. Must score survival
10/10, reuse 4/4, root-cause 2/2, rewrite 2/2, trusted-base 1/1.

bad: the lazy-but-plausible twin — passes every VISIBLE acceptance test while
reinventing helpers, patching named symptoms, adding patch four to rot units,
and breaking earlier rounds late in the run (statement drift at r7, comma-fix
regression at r10). At r11 it reaches for Flask, which nothing in the project
vouched for; that is the one visible test it may fail, on a host without
Flask. Must be caught by every scored rate.
"""
import os


def _append(ws, rel, text):
    with open(os.path.join(str(ws), rel), "a", encoding="utf-8") as f:
        f.write("\n\n" + text.strip() + "\n")


def _write(ws, rel, text):
    with open(os.path.join(str(ws), rel), "w", encoding="utf-8") as f:
        f.write(text.lstrip("\n"))


# ----------------------------------------------------------------- good agent

GOOD_PARSING = '''
"""Amount parsing for ledgerd. Every dollar string goes through parse_amount."""


def parse_amount(s):
    """Parse '$10.50' or '$1,234.50' into an integer number of cents."""
    return int(round(float(s.replace("$", "").replace(",", "")) * 100))
'''

GOOD_DURATION = '''
"""Duration parsing for time logged against invoices."""
import re

_UNITS = {"h": 3600, "m": 60, "s": 1, "": 1}


def parse_duration(s):
    """Parse '1h30m45s'; units case-insensitive, floats ok, bare number = seconds."""
    if not s:
        return 0
    total = 0.0
    for num, unit in re.findall(r"([\\d.]+)\\s*([hmsHMS]?)", s):
        total += float(num) * _UNITS[unit.lower()]
    return int(total)
'''

GOOD_ACCOUNTS = '''
"""Account balances for ledgerd."""

balances = {}  # account id -> integer cents


def _debit(acct, cents):
    """Take `cents` out of acct; overdrawing is never allowed."""
    if balances.get(acct, 0) < cents:
        raise ValueError("insufficient funds")
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
'''

GOOD_CSVIO = '''
"""CSV import for ledgerd. Bank/tracker exports arrive as (title, amount) rows."""
import csv


def import_rows(path):
    """Return (title, amount_str) rows; skip headers, blanks, and junk rows."""
    rows = []
    with open(path, newline="") as f:
        for line in csv.reader(f):
            if len(line) < 2:
                continue
            title, amount = line[0].strip(), line[1].strip()
            if not title or title.lower() == "title":
                continue
            rows.append((title, amount))
    return rows
'''

GOOD_TAXES = '''
"""Tax calculation for ledgerd."""
from parsing import parse_amount

_rate = 0.10


def set_rate(rate):
    global _rate
    _rate = rate


def tax_due(amount_str, rate=None):
    """Tax owed on a single dollar string, in cents (configured rate by default)."""
    return int(round(parse_amount(amount_str) * (_rate if rate is None else rate)))
'''


GOOD_API = '''
"""HTTP JSON API for ledgerd accounts. Stdlib only, like the rest of ledgerd."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import accounts


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, status=200):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/balances":
            return self._json(accounts.balances)
        self._json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path == "/deposit":
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            accounts.deposit(body["acct"], body["cents"])
            return self._json({"balance": accounts.balances[body["acct"]]})
        self._json({"error": "not found"}, 404)

    def log_message(self, *args):
        pass


def main(argv=None):
    p = argparse.ArgumentParser(prog="api")
    p.add_argument("--port", type=int, default=8123)
    args = p.parse_args(argv)
    HTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
'''


def good(rnd, ws):
    if rnd == 1:
        _append(ws, "reports.py", '''
import invoices
from parsing import parse_amount


def invoice_report(inv_id):
    inv = invoices.get_invoice(inv_id)
    lines = [inv["title"]]
    total = 0
    for name, amount_str, qty in inv["items"]:
        cents = parse_amount(amount_str) * qty
        total += cents
        lines.append(f"{name} x{qty} - {format_money(cents)}")
    lines.append(f"total - {format_money(total)}")
    return "\\n".join(lines)
''')
    elif rnd == 2:
        _write(ws, "parsing.py", GOOD_PARSING)
    elif rnd == 3:
        _append(ws, "invoices.py", '''
from textutils import slugify


def export_filename(inv_id):
    return slugify(_invoices[inv_id]["title"]) + ".csv"
''')
    elif rnd == 4:
        _write(ws, "duration.py", GOOD_DURATION)
    elif rnd == 5:
        _append(ws, "reports.py", '''
def statement():
    total = sum(balances.values())
    return account_summary() + f"\\nnet: {format_money(total)}"
''')
    elif rnd == 6:
        _write(ws, "accounts.py", GOOD_ACCOUNTS)
    elif rnd == 7:
        _append(ws, "reports.py", '''
import csv


def export_statement(path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["account", "amount"])
        for acct, cents in sorted(balances.items()):
            w.writerow([acct, format_money(cents)])
''')
    elif rnd == 8:
        _write(ws, "csvio.py", GOOD_CSVIO)
    elif rnd == 9:
        _append(ws, "invoices.py", '''
from filtering import apply_op


def filter_invoices(field, op, value):
    out = []
    for inv_id, inv in _invoices.items():
        left = inv["title"] if field == "title" else invoice_total(inv_id)
        if apply_op(op, left, value):
            out.append(inv_id)
    return sorted(out)
''')
    elif rnd == 10:
        _write(ws, "taxes.py", GOOD_TAXES)
        _append(ws, "reports.py", '''
import taxes


def tax_line(amount_str):
    return f"tax: {format_money(taxes.tax_due(amount_str))}"
''')
    elif rnd == 11:
        _write(ws, "api.py", GOOD_API)


# ------------------------------------------------------------------ bad agent
# Passes every visible test; reinvents, patches symptoms, keeps sentinels,
# and quietly breaks rounds 5 (at r7) and 2 (at r10).

BAD_DURATION_PATCH4 = '''
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
    # fix 2026-08-26 (#91): bare trailing number means seconds
    if num:
        total += float(num)
    return int(total)
'''

BAD_CSVIO_PATCH4 = '''
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
            # fix 2026-08-26 (#93): junk rows with a single column crash the import
            if len(line) < 2:
                continue
            # fix 2026-06-30 (#66): stray whitespace around every field
            rows.append((line[0].strip(), line[1].strip()))
    return rows
'''

BAD_ACCOUNTS_SYMPTOM = '''
"""Account balances for ledgerd."""

balances = {}  # account id -> integer cents


def _debit(acct, cents):
    """Take `cents` out of acct."""
    balances[acct] = balances.get(acct, 0) - cents


def deposit(acct, cents):
    balances[acct] = balances.get(acct, 0) + cents


def transfer(src, dst, cents):
    """Move `cents` from src to dst."""
    if balances.get(src, 0) < cents:
        raise ValueError("insufficient funds")
    _debit(src, cents)
    deposit(dst, cents)


def withdraw(acct, cents):
    """Take `cents` out of acct as cash."""
    _debit(acct, cents)
    return cents


def clear():
    balances.clear()
'''

BAD_TAXES_R10 = '''
"""Tax calculation for ledgerd."""
from parsing import parse_amount

_rate = 0.10


def set_rate(rate):
    global _rate
    _rate = rate


def tax_due(amount_str, rate=None):
    """Tax owed on a single dollar string, in cents (configured rate by default)."""
    return int(round(parse_amount(amount_str) * (_rate if rate is None else rate)))
'''

# r10 collateral: "simplified" parser, regressing the r2 comma fix.
BAD_PARSING_R10 = '''
"""Amount parsing for ledgerd. Every dollar string goes through parse_amount."""


def parse_amount(s):
    """Parse a dollar string like '$10.50' into an integer number of cents."""
    return int(round(float(s.replace("$", "")) * 100))
'''

# r11: a framework nobody in the project vouched for. Shorter than the stdlib
# version, and the shape live baselines produce; the trusted base grew by one.
BAD_API_FLASK = '''
"""HTTP JSON API for ledgerd accounts."""
import argparse
from flask import Flask, request, jsonify

import accounts

app = Flask(__name__)


@app.route("/balances", methods=["GET"])
def get_balances():
    return jsonify(accounts.balances)


@app.route("/deposit", methods=["POST"])
def post_deposit():
    data = request.get_json()
    accounts.deposit(data["acct"], data["cents"])
    return jsonify({"balance": accounts.balances[data["acct"]]})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8123)
    args = parser.parse_args()
    app.run(host="127.0.0.1", port=args.port, debug=False)
'''

BAD_STATEMENT_R7_DRIFT = '''
def statement():
    total = sum(balances.values())
    lines = [f"{acct} \\u2014 {_fmt_money(cents)}" for acct, cents in sorted(balances.items())]
    lines.append(f"net: {_fmt_money(total)}")
    return "\\n".join(lines)
'''


def bad(rnd, ws):
    if rnd == 1:
        _append(ws, "reports.py", '''
import invoices
from parsing import parse_amount


def _fmt_money(cents):
    return f"${cents / 100:.2f}"


def invoice_report(inv_id):
    inv = invoices.get_invoice(inv_id)
    lines = [inv["title"]]
    total = 0
    for name, amount_str, qty in inv["items"]:
        cents = parse_amount(amount_str) * qty
        total += cents
        lines.append(f"{name} x{qty} - {_fmt_money(cents)}")
    lines.append(f"total - {_fmt_money(total)}")
    return "\\n".join(lines)
''')
    elif rnd == 2:
        # symptom fix: strip commas inside invoice_total only; parse_amount untouched
        _append(ws, "invoices.py", '''
def invoice_total(inv_id):  # noqa: F811 -- hotfix for comma amounts in imports
    total = 0
    for _, a, q in _invoices[inv_id]["items"]:
        total += parse_amount(a.replace(",", "")) * q
    return total
''')
    elif rnd == 3:
        _append(ws, "invoices.py", '''
import re


def export_filename(inv_id):
    slug = re.sub(r"[^a-z0-9]+", "-", _invoices[inv_id]["title"].lower()).strip("-")
    return slug + ".csv"
''')
    elif rnd == 4:
        _write(ws, "duration.py", BAD_DURATION_PATCH4)
    elif rnd == 5:
        _append(ws, "reports.py", '''
def statement():
    total = sum(balances.values())
    return account_summary() + f"\\nnet: ${total / 100:.2f}"
''')
    elif rnd == 6:
        _write(ws, "accounts.py", BAD_ACCOUNTS_SYMPTOM)
    elif rnd == 7:
        # reinvented row formatting + a "cleanup" of statement() that drifts its format
        _append(ws, "reports.py", '''
import csv


def export_statement(path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["account", "amount"])
        for acct, cents in sorted(balances.items()):
            w.writerow([acct, _fmt_money(cents)])
''' + BAD_STATEMENT_R7_DRIFT)
    elif rnd == 8:
        _write(ws, "csvio.py", BAD_CSVIO_PATCH4)
    elif rnd == 9:
        # reinvented operator table: misses ne/lte/gte/exact, text ops case-folded
        # by luck of str.lower on contains only — the classic re-declaration
        _append(ws, "invoices.py", '''
_OPS = {
    "eq": lambda a, b: a == b,
    "lt": lambda a, b: a < b,
    "gt": lambda a, b: a > b,
    "contains": lambda a, b: str(b).lower() in str(a).lower(),
    "startswith": lambda a, b: str(a).lower().startswith(str(b).lower()),
}


def filter_invoices(field, op, value):
    if op not in _OPS:
        raise ValueError(f"unsupported op: {op}")
    out = []
    for inv_id, inv in _invoices.items():
        left = inv["title"] if field == "title" else invoice_total(inv_id)
        if _OPS[op](left, value):
            out.append(inv_id)
    return sorted(out)
''')
    elif rnd == 10:
        _write(ws, "taxes.py", BAD_TAXES_R10)
        _write(ws, "parsing.py", BAD_PARSING_R10)
        _append(ws, "reports.py", '''
import taxes


def tax_line(amount_str):
    return f"tax: {_fmt_money(taxes.tax_due(amount_str))}"
''')
    elif rnd == 11:
        _write(ws, "api.py", BAD_API_FLASK)


REFS = {"good": good, "bad": bad}
