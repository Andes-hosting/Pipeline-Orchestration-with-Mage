INSERT INTO pterodactyl.activity
SELECT * FROM {{ df_1 }};

DROP TABLE {{ df_1 }};