import pandas as pd
from datetime import datetime, timedelta
from uptime_kuma_api import UptimeKumaApi, MonitorType
from mage_ai.data_preparation.shared.secrets import get_secret_value

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    # Define Kuma variables
    kuma_url = get_secret_value('kuma_url')
    kuma_user = get_secret_value('kuma_user')
    kuma_pass = get_secret_value('kuma_pass')

    # Connect to Kuma
    api = UptimeKumaApi('https://kuma.andes-hosting.com')
    api.login(kuma_user, kuma_pass)

    # Get the ping result
    ping_result = api.avg_ping()

    # Get the uptime result
    uptime_result = api.uptime()

    # Mapping the server names by extracting the id and server names from monitors in kuma and putting them into a dictionary
    # (this is because the avg ping and uptime only give us the id and the info, not the server name)
    monitors = api.get_monitors()
    monitor_dict = {monitor.get("id"): monitor.get("name") for monitor in monitors}

    # Replace server numbers with names in the result
    ping_result_with_names = {monitor_dict.get(key, f"Unknown Server {key}"): value for key, value in ping_result.items()}
    uptime_result_with_names = {monitor_dict.get(key, f"Unknown Server {key}"): value for key, value in uptime_result.items()}
    # Convert ping and uptime to DataFrames
    ping_df = pd.DataFrame(list(ping_result_with_names.items()), columns=['server_name', 'avg_ping'])
    uptime_df = pd.DataFrame(list(uptime_result_with_names.items()), columns=['server_name', 'Uptime'])

    # Transform the NaN ping values to 0
    ping_df = ping_df.fillna('0')

    # Split the 'Uptime' column into '24 Hours' and '30 Days' columns
    uptime_df[['uptime_24hours', 'uptime_30days']] = pd.DataFrame(uptime_df['Uptime'].tolist(), index=uptime_df.index)
    # Drop the original 'Uptime' column and the '30 days column'
    uptime_df = uptime_df.drop(columns=['Uptime', 'uptime_30days'])

    # Multiply the percentage columns by 100
    #uptime_df['uptime_24hours'] *= 100
    #uptime_df['uptime_30days'] *= 100

    # Merge the DataFrames and add the 'creation_time' column
    final_df = pd.merge(ping_df, uptime_df, on='server_name', how='inner')
    final_df['creation_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Filter out rows with 'Unknown Server'
    final_df_filtered = final_df[~final_df['server_name'].str.startswith('Unknown Server')]

    # Print the filtered DataFrame
    return(final_df_filtered)



# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'