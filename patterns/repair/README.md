# Repair

Question: which failed attempt is safe to plan, and which key is already settled?

Inputs: two failed attempts. `KEY-OPEN` has never posted. `KEY-SETTLED` already settled on a payment.

Control: `sql/query.sql` flags a settled key. The script refuses that attempt. Dry run is the default. `--execute` inserts a plan row and does not insert a payment.

## Run

From the repo root:

```bash
python3 patterns/repair/python/run.py
python3 patterns/repair/python/run.py --execute
```
