--
MERGE INTO tuya.energy_devices AS d
USING {{ df_1 }} AS s
ON d.device_uid = s.device_uid
WHEN MATCHED THEN
    UPDATE SET
        name = s._name
WHEN NOT MATCHED THEN
  INSERT (device_uid, name)
  VALUES (s.device_uid, s._name);

--
INSERT INTO tuya.energy_consumption
SELECT
    d.id AS device_id,
    s._power,
    s._timestamp
FROM {{ df_1 }} AS s
LEFT JOIN tuya.energy_devices AS d
    ON s.device_uid = d.device_uid;

--
DROP TABLE {{ df_1 }}