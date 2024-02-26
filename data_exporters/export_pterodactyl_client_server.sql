WITH CTE_upsert(id)
AS (
  INSERT INTO pterodactyl.client_server (id, client_id, server_id, created_at, updated_at, is_active, deleted_at)
  SELECT id, client_id, server_id, created_at, updated_at, TRUE, NULL
  FROM {{ df_1 }}
  ON CONFLICT (id) DO
    UPDATE SET
      client_id = excluded.client_id,
      server_id = excluded.server_id,
      created_at = excluded.created_at,
      updated_at = excluded.updated_at
RETURNING id
)
UPDATE pterodactyl.client_server AS cs
SET 
  is_active = FALSE,
  deleted_at = '{{ execution_date }}'
FROM {{ df_1 }}
WHERE cs.id NOT IN (SELECT id FROM CTE_upsert);

DROP TABLE {{ df_1 }};