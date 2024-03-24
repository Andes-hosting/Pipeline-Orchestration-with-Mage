from uptime_kuma_api import UptimeKumaApi, MonitorType
from mage_ai.data_preparation.shared.secrets import get_secret_value

@transformer
def transform(result_servers, *args, **kwargs):

    kuma_url = get_secret_value('kuma_url')
    kuma_user = get_secret_value('kuma_user')
    kuma_pass = get_secret_value('kuma_pass')

    with UptimeKumaApi(kuma_url) as api:

        api.login(kuma_user, kuma_pass)

        # Create a nested dictionary
        nested_dict = {}
        # Transform DataFrame to a list of tuples
        result_servers = [tuple(x) for x in result_servers.to_records(index=False)]

        for server_info in result_servers:
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
        return None