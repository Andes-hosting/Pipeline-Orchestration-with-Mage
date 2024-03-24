INSERT INTO pterodactyl.utilization
SELECT *
FROM {{ df_1 }};

--
DROP TABLE {{ df_1 }}