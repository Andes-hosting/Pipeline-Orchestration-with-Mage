import pandas as pd

@transformer
def transform(data, *args, **kwargs):

    all_nests = data[4]

    df_nests = pd.DataFrame(all_nests[0])
    df_nests = df_nests[['id', 'uuid', 'name', 'description', 'author', 'created_at', 'updated_at']]

    df_nests['created_at'] = pd.to_datetime(df_nests['created_at'])
    df_nests['updated_at'] = pd.to_datetime(df_nests['updated_at'])

    return df_nests