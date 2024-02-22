import io, time
import pandas as pd
import requests
import os
from pydactyl import PterodactylClient
from sqlalchemy import create_engine, text
from datetime import datetime
from mage_ai.data_preparation.shared.secrets import get_secret_value

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test




@data_loader
def load_data_from_api(df, *args, **kwargs):
    """
    Template for loading data from API
    """
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
    
    # Setting variables
    WINDOW_EXTRACTION_TIME = 30 # the time window in which it recieves data from the servers [seconds]
    BREAK_TIME = 10 # the time it takes to rest after getting data from all servers [seconds]
    WAITING_TIME = 1 # the time it takes to rest after getting date from each server [seconds]

    # Define the schema and extrat all uuid from every server from postgres
    list_servers = [uuid for uuid, in df] #remove the tuples of uuid from results

    # Extract the data from every uuid in the postgres database
    all_utilizations = []
    start_time = time.time()
    while (time.time() - start_time) < WINDOW_EXTRACTION_TIME:
        print(time.time() - start_time)
        for server in list_servers:
            try:
                consumption = api_cli.client.servers.get_server_utilization(server)
                consumption.update({'identifier': server[:8]})
                all_utilizations.append(consumption)
            except:
                pass
            time.sleep(WAITING_TIME)
        time.sleep(BREAK_TIME)
    print(time.time() - start_time)

    return all_utilizations