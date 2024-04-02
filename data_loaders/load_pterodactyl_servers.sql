SELECT
	servers.name AS "servers_names",
	servers.id AS "servers_id",
	eggs.name AS "eggs_names",
    nodes.name AS "nodes_names",
	allocations.port AS "port"
FROM pterodactyl.servers
INNER JOIN pterodactyl.eggs
	ON servers.egg_id = eggs.id
INNER JOIN pterodactyl.nodes
	ON servers.node_id = nodes.id
INNER JOIN pterodactyl.allocations
	ON allocations.id = servers.allocation_id
GROUP BY servers.id, servers.name, eggs.name, nodes.name, allocations.port
HAVING servers.is_active = true
ORDER BY servers.id