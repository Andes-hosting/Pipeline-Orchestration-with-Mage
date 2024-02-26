import pandas as pd

@transformer
def transform(data, *args, **kwargs):

    all_servers = data[6]

    df_servers = pd.DataFrame(all_servers[0])
    df_servers['limit_memory'] = df_servers['limits'].apply(lambda x: x.get('memory', None))
    df_servers['limit_disk'] = df_servers['limits'].apply(lambda x: x.get('disk', None))
    df_servers['limit_io'] = df_servers['limits'].apply(lambda x: x.get('io', None))
    df_servers['limit_cpu'] = df_servers['limits'].apply(lambda x: x.get('cpu', None))
    df_servers['limit_oom_disable'] = df_servers['limits'].apply(lambda x: x.get('oom_disable', None))
    df_servers['limit_database'] = df_servers['feature_limits'].apply(lambda x: x.get('database', None))
    df_servers['limit_allocation'] = df_servers['feature_limits'].apply(lambda x: x.get('allocation', None))
    df_servers['limit_backup'] = df_servers['feature_limits'].apply(lambda x: x.get('backup', None))
    df_servers = df_servers[['id', 'uuid', 'identifier', 'user', 'node', 'allocation', 'nest', 'egg', 'name', 'description', 'limit_memory', 'limit_disk', 'limit_io', 'limit_cpu', 'limit_oom_disable', 'limit_database', 'limit_allocation', 'limit_backup', 'created_at', 'updated_at']].rename(columns={'user': 'client_id', 'node': 'node_id', 'allocation': 'allocation_id', 'nest': 'nest_id', 'egg': 'egg_id'})

    df_servers['limit_oom_disable'] = df_servers['limit_oom_disable'].astype(bool)
    df_servers['limit_database'] = df_servers['limit_database'].fillna(0).astype(int)
    df_servers['limit_allocation'] = df_servers['limit_allocation'].fillna(0).astype(int)
    df_servers['limit_backup'] = df_servers['limit_backup'].fillna(0).astype(int)
    df_servers['created_at'] = pd.to_datetime(df_servers['created_at'])
    df_servers['updated_at'] = pd.to_datetime(df_servers['updated_at'])

    return df_servers