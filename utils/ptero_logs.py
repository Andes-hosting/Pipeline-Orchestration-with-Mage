import zipfile, gzip, os

eggs_minecraft = ('Vanilla Minecraft', 'Forge Minecraft', 'Paper', 'Spigot', 'Mohist')
eggs_ark = ('Ark: Survival Evolved',)
all_eggs = eggs_minecraft + eggs_ark

folder_logs = {
    'Vanilla Minecraft': '/logs/',
    'Forge Minecraft': '/logs/',
    'Paper': '/logs/',
    'Spigot': '/logs/',
    'Mohist': '/logs/',
    'Ark: Survival Evolved': '/ShooterGame/Saved/Logs/'
}

log_pattern = {
    'Vanilla Minecraft': r'^\d{4}-\d{2}-\d{2}-\d.*', # yyyy-mm-dd-n*
    'Forge Minecraft': r'^\d{4}-\d{2}-\d{2}-\d.*',
    'Paper': r'^\d{4}-\d{2}-\d{2}-\d.*',
    'Spigot': r'^\d{4}-\d{2}-\d{2}-\d.*',
    'Mohist': r'^\d{4}-\d{2}-\d{2}-\d.*',
    'Ark: Survival Evolved': r'^\d{4}-\d{2}-\d{2}-\d.*' #ServerGame.316.2023.11.17_19.25.10.log or ShooterGame-backup-2023.11.16-21.13.36.log - not sure 
}

# Create new folder if not exists
def mkdir(folder_dir):
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)


# Sort a list of logs names
def sort_list_logs(logs):
    def logs_modifications(log):
        # remove the '-' from the log
        date_part, number_part = log.split('-')[:3], log.split('-')[3]
        # Join the parts of date to transform
        date_log = '-'.join(date_part)
        # remove the '.log' extension and pass the number to int
        number_log = int(number_part.split('.')[0])
        # return the date and number for sorting
        return date_log, number_log

    # use the logs_modifications function to sort the logs by date and number
    sorted_logs = sorted(logs, key=logs_modifications)
    return sorted_logs


# Get last index from a list when matching with an element
def last_index(list, element):
    try:
        return len(list) - 1 - list[::-1].index(element)
    except ValueError:
        raise ValueError(f"'{element}' not found in the list")


# Extract the compressed files (.gz and .zip)    
def extract_compressed_file(compressed_file_path, decompressed_folder_path):
    if compressed_file_path.endswith('.gz'):
        with gzip.open(compressed_file_path, 'rb') as compressed_file:
            with open(decompressed_folder_path, 'wb') as decompressed_file:
                decompressed_file.write(compressed_file.read())
    elif compressed_file_path.endswith('.zip'):
        with zipfile.ZipFile(compressed_file_path, 'r') as zip_file:
            zip_file.extractall(os.path.dirname(decompressed_folder_path))


def transform_logs(id, path_dir, df_servers):

    eggs_minecraft = ('Vanilla Minecraft', 'Forge Minecraft', 'Paper', 'Spigot', 'Mohist')
    eggs_ark = ('Ark: Survival Evolved',)
    all_eggs = eggs_minecraft + eggs_ark

    # Recognize current egg based on server id (folder name)
    current_egg = df_servers.loc[df_servers['id'] == int(id)]['egg'].item()

    # Check if the egg is available for processing
    if current_egg in all_eggs:

        # Read all logs as one
        log_files = [log for log in os.listdir(path_dir) if log.endswith('.log')]
        log_files = sort_list_logs(log_files)

        if log_files:

            all_logs = ""
            for log_file in log_files:
                with open(os.path.join(path_dir, log_file), 'r', encoding='utf-8') as file:
                    log_contents = file.read().split('\n')
                    log_contents = "\n".join([f'[{log_file[:10]}] ' + line for line in log_contents if line.strip() != ""])
                    all_logs += log_contents + "\n"

            # Transformation for all Minecraft Eggs
            if current_egg in eggs_minecraft:

                # Transform information in meaningful information

                pattern = r'\[(\d{4}-\d{2}-\d{2})\] \[.*?(\d{2}:\d{2}:\d{2}).*?\].*?: (.*)'
                matches = re.findall(pattern, all_logs)

                # Create a list of dictionaries to store the extracted data
                log_data = [{'server_id': id, 'date': match[0], 'time': match[1], 'information': match[2]} for match in matches]
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

    # Return an empty dataframe if the egg is not supported
    else:
        df_logs = pd.DataFrame()

    return df_logs