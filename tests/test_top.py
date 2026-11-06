import pytest

from expense_tracker import cli
from expense_tracker.commands import add, top
from tests.conftest import args, make_store


def _seed(store):
    add.handle(
        args(amount="10.00", category="food", date="2026-01-01", note=""),
        store,
    )
    add.handle(
        args(amount="40.00", category="travel", date="2026-01-02", note=""),
        store,
    )
    add.handle(
        args(amount="5.00", category="food", date="2026-01-03", note=""),
        store,
    )
    add.handle(
        args(amount="20.00", category="travel", date="2026-01-04", note=""),
        store,
    )


def test_top_defaults_to_three_largest_in_descending_order(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()

    parsed = cli.build_parser().parse_args(["top"])
    code = top.handle(parsed, store)
    output = capsys.readouterr().out

    assert parsed.limit == 3
    assert code == 0
    assert [line.split()[2] for line in output.splitlines()] == [
        "$40.00",
        "$20.00",
        "$10.00",
    ]


def test_top_respects_limit(tmp_path, capsys):
    store = make_store(tmp_path)
    _seed(store)
    capsys.readouterr()

    parsed = cli.build_parser().parse_args(["top", "--limit", "2"])
    code = top.handle(parsed, store)
    output = capsys.readouterr().out

    assert code == 0
    assert [line.split()[2] for line in output.splitlines()] == ["$40.00", "$20.00"]


def test_top_limit_larger_than_expense_count_prints_all(tmp_path, capsys):
    store = make_store(tmp_path)
    add.handle(
        args(amount="5.00", category="food", date="2026-01-01", note=""),
        store,
    )
    capsys.readouterr()

    parsed = cli.build_parser().parse_args(["top", "--limit", "5"])
    code = top.handle(parsed, store)
    output = capsys.readouterr().out

    assert code == 0
    assert len(output.splitlines()) == 1
    assert "$5.00" in output


def test_top_empty_store_prints_no_expenses(tmp_path, capsys):
    store = make_store(tmp_path)

    code = top.handle(cli.build_parser().parse_args(["top"]), store)

    assert code == 0
    assert capsys.readouterr().out == "No expenses found.\n"


def test_top_rejects_nonpositive_limit():
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(["top", "--limit", "0"])