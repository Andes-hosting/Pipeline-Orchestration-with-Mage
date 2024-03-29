import pandas as pd
from uptime_kuma_api import UptimeKumaApi, MonitorType
from mage_ai.data_preparation.shared.secrets import get_secret_value

@transformer
def transform(data, *args, **kwargs):

    kuma_url = get_secret_value('kuma_url')
    kuma_user = get_secret_value('kuma_user')
    kuma_pass = get_secret_value('kuma_pass')

    # Connect to Kuma
    with UptimeKumaApi(kuma_url) as api:
        api.login(kuma_user, kuma_pass)

        # Create the Nodes group
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

        result_nodes = data
        # Transform DataFrame to a list of tuples
        result_nodes = [tuple(x) for x in result_nodes.to_records(index=False)]

        # Modify the result_nodes dictionary creation
        result_nodes_dict = {f'{node_id} | {node_name}': f'http://{node_fqdn}' for node_id, node_name, node_fqdn in result_nodes}
        result_nodes_dict

        for server_name, server_url in result_nodes_dict.items():
            monitor_exists = any(monitor['name'] == server_name for monitor in existing_monitors)
            if not monitor_exists:
                api.add_monitor(
                    type=MonitorType.HTTP,
                    name=server_name,
                    url=server_url,
                    accepted_statuscodes=['401'],
                    parent=monitor_id
                )
    return None