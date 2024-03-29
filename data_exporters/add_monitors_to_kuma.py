from mage_ai.data_preparation.shared.secrets import get_secret_value
from uptime_kuma_api import UptimeKumaApi, MonitorType

@data_exporter
def export_data(nodes, servers, *args, **kwargs):

    kuma_url = get_secret_value('kuma_url')
    kuma_user = get_secret_value('kuma_user')
    kuma_pass = get_secret_value('kuma_pass')

    with UptimeKumaApi(kuma_url) as api:

        api.login(kuma_user, kuma_pass)

        #### Creating Monitors for each Node ####

        existing_monitors = api.get_monitors()
        monitor_name = 'Nodes'

        # Check if the monitor_name already exists
        if any(monitor_name == monitor.get('name') for monitor in existing_monitors):
            print(f"The monitor group '{monitor_name}' already exists.")
        else:
            # Create the monitor group if it doesn't exist
            api.add_monitor(
                type=MonitorType.GROUP,
                name=monitor_name,
            )

        # Looking for the 'Nodes' group id
        monitor_group = 'Nodes'
        existing_monitors = api.get_monitors()

        # Find the monitor with the specified name and type
        target_monitor = next(
            (monitor for monitor in existing_monitors if monitor.get('name') == monitor_group and monitor.get('type') == MonitorType.GROUP.value),
            None
        )

        # Transform the id from int to str
        monitor_id = target_monitor.get('id')
        monitor_id = str(monitor_id)

        # Transform DataFrame to a list of tuples
        nodes = [tuple(x) for x in nodes.to_records(index=False)]

        # Modify the nodes dictionary creation
        nodes_dict = {f'{node_id} | {node_name}': f'http://{node_fqdn}' for node_id, node_name, node_fqdn in nodes}

        for node_name, node_url in nodes_dict.items():
            monitor_exists = any(monitor['name'] == node_name for monitor in existing_monitors)
            if not monitor_exists:
                api.add_monitor(
                    type=MonitorType.HTTP,
                    name=node_name,
                    url=node_url,
                    accepted_statuscodes=['401'],
                    parent=monitor_id
                )

        #### Creating Monitors for each Server ####

        # Create a nested dictionary
        nested_dict = {}
        # Transform DataFrame to a list of tuples
        servers = [tuple(x) for x in servers.to_records(index=False)]

        for server_info in servers:
            server_name, server_identifier, server_egg, server_node, server_port = server_info

            # Create a dictionary for each server
            server_dict = {
                'identifier': server_identifier,
                'egg': server_egg,
                'node': server_node,
                'port': server_port
            }

            # Add the server dictionary to the nested dictionary with the server name as the key
            nested_dict[server_name] = server_dict

        # Determine the game and add a monitor for each server in filtered_servers
        for server_name, server_info in nested_dict.items():
            server_identifier = server_info['identifier']
            server_egg = server_info['egg']
            server_node = server_info['node']
            server_port = server_info['port']

            # Check if the monitor already exists
            #existing_monitors = api.get_monitors()
            #monitor_exists = any(monitor['name'] == server_node for monitor in existing_monitors)

            # Check if server_node has been added
            #if not monitor_exists:
                #api.add_monitor(
                    #type=MonitorType.GROUP,
                    #name=server_info['node'],
                #)

            # Extract only the first word of 'node' in lowercase
            node_lowercase = server_node.split()[0].lower()

            # Determine the game based on the server egg
            if 'Bedrock' in server_egg:
                game_name = 'minecraftbe'
            else:
                game_name = 'minecraft'

            # Create the host by concatenating the first word with '.stiv.tech'
            host_minecraft = f"{node_lowercase}.stiv.tech"

            port_minecraft = server_port

            # Get the list of monitors
            monitors = api.get_monitors()

            # Process host_minecraft for comparison
            processed_host = host_minecraft.split('.')[0]

            # Iterate through monitors to find a match based on processed host
            for monitor in monitors:
                if monitor['type'] == "<MonitorType.GROUP: 'group'>":  # Skip non-group monitors
                    continue
                
                print(monitor['name']
                    )
                # Process monitor name for comparison
                words = monitor['name'].lower().split(' ')
                if len(words) >= 2:
                    processed_name = words[-1]  # Use [-2] to get the second-to-last word
                    print(processed_name)
                
                    # Check if the processed names are similar
                    if processed_host in processed_name or processed_name in processed_host:
                        parent_id = monitor['id']
                        break  # Stop iterating once a match is found

            # Check if the monitor already exists
            existing_monitors = api.get_monitors()
            monitor_exists = any(monitor['name'] == server_identifier + ' | ' + server_name for monitor in existing_monitors)

            # Add the monitor only if it doesn't exist
            if not monitor_exists:
                api.add_monitor(
                    type=MonitorType.GAMEDIG,
                    name=server_identifier + ' | ' + server_name,
                    hostname=host_minecraft,
                    port=int(port_minecraft),
                    game=game_name,
                    parent= parent_id
                    )