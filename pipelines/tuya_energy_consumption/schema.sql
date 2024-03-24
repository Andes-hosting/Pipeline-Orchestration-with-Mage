-- CREATE SCHEMA 
CREATE SCHEMA tuya;

-- TABLE FOR TUYA ENERGY CONSUMPTION RECORDS

CREATE TABLE tuya.energy_devices (
	id serial4 NOT NULL PRIMARY KEY,
	device_uid text NOT NULL UNIQUE,
	"name" text NOT NULL
);

CREATE TABLE tuya.energy_consumption (
	device_id int4 NOT NULL REFERENCES tuya.energy_devices(id),
	power numeric(6, 1) NOT NULL,
	"timestamp" timestamptz NOT NULL
);