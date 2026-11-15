# Variance

Question: which business total is outside tolerance, and by how many dollars?

Inputs: three lines. Collections and fees are already dollars. Hours are 40 expected and 36 actual, priced at $45 an hour so the gap prints in dollars. Tolerance is $50 on collections, $25 on fees, and $45 on hours (one hour).

| Line | Expected | Actual | Tolerance |
| --- | ---: | ---: | ---: |
| Collections | $12,400.00 | $12,110.00 | $50.00 |
| Fees | $860.00 | $860.00 | $25.00 |
| Hours | $1,800.00 | $1,620.00 | $45.00 |

Control: `sql/query.sql` subtracts expected from actual and flags a row when the absolute gap is larger than the tolerance. The script prints the dollars. It does not post an adjustment.

## Run

From the repo root:

```bash
python3 patterns/variance/python/run.py
```
