from Andes.utils.ptero_logs import eggs_minecraft, eggs_ark, all_eggs, folder_logs, log_pattern
from Andes.utils.ptero_logs import sort_list_logs
from datetime import datetime
import pandas as pd
import os, re

@transformer
def transform(logs_path, df_servers, *args, **kwargs):

    df_all_logs = pd.DataFrame(columns=['server_id', 'timestamp', 'information', 'user', 'activity'])

    for folder_server_id in os.listdir(logs_path): 
        folder_server_dir = os.path.join(logs_path, folder_server_id)

        current_egg = df_servers.loc[df_servers['id'] == int(folder_server_id)]['egg'].item()

        # Check if the egg is available for processing
        if current_egg in all_eggs:

            # Read all logs as one
            log_files = [log for log in os.listdir(folder_server_dir) if log.endswith('.log')]
            log_files = sort_list_logs(log_files)

            if log_files:

                all_logs = ""
                for log_file in log_files:
                    with open(os.path.join(folder_server_dir, log_file), 'r', encoding='utf-8') as file:
                        log_contents = file.read().split('\n')
                        log_contents = "\n".join([f'[{log_file[:10]}] ' + line for line in log_contents if line.strip() != ""])
                        all_logs += log_contents + "\n"

                # Transformation for all Minecraft Eggs
                if current_egg in eggs_minecraft:

                    # Transform information in meaningful information
                    pattern = r'\[(\d{4}-\d{2}-\d{2})\] \[.*?(\d{2}:\d{2}:\d{2}).*?\].*?: (.*)'
                    matches = re.findall(pattern, all_logs)

                    # Create a list of dictionaries to store the extracted data
                    log_data = [{'server_id': int(folder_server_id), 'timestamp': datetime.combine(datetime.strptime(match[0], '%Y-%m-%d').date(), datetime.strptime(match[1], '%H:%M:%S').time()), 'information': match[2]} for match in matches]
                    # Create a dataframe of the logs
                    df_logs = pd.DataFrame(log_data)
                    df_logs['user'] = None
                    df_logs['activity'] = None

                    # Add information when server started
                    index=df_logs[df_logs['information'].str.startswith("Starting minecraft server version")].index
                    if not index.empty:
                        df_logs.loc[index, 'user'] = 'server'
                        df_logs.loc[index, 'activity'] = 'start'

                    # Add information when server stopped
                    index=df_logs[df_logs['information'].str.startswith("Stopping the server")].index
                    if not index.empty:
                        df_logs.loc[index, 'user'] = 'server'
                        df_logs.loc[index, 'activity'] = 'stop'

                    # Add information when user login
                    users_logged_in = df_logs['information'].str.extract(r'(\w+)\[.*\] logged in with entity id \d+ at \(.*\)')
                    df_logs.update(users_logged_in.rename(columns={0: 'user'}), overwrite=False)
                    df_logs.loc[users_logged_in.dropna().index, 'activity'] = 'login'

                    # Add information when user logout
                    users_logged_out = df_logs['information'].str.extract(r'(\w+) left the game')
                    df_logs.update(users_logged_out.rename(columns={0: 'user'}), overwrite=False)
                    df_logs.loc[users_logged_out.dropna().index, 'activity'] = 'logout'

                    # Add information when user chat
                    users_chat = df_logs['information'].str.extract(r'<(\w+)> .*')
                    df_logs.update(users_chat.rename(columns={0: 'user'}), overwrite=False)
                    df_logs.loc[users_chat.dropna().index, 'activity'] = 'chat'

                    # Add information when user get an achievement
                    users_achievement = df_logs['information'].str.extract(r'(\w+) has made the advancement')
                    df_logs.update(users_achievement.rename(columns={0: 'user'}), overwrite=False)
                    df_logs.loc[users_achievement.dropna().index, 'activity'] = 'achievement'

                    # Rows with no server/user activity is deleted
                    df_logs = df_logs.dropna(subset=['activity'])

                # Transformation for all Ark Eggs
                elif current_egg in eggs_ark:
                    df_logs = pd.DataFrame()

            # Return an empty dataframe if there are no logs to be processed
            else:
                df_logs = pd.DataFrame()

        # Return an empty dataframe if the egg is not supported
        else:
            df_logs = pd.DataFrame()

    # Save every log in df_all_logs for each iteration
    df_all_logs = pd.concat([df_all_logs, df_logs], ignore_index=True)

    # Delete all logs inside each server folder
    for folder in os.listdir(logs_path):
        folder_server_dir = os.path.join(logs_path, folder)
        [os.remove(os.path.join(folder_server_dir, log)) for log in os.listdir(folder_server_dir) if log.endswith('.log')]

    return df_all_logs