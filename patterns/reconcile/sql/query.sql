-- Left is the ledger. Right is the batch file.
WITH left_src AS (
  SELECT trace, SUM(amount_cents) AS amount_cents, COUNT(*) AS n
  FROM ledger
  GROUP BY trace
),
right_src AS (
  SELECT trace, SUM(amount_cents) AS amount_cents, COUNT(*) AS n
  FROM batch
  GROUP BY trace
),
keys AS (
  SELECT trace FROM left_src
  UNION
  SELECT trace FROM right_src
)
SELECT
  k.trace,
  l.amount_cents AS left_cents,
  r.amount_cents AS right_cents,
  COALESCE(l.n, 0) AS left_n,
  COALESCE(r.n, 0) AS right_n,
  CASE
    WHEN l.trace IS NULL THEN 'missing_left'
    WHEN r.trace IS NULL THEN 'missing_right'
    WHEN COALESCE(l.n, 0) > 1 OR COALESCE(r.n, 0) > 1 THEN 'duplicate_key'
    WHEN l.amount_cents != r.amount_cents THEN 'amount_mismatch'
    ELSE 'matched'
  END AS break
FROM keys k
LEFT JOIN left_src l ON l.trace = k.trace
LEFT JOIN right_src r ON r.trace = k.trace
ORDER BY k.trace;
