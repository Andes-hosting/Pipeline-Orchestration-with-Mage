WITH CTE_get_latest_date
AS (
  SELECT
    su.shorturl_id,
    CASE
      WHEN MAX(v.date) IS NULL
        THEN '2000-01-01'
      ELSE MAX(v.date)
    END AS latest_update
  FROM shlink.shorturls AS su
  LEFT JOIN shlink.visits AS v
    ON su.id = v.shorturl_id
  GROUP BY v.shorturl_id
)
INSERT INTO shlink.visits
SELECT * FROM {{ df_1 }}
WHERE ;