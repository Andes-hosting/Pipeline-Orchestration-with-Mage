import pandas as pd

@transformer
def transform(data, *args, **kwargs):

    all_clients = data[0]

    df_clients = pd.DataFrame(all_clients[0])
    df_clients = df_clients[['id', 'uuid', 'username', 'email', 'first_name', 'last_name', 'root_admin', '2fa', 'created_at', 'updated_at']].rename(columns={'username': 'client_name', 'root_admin': 'admin'})

    df_clients['created_at'] = pd.to_datetime(df_clients['created_at'])
    df_clients['updated_at'] = pd.to_datetime(df_clients['updated_at'])

    return df_clients