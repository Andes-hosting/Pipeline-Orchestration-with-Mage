SELECT
    nodes.id,
    nodes.name,
    nodes.fqdn
FROM pterodactyl.nodes
ORDER BY nodes.id