-- Docs: https://docs.mage.ai/guides/sql-blocks
WITH CTE_upsert AS (
  INSERT INTO shlink.shorturls (shortCode, shortUrl, longUrl, dateCreated, tags, title, total, nonBots, bots)
  SELECT shortCode, shortUrl, longUrl, dateCreated, tags, title, total, nonBots, bots
  FROM {{ df_1 }} as d
  WHERE NOT EXISTS (
    SELECT 1
    FROM shlink.shorturls as su
    WHERE su.shortCode = d.shortCode
  )
  RETURNING shortCode
)
SELECT COUNT(*) AS rows_inserted
FROM CTE_upsert;