WITH CTE_last_log_date
AS (
    SELECT
        server_id,
        MAX(timestamp) AS last_date
    FROM pterodactyl.activity
    GROUP BY server_id
)
SELECT
    s.id,
    s.identifier,
    e.name AS egg,
    CASE
        WHEN last_date IS NOT NULL
        THEN last_date
        WHEN last_date IS NULL
        THEN '2000-01-01'
    END AS last_date
    
FROM pterodactyl.servers AS s
INNER JOIN pterodactyl.eggs AS e
    ON e.id = s.egg_id
LEFT JOIN CTE_last_log_date AS lld
    ON lld.server_id = s.id
WHERE s.is_active = true;