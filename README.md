# Work projects

Technical operations projects by Haley Maes: payment exceptions, disbursement drills, and reusable investigation patterns.

All data in this repository is synthetic.

## Open the site

From this folder:

```bash
python3 -m http.server
```

Then open http://localhost:8000/

GitHub Pages: https://haleymykellemaes-beep.github.io/work-projects/

## Run the projects

From the repo root. Python 3 standard library only. No packages to install.

### Payment exceptions

```bash
python3 payment-exceptions/python/seed.py
python3 payment-exceptions/python/investigate.py
python3 payment-exceptions/python/reprocess_plan.py
```

### Choice ops

```bash
python3 choice-ops/python/seed.py
python3 choice-ops/python/investigate_failure.py
python3 choice-ops/python/investigate_failure.py DSP-7001
python3 choice-ops/python/reprocess.py
python3 choice-ops/python/reconcile_batch.py
python3 choice-ops/python/classify_webhook.py
```

### Patterns

```bash
python3 patterns/investigate/python/run.py
python3 patterns/repair/python/run.py
python3 patterns/reconcile/python/run.py
python3 patterns/classify/python/run.py
python3 patterns/variance/python/run.py
```

`python3 patterns/repair/python/run.py --execute` writes a plan row and does not create a payment.
