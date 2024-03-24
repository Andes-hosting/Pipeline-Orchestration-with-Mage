import pandas as pd
import datetime

@transformer
def transform(data, *args, **kwargs):

    transformed_data = []

    for entry in data:
        power = entry['status_device']['result'][4]['value'] / 10
        timestamp = datetime.datetime.fromtimestamp(entry['status_device']['t'] / 1000)

        transformed_data.append({'device_uid': entry['device_uid'], 'name': entry['name'], 'power': power, 'timestamp': timestamp})

    df_energy_devices = pd.DataFrame(transformed_data)
    return df_energy_devices