INSERT INTO shlink.shorturls (shortcode, shorturl, longurl, dateCreated, tags, title, visitscount, maxvisits, validsince, validuntil)
SELECT shortcode, shorturl, longurl, dateCreated, tags, title, visitscount, maxvisits, validsince, validuntil
FROM {{ df_1 }}
ON CONFLICT (shortcode) DO
  UPDATE SET
    shortUrl = excluded.shortUrl,
    longurl = excluded.longurl,
    dateCreated = excluded.dateCreated,
    tags = excluded.tags,
    title = excluded.title,
    visitscount = excluded.visitscount,
    maxvisits = excluded.maxvisits,
    validsince = excluded.validsince,
    validuntil = excluded.validuntil