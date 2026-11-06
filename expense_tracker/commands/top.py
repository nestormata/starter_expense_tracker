"""The ``top`` command: show the largest expenses."""

from __future__ import annotations

import argparse

from ..money import format_amount

NAME = "top"
HELP = "Show the largest expenses"


def _positive_int(value: str) -> int:
    limit = int(value)
    if limit < 1:
        raise argparse.ArgumentTypeError("limit must be a positive integer")
    return limit


def add_parser(subparsers) -> None:
    parser = subparsers.add_parser(NAME, help=HELP)
    parser.add_argument(
        "--limit",
        type=_positive_int,
        default=3,
        help="Number of expenses to show (default: 3)",
    )


def handle(args, store) -> int:
    expenses = sorted(
        store.load(),
        key=lambda expense: expense.amount_cents,
        reverse=True,
    )[: args.limit]

    if not expenses:
        print("No expenses found.")
        return 0

    for expense in expenses:
        note = f"  ({expense.note})" if expense.note else ""
        print(
            f"#{expense.id}  {expense.date}  "
            f"{format_amount(expense.amount_cents):>10}  "
            f"{expense.category}{note}"
        )
    return 0