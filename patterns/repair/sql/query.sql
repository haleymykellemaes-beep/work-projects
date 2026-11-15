-- Failed attempts, and whether that idempotency key already settled.
SELECT
  a.attempt_id,
  a.idempotency_key,
  a.amount_cents,
  CASE WHEN EXISTS (
    SELECT 1
    FROM posted p
    WHERE p.idempotency_key = a.idempotency_key
      AND p.status = 'settled'
  ) THEN 1 ELSE 0 END AS key_settled
FROM attempts a
WHERE a.status = 'failed'
ORDER BY a.attempt_id;
