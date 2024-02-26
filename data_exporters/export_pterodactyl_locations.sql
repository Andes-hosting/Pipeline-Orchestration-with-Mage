WITH CTE_upsert(id)
AS (
  INSERT INTO pterodactyl.locations (id, short, long, created_at, updated_at, is_active, deleted_at)
  SELECT id, short, _long, created_at, updated_at, TRUE, NULL
  FROM {{ df_1 }}
  ON CONFLICT (id) DO
    UPDATE SET
      short = excluded.short,
      long = excluded.long,
      created_at = excluded.created_at,
      updated_at = excluded.updated_at   
RETURNING id
)
UPDATE pterodactyl.locations AS l
SET 
  is_active = FALSE,
  deleted_at = '{{ execution_date }}'
FROM {{ df_1 }}
WHERE l.id NOT IN (SELECT id FROM CTE_upsert);

DROP TABLE {{ df_1 }};