import pandas as pd

@transformer
def transform(data, *args, **kwargs):

    all_nodes = data[2]

    df_nodes = pd.DataFrame(all_nodes[0])
    df_nodes['allocated_memory'] = df_nodes['allocated_resources'].apply(lambda x: x.get('memory', None))
    df_nodes['allocated_disk'] = df_nodes['allocated_resources'].apply(lambda x: x.get('disk', None))
    df_nodes = df_nodes[['id', 'uuid', 'location_id', 'name', 'description', 'fqdn', 'maintenance_mode', 'memory', 'disk', 'allocated_memory', 'allocated_disk','created_at', 'updated_at']].rename(columns={'': '', '': ''})

    df_nodes['created_at'] = pd.to_datetime(df_nodes['created_at'])
    df_nodes['updated_at'] = pd.to_datetime(df_nodes['updated_at'])

    return df_nodes