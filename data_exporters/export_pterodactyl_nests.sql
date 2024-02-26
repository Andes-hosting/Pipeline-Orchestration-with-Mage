WITH CTE_upsert(id)
AS (
  INSERT INTO pterodactyl.nests (id, uuid, name, description, author, created_at, updated_at, is_active, deleted_at)
  SELECT id, uuid, _name, description, author, created_at, updated_at, TRUE, NULL
  FROM {{ df_1 }}
  ON CONFLICT (id) DO
    UPDATE SET
      uuid = excluded.uuid,
      name = excluded.name,
      description = excluded.description,
      author = excluded.author,
      created_at = excluded.created_at,
      updated_at = excluded.updated_at
RETURNING id
)
UPDATE pterodactyl.nests AS n
SET 
  is_active = FALSE,
  deleted_at = '{{ execution_date }}'
FROM {{ df_1 }}
WHERE n.id NOT IN (SELECT id FROM CTE_upsert);

DROP TABLE {{ df_1 }};