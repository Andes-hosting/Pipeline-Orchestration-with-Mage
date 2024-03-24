WITH CTE_last_log_date
AS (
    SELECT
        server_id,
        MAX(date) AS last_date
    FROM pterodactyl.activity
    GROUP BY server_id
)
SELECT
    s.id,
    s.identifier,
    e.name AS egg,
    lld.last_date
FROM pterodactyl.servers AS s
INNER JOIN pterodactyl.eggs AS e
    ON e.id = s.egg_id
LEFT JOIN CTE_last_log_date AS lld
    ON lld.server_id = s.id
WHERE s.is_active = true;