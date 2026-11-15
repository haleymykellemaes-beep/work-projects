#!/usr/bin/env python3
"""Map a code to an action label. No live side effect."""

from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERY = (ROOT / "sql" / "query.sql").read_text()

CODE_MAP = [
    ("96", "retry"),
    ("91", "retry"),
    ("R01", "wait"),
    ("R03", "fix_data"),
    ("settled", "do_not_retry"),
]
EVENTS = [
    ("WH-1", "96", "retry"),
    ("WH-2", "91", "retry"),
    ("WH-3", "R01", "wait"),
    ("WH-4", "R03", "fix_data"),
    ("WH-5", "settled", "do_not_retry"),
    ("WH-6", "XX", "escalate"),
]


def main() -> int:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE code_map (code TEXT PRIMARY KEY, action TEXT)")
    conn.executemany("INSERT INTO code_map VALUES (?, ?)", CODE_MAP)

    print(f"{'Event':<8} {'Code':<10} Action")
    for event_id, code, expected in EVENTS:
        action = conn.execute(QUERY, {"code": code}).fetchone()["action"]
        print(f"{event_id:<8} {code:<10} {action}")
        if action != expected:
            print(f"{event_id} labeled {action}; expected {expected}")
            return 1

    print("Labels only. Nothing was sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
