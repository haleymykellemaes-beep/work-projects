-- Flag a business total when actual is outside tolerance of expected.
SELECT
  line,
  expected_cents,
  actual_cents,
  actual_cents - expected_cents AS variance_cents,
  tolerance_cents,
  CASE
    WHEN ABS(actual_cents - expected_cents) > tolerance_cents THEN 1
    ELSE 0
  END AS flagged
FROM totals
ORDER BY line;
