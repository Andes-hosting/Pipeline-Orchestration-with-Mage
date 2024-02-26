WITH CTE_upsert(id)
AS (
  INSERT INTO pterodactyl.allocations (id, node_id, port, assigned, is_active)
  SELECT id, node_id, port, assigned, TRUE
  FROM {{ df_1 }}
  ON CONFLICT (id) DO
    UPDATE SET
      node_id = excluded.node_id,
      port = excluded.port,
      assigned = excluded.assigned 
RETURNING id
)
UPDATE pterodactyl.allocations AS a
SET 
  is_active = FALSE
FROM {{ df_1 }}
WHERE a.id NOT IN (SELECT id FROM CTE_upsert);

DROP TABLE {{ df_1 }};