-- Docs: https://docs.mage.ai/guides/sql-blocks
INSERT INTO pterodactyl.utilization
SELECT *
FROM {{ df_1 }};

--
DROP TABLE {{ df_1 }}