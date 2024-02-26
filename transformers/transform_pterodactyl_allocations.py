from Andes.utils.ptero_app import flatten_list
import pandas as pd

@transformer
def transform(data, *args, **kwargs):

    all_allocations = data[3]

    df_allocations = pd.DataFrame(flatten_list(all_allocations))
    df_allocations = df_allocations[['id', 'node_id', 'port', 'assigned']]

    return df_allocations