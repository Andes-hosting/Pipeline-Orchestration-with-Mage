import pandas as pd
import requests
from shlink import Shlink
from datetime import datetime
from user_agents import parse
from mage_ai.data_preparation.shared.secrets import get_secret_value

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(urls_df, *args, **kwargs):
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
    # Specify your transformation logic here
    # Create an empty DataFrame to store visit data
    visits_info_df = pd.DataFrame()

    # Connecto to Shlink API
    shlink = Shlink(
                url = get_secret_value('shlink_url'), 
                api_key = get_secret_value('shlink_api_key'))

    # Loop through the urls_df and use each 'shortCode' in list_visit function
    for index, row in urls_df.iterrows():
        shortCode = row['shortcode']
        visits_data = shlink.list_visit_data(shortCode)
        
        if 'visits' in visits_data and 'data' in visits_data['visits']:
            visits_data_list = visits_data['visits']['data']
            df_visits = pd.DataFrame(visits_data_list)
            df_visits['shortCode'] = shortCode  # Add shortCode as a column

            # Check if 'visitLocation' is in columns before normalizing
            if 'visitLocation' in df_visits.columns:
                visit_location_df = pd.json_normalize(df_visits['visitLocation'])
                df_visits = pd.concat([df_visits, visit_location_df], axis=1)
            
                # Drop the original 'visitLocation' column
                df_visits = df_visits.drop(columns='visitLocation')

            visits_info_df = pd.concat([visits_info_df, df_visits])

    # Create new columns for browser, operating system, and device
    visits_info_df['Browser'] = visits_info_df['userAgent'].apply(lambda x: parse(x).browser.family)
    visits_info_df['Operating_System'] = visits_info_df['userAgent'].apply(lambda x: parse(x).os.family)
    visits_info_df['Device'] = visits_info_df['userAgent'].apply(lambda x: parse(x).device.family)

    # Filter out rows where 'potentialBot' is True
    visits_info_df = visits_info_df[visits_info_df['potentialBot'] == False]

    # Drop the original 'userAgent' and 'potentialBot' column
    visits_info_df.drop(columns=['userAgent'], inplace=True)
    visits_info_df.drop(columns=['potentialBot'], inplace=True)

    # Drop the specified columns
    columns_to_drop = ['countryCode', 'cityName', 'latitude', 'longitude', 'isEmpty', 'Device']
    visits_info_df.drop(columns=columns_to_drop, inplace=True)

    # Function to classify operating system into 'Mobile' or 'Desktop'
    def classify_device(os):
        if 'Android' in os or 'iOS' in os:
            return 'Mobile'
        else:
            return 'Desktop'

    # Apply the function to create a new 'Device' column
    visits_info_df['Device'] = visits_info_df['Operating_System'].apply(classify_device)

    # Assuming urls_df is your DataFrame
    visits_info_df.columns = visits_info_df.columns.str.lower()

    # Display the modified DataFrame
    return visits_info_df


# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'