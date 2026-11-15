# Classify

Question: what should a person do with this code, before anyone sends money?

Inputs: a small code map and six sample events.

| Code | Action |
| --- | --- |
| 96 | retry |
| 91 | retry |
| R01 | wait |
| R03 | fix data |
| settled | do not retry |
| anything else | escalate |

Control: `sql/query.sql` looks up the code. A code that is not on the map escalates. The script prints labels only. It does not retry, edit a recipient, or write a payment.

## Run

From the repo root:

```bash
python3 patterns/classify/python/run.py
```
