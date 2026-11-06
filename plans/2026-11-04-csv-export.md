---
title: Add CSV export command
status: Planned
created: 2026-11-04
last_updated: 2026-11-04
type: Feature
scope: CLI
---

# Add CSV Export Command

## Goal

Add an `export` command that outputs the tracked expenses as CSV without
changing how expenses are stored.

## Decisions

- This is an additional command, separate from workshop variants A, B, and C.
- Write CSV to stdout by default; accept `--output PATH` to write to a file.
- Use columns in this order: `id,date,amount,amount_cents,category,note`.
- Format `amount` as a plain decimal (for example, `12.50`) without a currency
  symbol. Keep `amount_cents` as the stored integer value.
- Export every expense in the order returned by storage; do not add filters or
  sorting options in this version.
- Emit the CSV header even when there are no expenses.

## Implementation Plan

0. Use TDD start by creating the tests first, run them red, and then fix them, and repeat.
1. Add `expense_tracker/commands/export.py` with `NAME`, `HELP`, `add_parser`,
   and `handle`, following the existing command-module pattern.
2. Add the command module to `expense_tracker/commands/__init__.py` so the CLI
   registers and dispatches it.
3. Load expenses through `store.load()` and serialize them with Python's
   standard `csv` module. Use integer-safe money formatting for the decimal
   amount; do not use floating-point arithmetic.
4. Add focused tests for stdout output, file output, headers and row values,
   CSV escaping, empty data, and CLI registration.
5. Update the README command table and examples.

## Acceptance Criteria

- `python -m expense_tracker export` writes valid CSV to stdout.
- `python -m expense_tracker export --output PATH` writes the same CSV to the
  requested file.
- The CSV includes all six columns in the specified order, with accurate money
  values and correctly escaped text.
- Empty storage produces a header-only CSV.
- Existing commands and tests continue to work; the full pytest suite passes.
- README usage documents the new command.

## Open Questions

None. The destination, schema, amount representation, row ordering, and empty
export behavior are agreed. No category filtering or sorting is planned for
this version.
