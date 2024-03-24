-- CREATE SCHEMA 
CREATE SCHEMA pterodactyl;

-- TABLES FOR PTERODACTYL LOGS ACTIVITY
CREATE TABLE pterodactyl.activity (
	server_id int8 NOT NULL REFERENCES pterodactyl.servers(id),
	"timestamp" timestamptz NOT NULL,
	information text NOT NULL,
	"user" text NOT NULL,
	activity text NOT NULL
);