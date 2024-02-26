WITH CTE_upsert(id)
AS (
  INSERT INTO pterodactyl.eggs (id, uuid, nest_id, name, description, author, created_at, updated_at, is_active, deleted_at)
  SELECT id, uuid, nest_id, _name, description, author, created_at, updated_at, TRUE, NULL
  FROM {{ df_1 }}
  ON CONFLICT (id) DO
    UPDATE SET
      uuid = excluded.uuid,
      nest_id = excluded.nest_id,
      name = excluded.name,
      description = excluded.description,
      author = excluded.author,
      created_at = excluded.created_at,
      updated_at = excluded.updated_at
RETURNING id
)
UPDATE pterodactyl.eggs AS e
SET 
  is_active = FALSE,
  deleted_at = '{{ execution_date }}'
FROM {{ df_1 }}
WHERE e.id NOT IN (SELECT id FROM CTE_upsert);

DROP TABLE {{ df_1 }};