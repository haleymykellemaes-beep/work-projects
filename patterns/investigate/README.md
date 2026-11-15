# Investigate

Question: for this one id, does the ledger match the event log?

Inputs: one entity, `PAY-1042`. A ledger row (system of record) and two log lines.

Control: `sql/query.sql` returns the timeline. The script states the mismatch in one sentence. It does not update either side.

Synthetic. The ledger says failed. The last webhook says settled.

## Run

From the repo root:

```bash
python3 patterns/investigate/python/run.py
```
