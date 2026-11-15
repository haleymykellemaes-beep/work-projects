# Reconcile

Question: where do the ledger and the batch file fail to tie?

Inputs: left is the settled ledger. Right is the batch file. Five traces.

Control: `sql/query.sql` labels each trace matched, missing left, missing right, amount mismatch, or duplicate key. The script prints the label and the dollars. It does not change either source.

| Trace | Ledger | File | Label |
| --- | ---: | ---: | --- |
| TR-1001 | $100.00 | $100.00 | matched |
| TR-1002 | $200.00 | — | missing right |
| TR-1003 | — | $150.00 | missing left |
| TR-1004 | $300.00 | $280.00 | amount mismatch |
| TR-1005 | $64.00 once | $64.00 twice | duplicate key |

## Run

From the repo root:

```bash
python3 patterns/reconcile/python/run.py
```
