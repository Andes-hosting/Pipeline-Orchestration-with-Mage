WITH CTE_upsert(id)
AS (
  INSERT INTO pterodactyl.nodes (id, uuid, location_id, name, description, fqdn, maintenance_mode, memory, disk, allocated_memory, allocated_disk, created_at, updated_at, is_active, deleted_at)
  SELECT id, uuid, location_id, _name, description, fqdn, maintenance_mode, memory, _disk, allocated_memory, allocated_disk, created_at, updated_at, TRUE, NULL
  FROM {{ df_1 }}
  ON CONFLICT (id) DO
    UPDATE SET
      uuid = excluded.uuid,
      location_id = excluded.location_id,
      name = excluded.name,
      description = excluded.description,
      fqdn = excluded.fqdn,
      maintenance_mode = excluded.maintenance_mode,
      memory = excluded.memory,
      disk = excluded.disk,
      allocated_memory = excluded.allocated_memory,
      allocated_disk = excluded.allocated_disk,
      created_at = excluded.created_at,
      updated_at = excluded.updated_at
RETURNING id
)
UPDATE pterodactyl.nodes AS n
SET 
  is_active = FALSE,
  deleted_at = '{{ execution_date }}'
FROM {{ df_1 }}
WHERE n.id NOT IN (SELECT id FROM CTE_upsert);

DROP TABLE {{ df_1 }}