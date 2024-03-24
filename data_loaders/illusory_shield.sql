WITH CTE_latest_visits
AS (
  SELECT
    short_url_id,
    MAX(date) AS latest_date
  FROM shlink.visits
  GROUP BY short_url_id
)
SELECT
  s.id,
  lv.latest_date
FROM shlink.shorturls AS s
LEFT JOIN CTE_latest_visits AS lv
ON s.id = lv.short_url_id;