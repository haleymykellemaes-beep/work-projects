-- Timeline for one entity: system of record, then the event log.
SELECT 'ledger' AS source,
       updated_at AS at,
       status,
       'system of record' AS detail
FROM ledger
WHERE entity_id = :entity_id
UNION ALL
SELECT 'event',
       at,
       status,
       event
FROM events
WHERE entity_id = :entity_id
ORDER BY at;
