import csv
import io

from expense_tracker.cli import build_parser
from expense_tracker.commands import export
from expense_tracker.models import Expense
from tests.conftest import args, make_store


def _seed(store):
    store.save(
        [
            Expense(
                id=1,
                amount_cents=1250,
                category="food",
                date="2026-01-01",
                note='lunch, "team"',
            ),
            Expense(
                id=2,
                amount_cents=5,
                category="travel",
                date="2026-01-02",
            ),
        ]
    )


def test_export_writes_csv_to_stdout(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)

    code = export.handle(args(output=None), store)
    output = capsys.readouterr().out
    rows = list(csv.reader(io.StringIO(output)))

    assert code == 0
    assert rows == [
        ["id", "date", "amount", "amount_cents", "category", "note"],
        ["1", "2026-01-01", "12.50", "1250", "food", 'lunch, "team"'],
        ["2", "2026-01-02", "0.05", "5", "travel", ""],
    ]


def test_export_writes_csv_to_file(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    output_path = tmp_path / "expenses.csv"

    code = export.handle(args(output=output_path), store)
    output = capsys.readouterr().out

    assert code == 0
    assert output == ""
    assert list(csv.reader(output_path.open(encoding="utf-8", newline=""))) == [
        ["id", "date", "amount", "amount_cents", "category", "note"],
        ["1", "2026-01-01", "12.50", "1250", "food", 'lunch, "team"'],
        ["2", "2026-01-02", "0.05", "5", "travel", ""],
    ]


def test_export_empty_store_writes_header(tmp_path, capsys):
    store = make_store(tmp_path)

    code = export.handle(args(output=None), store)
    rows = list(csv.reader(io.StringIO(capsys.readouterr().out)))

    assert code == 0
    assert rows == [["id", "date", "amount", "amount_cents", "category", "note"]]


def test_export_is_registered_with_cli():
    parsed = build_parser().parse_args(["export", "--output", "expenses.csv"])

    assert parsed.command == "export"
    assert str(parsed.output) == "expenses.csv"