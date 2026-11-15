#!/usr/bin/env python3
"""Two sources. Report missing left, missing right, amount mismatch, and duplicate key."""

from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERY = (ROOT / "sql" / "query.sql").read_text()

LEDGER = [
    ("TR-1001", 10000),
    ("TR-1002", 20000),
    ("TR-1004", 30000),
    ("TR-1005", 6400),
]
BATCH = [
    ("TR-1001", 10000),
    ("TR-1003", 15000),
    ("TR-1004", 28000),
    ("TR-1005", 6400),
    ("TR-1005", 6400),
]
EXPECTED = {
    "TR-1001": "matched",
    "TR-1002": "missing_right",
    "TR-1003": "missing_left",
    "TR-1004": "amount_mismatch",
    "TR-1005": "duplicate_key",
}


def money(cents) -> str:
    if cents is None:
        return "—"
    return f"${cents // 100:,}.{cents % 100:02d}"


def main() -> int:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE ledger (trace TEXT, amount_cents INTEGER);
        CREATE TABLE batch (trace TEXT, amount_cents INTEGER);
        """
    )
    conn.executemany("INSERT INTO ledger VALUES (?, ?)", LEDGER)
    conn.executemany("INSERT INTO batch VALUES (?, ?)", BATCH)

    print(f"{'Trace':<10} {'Ledger':>10} {'File':>10}  Break")
    found = {}
    for row in conn.execute(QUERY):
        found[row["trace"]] = row["break"]
        print(f"{row['trace']:<10} {money(row['left_cents']):>10} {money(row['right_cents']):>10}  {row['break']}")

    if found != EXPECTED:
        print("Reconcile check failed.")
        return 1
    print("Four break types and one match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
