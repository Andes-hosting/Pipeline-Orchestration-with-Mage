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

CREATE TABLE shlink.visits (
	short_url_id int4 NOT NULL REFERENCES shlink.shorturls(id),
	referer text NULL,
	date timestamptz NOT NULL,
	countryname text,
	regionname text,
	timezone text,
	browser text NOT NULL,
	operating_system text NOT NULL,
    device text NOT NULL
);