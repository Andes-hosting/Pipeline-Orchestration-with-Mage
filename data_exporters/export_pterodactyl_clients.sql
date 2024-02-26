WITH CTE_upsert(id)
AS (
  INSERT INTO pterodactyl.clients (id, uuid, client_name, email, first_name, last_name, admin, "2fa", created_at, updated_at, is_active, deleted_at)
  SELECT id, uuid, client_name, email, first_name, last_name, _admin, letter_2fa, created_at, updated_at, TRUE, NULL
  FROM {{ df_1 }}
  ON CONFLICT (id) DO
    UPDATE SET
      uuid = excluded.uuid,
      client_name = excluded.client_name,
      email = excluded.email,
      first_name = excluded.first_name,
      last_name = excluded.last_name,
      admin = excluded.admin,
      "2fa" = excluded."2fa",
      created_at = excluded.created_at,
      updated_at = excluded.updated_at   
RETURNING id
)
UPDATE pterodactyl.clients AS c
SET 
  is_active = FALSE,
  deleted_at = '{{ execution_date }}'
FROM {{ df_1 }}
WHERE c.id NOT IN (SELECT id FROM CTE_upsert);

DROP TABLE {{ df_1 }};