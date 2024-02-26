from mage_ai.data_preparation.shared.secrets import get_secret_value
from Andes.utils.ptero_app import flatten_list
from pydactyl import PterodactylClient
import pandas as pd
import datetime

@data_loader
def load_data(*args, **kwargs):

    # Connecto to Pterodactyl Application API
    api_app = PterodactylClient(
                url = get_secret_value('pterodactyl_url'), 
                api_key = get_secret_value('pterodactyl_application_api_key'), 
                debug=False)
    # Connecto to Pterodactyl Client API
    api_cli = PterodactylClient(
                url = get_secret_value('pterodactyl_url'), 
                api_key = get_secret_value('pterodactyl_client_api_key'), 
                debug=False)

    # Extracting data from Pterodactyl App
    list_of_clients = api_app.user.list_users()
    all_clients = [[client['attributes'] for client in clients]for clients in list_of_clients]

    list_of_locations = api_app.locations.list_locations()
    all_locations = [[location['attributes'] for location in locations]for locations in list_of_locations]

    list_of_nodes = api_app.nodes.list_nodes()
    all_nodes = [[node['attributes']for node in nodes] for nodes in list_of_nodes]

    list_of_nodes_and_allocations = api_app.nodes.list_nodes(includes=['allocations'])
    all_allocations = [[[{'node_id': node['attributes']['id'], **allocations['attributes']} for allocations in node['attributes']['relationships']['allocations']['data']] for node in nodes] for nodes in list_of_nodes_and_allocations][0]

    list_of_nests_and_eggs = api_app.nests.list_nests(includes=['eggs'])
    all_nests = [[nest['attributes'] for nest in nests] for nests in list_of_nests_and_eggs]
    all_eggs = [flatten_list([[eggs['attributes'] for eggs in nests['attributes']['relationships']['eggs']['data']] for nests in list_of_nests_and_eggs])]

    list_of_servers_and_clients = api_app.servers.list_servers(includes=['subusers'])
    all_servers = [[server['attributes'] for server in servers] for servers in list_of_servers_and_clients]
    all_client_server = [[client_server['attributes'] for client_server in servers['attributes']['relationships']['subusers']['data']] for servers in list_of_servers_and_clients]

    return all_clients, all_locations, all_nodes, all_allocations, all_nests, all_eggs, all_servers, all_client_server