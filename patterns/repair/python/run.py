#!/usr/bin/env python3
"""Dry-run by default. Refuse a settled idempotency key. --execute writes a plan row only."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERY = (ROOT / "sql" / "query.sql").read_text()

ATTEMPTS = [
    ("ATT-11", "KEY-OPEN", 41000, "failed"),
    ("ATT-12", "KEY-SETTLED", 180000, "failed"),
]
POSTED = [("PAY-9", "KEY-SETTLED", 180000, "settled")]


def money(cents: int) -> str:
    return f"${cents // 100:,}.{cents % 100:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan a retry. Dry-run unless --execute.")
    parser.add_argument("--execute", action="store_true", help="Insert a plan row. Does not create a payment.")
    args = parser.parse_args()

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE attempts (
          attempt_id TEXT PRIMARY KEY,
          idempotency_key TEXT,
          amount_cents INTEGER,
          status TEXT
        );
        CREATE TABLE posted (
          payment_id TEXT PRIMARY KEY,
          idempotency_key TEXT,
          amount_cents INTEGER,
          status TEXT
        );
        CREATE TABLE reprocess_plan (
          attempt_id TEXT PRIMARY KEY,
          idempotency_key TEXT,
          amount_cents INTEGER,
          status TEXT
        );
        """
    )
    conn.executemany("INSERT INTO attempts VALUES (?, ?, ?, ?)", ATTEMPTS)
    conn.executemany("INSERT INTO posted VALUES (?, ?, ?, ?)", POSTED)

    payments_before = conn.execute("SELECT COUNT(*) FROM posted").fetchone()[0]
    print("mode: execute" if args.execute else "mode: dry run")

    decisions = {}
    inserted = 0
    for row in conn.execute(QUERY):
        if row["key_settled"]:
            decision = "refuse"
            detail = "idempotency key already settled"
        else:
            decision = "plan"
            detail = "key is not posted"
        decisions[row["attempt_id"]] = decision
        print(f"{decision:<8} {row['attempt_id']}  {row['idempotency_key']:<12} {money(row['amount_cents']):>10}  {detail}")
        if args.execute and decision == "plan":
            conn.execute(
                "INSERT INTO reprocess_plan (attempt_id, idempotency_key, amount_cents, status) VALUES (?, ?, ?, 'planned')",
                (row["attempt_id"], row["idempotency_key"], row["amount_cents"]),
            )
            inserted += 1

    payments_after = conn.execute("SELECT COUNT(*) FROM posted").fetchone()[0]
    planned = conn.execute("SELECT COUNT(*) FROM reprocess_plan").fetchone()[0]
    print(f"plan rows written: {planned}")
    print(f"posted payments before {payments_before}, after {payments_after}")

    if decisions != {"ATT-11": "plan", "ATT-12": "refuse"}:
        return 1
    if payments_before != payments_after:
        return 1
    if args.execute and inserted != 1:
        return 1
    if not args.execute and planned != 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
