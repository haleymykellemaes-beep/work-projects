#!/usr/bin/env python3
"""Expected versus actual. Flag rows outside tolerance and print the dollars."""

from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERY = (ROOT / "sql" / "query.sql").read_text()

# line, expected cents, actual cents, tolerance cents.
# Hours are 40 vs 36 at $45, so both sides are already dollars.
TOTALS = [
    ("collections", 1240000, 1211000, 5000),
    ("fees", 86000, 86000, 2500),
    ("hours", 180000, 162000, 4500),
]


def money(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100:,}.{cents % 100:02d}"


def main() -> int:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE totals (
          line TEXT PRIMARY KEY,
          expected_cents INTEGER,
          actual_cents INTEGER,
          tolerance_cents INTEGER
        )
        """
    )
    conn.executemany("INSERT INTO totals VALUES (?, ?, ?, ?)", TOTALS)

    print(f"{'Line':<14} {'Expected':>12} {'Actual':>12} {'Variance':>12}  Flag")
    flagged = []
    flagged_cents = 0
    for row in conn.execute(QUERY):
        mark = "FLAG" if row["flagged"] else ""
        print(
            f"{row['line']:<14} {money(row['expected_cents']):>12} "
            f"{money(row['actual_cents']):>12} {money(row['variance_cents']):>12}  {mark}"
        )
        if row["flagged"]:
            flagged.append(row["line"])
            flagged_cents += row["variance_cents"]

    print(f"Flagged dollars: {money(flagged_cents)}")
    if flagged != ["collections", "hours"]:
        return 1
    if flagged_cents != -47000:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
