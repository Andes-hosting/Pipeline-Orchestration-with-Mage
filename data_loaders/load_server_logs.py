from mage_ai.data_preparation.shared.secrets import get_secret_value
from Andes.utils.ptero_logs import mkdir, sort_list_logs, get_timestamp_log_names, extract_compressed_file, last_index
from Andes.utils.ptero_logs import all_eggs, folder_logs, log_pattern
from pydactyl import PterodactylClient
from datetime import datetime
import urllib, os, re
import pandas as pd

@data_loader
def load_data(data, *args, **kwargs):

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

    # Create a staging folder to store the logs files
    project_path = os.environ.get('USER_CODE_PATH')
    logs_path = os.path.join(project_path, 'staging_area', 'pterodactyl_logs')
    mkdir(logs_path)

    compression_ext = ('.gz', '.zip')

    for server_info in data.iterrows():

        id = server_info[1]['id']
        identifier = server_info[1]['identifier']
        egg = server_info[1]['egg']
        last_log = server_info[1]['last_date']

        # Convert id to a string
        id_str = str(id)

        if egg in all_eggs:
            # Create a folder as staging area for each server
            folder_server_dir = os.path.join(logs_path, id_str)
            mkdir(folder_server_dir)

            # Get the last log date to download only necessary logs
            last_log_date = last_log

            # Get a list of the logs inside the server
            try:
                log_files = api_cli.client.servers.files.list_files(identifier, folder_logs[egg])
                log_files_data = log_files.get('data', [])
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404 or e.response.status_code == 504:
                    print(f"Server {identifier} not found in Pterodactyl.")
                    return None # Skip this and continue to the next iteration

            # If log_files_data is not empty, sort the list of logs based on the date naming
            if log_files_data:
                list_logs = [file['attributes']['name'] for file in log_files_data if re.match(log_pattern[egg], file['attributes']['name'])]
                sorted_list_logs = sort_list_logs(egg, list_logs)
                sorted_list_logs_timestamp = get_timestamp_log_names(egg, sorted_list_logs)
            else:
                print(f"No log files found in server {identifier} with the client API.")

            # Select only a list of downloadable_logs which are new; after the last_log_date
            index_last_log = last_index(sorted_list_logs_timestamp, last_log_date)
            downloadable_logs = sorted_list_logs[index_last_log:]

            # Download all logs in the list downloadable_logs
            list_download = [api_cli.client.servers.files.download_file(identifier, f'/{folder_logs[egg]}/{log}') for log in downloadable_logs]
            if list_download:
                [urllib.request.urlretrieve(list_download[i], os.path.join(folder_server_dir, list_logs[i])) for i in range(len(list_download))]
            print(f'Files downloaded: {len(list_download)}')

            # Uncompressing files if needed
            for filename in os.listdir(folder_server_dir):
                if filename.endswith(compression_ext):
                    compressed_file_path = os.path.join(folder_server_dir, filename)
                    decompressed_file_path = os.path.splitext(compressed_file_path)[0]  # Remove the last extension

                    # Uncompress the file
                    extract_compressed_file(compressed_file_path, decompressed_file_path)

                    # Delete the compressed file
                    os.remove(compressed_file_path)

    return logs_path