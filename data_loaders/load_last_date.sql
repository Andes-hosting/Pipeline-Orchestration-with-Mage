-- Docs: https://docs.mage.ai/guides/sql-blocks
SELECT servers.uuid FROM pterodactyl.servers  WHERE servers.is_active = true