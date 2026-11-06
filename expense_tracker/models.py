"""The Expense record and its (de)serialisation."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Expense:
    """A single tracked expense. Amounts are integer cents (see money.py)."""

    id: int
    amount_cents: int
    category: str
    date: str  # ISO 8601, e.g. "2026-01-15"
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Expense:
        return cls(
            id=int(data["id"]),
            amount_cents=int(data["amount_cents"]),
            category=str(data["category"]),
            date=str(data["date"]),
            note=str(data.get("note", "")),
        )
