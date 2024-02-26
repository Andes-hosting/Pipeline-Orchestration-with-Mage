-- CREATE SCHEMA 
CREATE SCHEMA shlink;

-- TABLES FOR SHLINK DATA

CREATE TABLE shlink.shorturls (
	id serial4 NOT NULL PRIMARY KEY,
	shortcode text NOT NULL UNIQUE,
	shorturl text NOT NULL,
	longurl text NOT NULL,
	datecreated timestamptz NOT NULL,
	tags _text NULL,
	title text NULL,
    visitsCount int4 NULL,
    maxvisits int4 NULL,
    validsince timestamptz NULL,
    validuntil timestamptz NULL
);