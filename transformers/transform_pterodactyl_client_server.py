import pandas as pd

@transformer
def transform(data, *args, **kwargs):

    all_client_server = data[7]

    flattened_client_server = [item for sublist in all_client_server for item in sublist]
    df_client_server = pd.DataFrame(flattened_client_server)[['id', 'user_id', 'server_id', 'created_at', 'updated_at']].rename(columns={'user_id': 'client_id'})

    df_client_server['created_at'] = pd.to_datetime(df_client_server['created_at'])
    df_client_server['updated_at'] = pd.to_datetime(df_client_server['updated_at'])

    return df_client_server