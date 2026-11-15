-- Map a processor code to an action. Unknown codes escalate.
SELECT COALESCE(
  (SELECT action FROM code_map WHERE code = :code),
  'escalate'
) AS action;
