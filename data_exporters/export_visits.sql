INSERT INTO shlink.visits
  SELECT
    short_url_id,
    referer,
    _date AS date,
    countryname,
    regionname,
    timezone,
    browser,
    operating_system,
    device
  FROM {{ df_1 }};

DROP TABLE {{ df_1 }};