# SQL and Python operations toolkit

Each example has the same structure:

1. `README.md` — the question, the inputs, the control, and how to run.
2. `sql/query.sql` — the check.
3. `python/run.py` — load a few synthetic rows, run the check, print a short result, exit 0.

The rows themselves are written in the script.

Python 3 standard library and sqlite only. No packages. No network.

These are practice examples for this portfolio. They are not the dental payment ledger or the disbursement project.

## When I use each one

| Pattern | When |
| --- | --- |
| [investigate](investigate/) | One entity id. The system of record and the event log disagree. I want the timeline and one sentence. |
| [repair](repair/) | A retry might pay twice. Dry run unless the idempotency key is clear. `--execute` writes a plan row only. |
| [reconcile](reconcile/) | Two sources should tie: a ledger and a batch file, or any left and right extract. Report missing left, missing right, amount mismatch, and a duplicate key. |
| [classify](classify/) | A processor code, return code, or webhook needs an action label: retry, do not retry, fix data, wait, or escalate. Nothing is sent. |
| [variance](variance/) | A business total does not tie: collections, fees, or hours. Flag rows outside a tolerance and print the dollars. |

These synthetic examples show how I would investigate failed payments in a technical operations role. Investigation, a safe reprocess, a two-source reconcile, and a code label are the payment checks. Variance is the one I use when the unit is a week, a fee, or a shift rather than a payment id. It compares expected dollars with actual dollars. It does not compute a failure rate.

## Run

From the repo root:

```bash
python3 patterns/investigate/python/run.py
python3 patterns/repair/python/run.py
python3 patterns/reconcile/python/run.py
python3 patterns/classify/python/run.py
python3 patterns/variance/python/run.py
```

All of the rows are synthetic.
