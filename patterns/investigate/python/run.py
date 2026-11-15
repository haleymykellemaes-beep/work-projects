#!/usr/bin/env python3
"""One entity: ledger beside the event log. State the mismatch in one sentence."""

from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERY = (ROOT / "sql" / "query.sql").read_text()
ENTITY = "PAY-1042"

LEDGER = [("PAY-1042", "failed", 125000, "2026-11-12T10:05:00Z")]
EVENTS = [
    ("EV-1", "PAY-1042", "2026-11-12T10:00:00Z", "api.submit", "pending", 125000),
    ("EV-2", "PAY-1042", "2026-11-12T10:04:00Z", "webhook.settled", "settled", 125000),
]


def main() -> int:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE ledger (
          entity_id TEXT PRIMARY KEY,
          status TEXT,
          amount_cents INTEGER,
          updated_at TEXT
        );
        CREATE TABLE events (
          event_id TEXT PRIMARY KEY,
          entity_id TEXT,
          at TEXT,
          event TEXT,
          status TEXT,
          amount_cents INTEGER
        );
        """
    )
    conn.executemany("INSERT INTO ledger VALUES (?, ?, ?, ?)", LEDGER)
    conn.executemany("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)", EVENTS)

    rows = list(conn.execute(QUERY, {"entity_id": ENTITY}))
    ledger_status = next(row["status"] for row in rows if row["source"] == "ledger")
    event_status = [row["status"] for row in rows if row["source"] == "event"][-1]

    print(f"Entity {ENTITY}")
    print(f"{'Source':<8} {'At':<22} {'Status':<10} Detail")
    for row in rows:
        print(f"{row['source']:<8} {row['at']:<22} {row['status']:<10} {row['detail']}")

    if ledger_status == event_status:
        print(f"\n{ENTITY} matches: {ledger_status} on both sides.")
        return 1

    print(f"\n{ENTITY} is {ledger_status} on the ledger and {event_status} in the event log.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
