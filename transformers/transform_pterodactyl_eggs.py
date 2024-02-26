import pandas as pd

@transformer
def transform(data, *args, **kwargs):

    all_eggs = data[5]

    df_eggs = pd.DataFrame(all_eggs[0])
    df_eggs = df_eggs[['id', 'uuid', 'nest', 'name', 'description', 'author', 'created_at', 'updated_at']].rename(columns={'nest': 'nest_id'})

    df_eggs['created_at'] = pd.to_datetime(df_eggs['created_at'])
    df_eggs['updated_at'] = pd.to_datetime(df_eggs['updated_at'])

    return df_eggs