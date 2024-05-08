import datetime, zipfile, gzip, os

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
    'Ark: Survival Evolved': r'ServerGame.\d+.\d{4}.\d{2}.\d{2}_\d+.\d+.\d+\d+.log'
}

# Create new folder if not exists
def mkdir(folder_dir):
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)

def minecraft_logs_sorting(log):
    # Remove the '-' from the log
    date_part, number_part = log.split('-')[:3], log.split('-')[3]
    # Join the parts of date to transform
    date_log = '-'.join(date_part)
    # Remove the '.log' extension and pass the number to int
    number_log = int(number_part.split('.')[0])
    # Return the date and number for sorting
    return date_log, number_log

def ark_logs_sorting(log):
    # Extract date and time parts from filename
    date_str, time_str = log.split('_')[0].split('.')[2:5], log.split('_')[1].split('.')[:3]
    # Combine date and time strings into a single timestamp string
    timestamp_str = f"{'-'.join(date_str)}_{':'.join(time_str)}"
    # Convert timestamp string to datetime object
    return datetime.datetime.strptime(timestamp_str, "%Y-%m-%d_%H:%M:%S")

# Sort a list of logs names
def sort_list_logs(egg, logs):
    # Use the logs_modifications function to sort the logs by date and number
    if len(logs)>1 and egg in eggs_minecraft:
        sorted_logs = sorted(logs, key=minecraft_logs_sorting)
    elif len(logs)>1 and egg in eggs_ark:
        sorted_logs = sorted(logs, key=ark_logs_sorting)
    else:
        sorted_logs = logs
    return sorted_logs

def get_timestamp_log_names(egg, list_log_names):
    if egg in eggs_minecraft:
        timestamp_logs = [datetime.datetime.strptime(item[:10], "%Y-%m-%d") for item in list_log_names]
    elif egg in eggs_ark:
        timestamp_logs = [ark_logs_sorting(item) for item in list_log_names]
    return timestamp_logs

# Get last index from a list when matching with an element
def last_index(timestamp_list, timestamp):

    # Making sure that both timestamp are in the same timezone for comparision
    timestamp = timestamp.replace(tzinfo=datetime.timezone.utc)
    timestamp_list = [ts.replace(tzinfo=datetime.timezone.utc) for ts in timestamp_list]

    for ts in timestamp_list:
        # Exact match
        if ts == timestamp:
            closest_timestamp = ts
            break

        # Match only date
        if ts.date() == timestamp.date():
            closest_timestamp = ts
            break

    # If no exact match or matching date, find the closest timestamp in the past
    closest_timestamp = min((ts for ts in timestamp_list if ts < timestamp), key=lambda x: timestamp - x, default=None)
    if closest_timestamp is None:
        return 0
    else:
        return timestamp_list.index(closest_timestamp)


# Extract the compressed files (.gz and .zip)    
def extract_compressed_file(compressed_file_path, decompressed_folder_path):
    if compressed_file_path.endswith('.gz'):
        with gzip.open(compressed_file_path, 'rb') as compressed_file:
            with open(decompressed_folder_path, 'wb') as decompressed_file:
                decompressed_file.write(compressed_file.read())
    elif compressed_file_path.endswith('.zip'):
        with zipfile.ZipFile(compressed_file_path, 'r') as zip_file:
            zip_file.extractall(os.path.dirname(decompressed_folder_path))