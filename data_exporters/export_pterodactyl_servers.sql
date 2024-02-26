WITH CTE_upsert(id)
AS (
  INSERT INTO pterodactyl.servers (id, uuid, identifier, client_id, node_id, allocation_id, nest_id, egg_id, name, description, limit_memory, limit_disk, limit_io, limit_cpu, limit_oom_disable, limit_database, limit_allocation, limit_backup, created_at, updated_at, is_active, deleted_at)
  SELECT id, uuid, identifier, client_id, node_id, allocation_id, nest_id, egg_id, _name, description, limit_memory, limit_disk, limit_io, limit_cpu, limit_oom_disable, limit_database, limit_allocation, limit_backup, created_at, updated_at, TRUE, NULL
  FROM {{ df_1 }}
  ON CONFLICT (id) DO
    UPDATE SET
      uuid = excluded.uuid,
      identifier = excluded.identifier,
      client_id = excluded.client_id,
      node_id = excluded.node_id,
      allocation_id = excluded.allocation_id,
      nest_id = excluded.nest_id,
      egg_id = excluded.egg_id,
      name = excluded.name,
      description = excluded.description,
      limit_memory = excluded.limit_memory,
      limit_disk = excluded.limit_disk,
      limit_io = excluded.limit_io,
      limit_cpu = excluded.limit_cpu,
      limit_oom_disable = excluded.limit_oom_disable,
      limit_database = excluded.limit_database,
      limit_allocation = excluded.limit_allocation,
      limit_backup = excluded.limit_backup,
      created_at = excluded.created_at,
      updated_at = excluded.updated_at
RETURNING id
)
UPDATE pterodactyl.servers AS s
SET 
  is_active = FALSE,
  deleted_at = '{{ execution_date }}'
FROM {{ df_1 }}
WHERE s.id NOT IN (SELECT id FROM CTE_upsert);

DROP TABLE {{ df_1 }};