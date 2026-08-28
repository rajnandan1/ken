"""ledgerd command line."""
import argparse

import accounts
import csvio
import duration
import filtering
import invoices
import reports


def main(argv=None):
    p = argparse.ArgumentParser(prog="ledgerd")
    sub = p.add_subparsers(dest="cmd", required=True)

    imp = sub.add_parser("import", help="import invoices from a CSV export")
    imp.add_argument("path")

    log = sub.add_parser("log", help="log time against an invoice")
    log.add_argument("invoice")
    log.add_argument("duration")

    sub.add_parser("summary", help="print the account summary")

    flt = sub.add_parser("filter", help="list invoice ids where FIELD OP VALUE")
    flt.add_argument("field", choices=["title", "total"])
    flt.add_argument("op")
    flt.add_argument("value")

    args = p.parse_args(argv)
    if args.cmd == "import":
        for i, (title, amount) in enumerate(csvio.import_rows(args.path), 1):
            invoices.add_invoice(f"inv-{i}", title)
            invoices.add_item(f"inv-{i}", title, amount)
        print(f"imported {i} invoices")
    elif args.cmd == "log":
        invoices.log_seconds(args.invoice, duration.parse_duration(args.duration))
        print("logged")
    elif args.cmd == "summary":
        print(reports.account_summary())
    elif args.cmd == "filter":
        for inv_id, inv in sorted(invoices.all_invoices().items()):
            left = inv["title"] if args.field == "title" else invoices.invoice_total(inv_id)
            right = args.value if args.field == "title" else int(args.value)
            if filtering.apply_op(args.op, left, right):
                print(inv_id)


if __name__ == "__main__":
    main()
