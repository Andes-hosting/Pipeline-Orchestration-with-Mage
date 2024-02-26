import pandas as pd

@transformer
def transform(data, *args, **kwargs):

    all_locations = data[1]

    df_locations = pd.DataFrame(all_locations[0])
    df_locations = df_locations[['id', 'short', 'long', 'created_at', 'updated_at']]

    df_locations['created_at'] = pd.to_datetime(df_locations['created_at'])
    df_locations['updated_at'] = pd.to_datetime(df_locations['updated_at'])

    return df_locations