import pandas as pd
import datetime

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    
    # Create the dataframe and extract data from resources
    df_consumptions = pd.DataFrame(all_utilizations)
    df_consumptions['status'] = df_consumptions['current_state'].replace({'running': True, 'offline': False})
    df_consumptions['cpu'] = df_consumptions['resources'].apply(lambda x: x.get('cpu_absolute', None))
    df_consumptions['ram'] = df_consumptions['resources'].apply(lambda x: bytes_to_megabytes(x.get('memory_bytes', None)))
    df_consumptions['disk'] = df_consumptions['resources'].apply(lambda x: bytes_to_megabytes(x.get('disk_bytes', None)))
    df_consumptions['capture_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    df_consumptions = df_consumptions[['identifier', 'status', 'ram', 'cpu', 'disk', 'capture_time']]

    # Group by 'identifier' and calculate mean, std, min, and max for each group
    final_utilization_df = df_consumptions.groupby('identifier').agg({
        'status': ['first'],  # Include 'current_state' in the aggregation
        'ram': ['mean', 'std', 'min', 'max'],
        'cpu': ['mean', 'std', 'min', 'max'],
        'disk': ['mean', 'std', 'min', 'max'],
        'capture_time': ['first']  
    }).reset_index()

    # Flatten the column names
    final_utilization_df.columns = ['_'.join(col).strip() for col in final_utilization_df.columns.values]

    # Rename columns
    final_utilization_df = final_utilization_df.rename(columns={'identifier_': 'server_identifier'})
    final_utilization_df = final_utilization_df.rename(columns={'status_first': 'status'})
    final_utilization_df = final_utilization_df.rename(columns={'capture_time_first': 'capture_time'})
    return final_utilization_df


