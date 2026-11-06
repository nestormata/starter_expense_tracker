"""The ``export`` command: write expenses as CSV."""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import TextIO

NAME = "export"
HELP = "Export expenses as CSV"

HEADERS = ["id", "date", "amount", "amount_cents", "category", "note"]


def add_parser(subparsers) -> None:
    parser = subparsers.add_parser(NAME, help=HELP)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Write CSV to this file instead of stdout",
    )


def _format_amount(cents: int) -> str:
    dollars, remainder = divmod(cents, 100)
    return f"{dollars}.{remainder:02d}"


def _write_csv(stream: TextIO, expenses) -> None:
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(HEADERS)
    for expense in expenses:
        writer.writerow(
            [
                expense.id,
                expense.date,
                _format_amount(expense.amount_cents),
                expense.amount_cents,
                expense.category,
                expense.note,
            ]
        )


def handle(args, store) -> int:
    expenses = store.load()
    if args.output is None:
        _write_csv(sys.stdout, expenses)
    else:
        with args.output.open("w", encoding="utf-8", newline="") as output:
            _write_csv(output, expenses)
    return 0