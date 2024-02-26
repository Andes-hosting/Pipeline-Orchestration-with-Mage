import io
import pandas as pd
import requests
from shlink import Shlink
from datetime import datetime
from mage_ai.data_preparation.shared.secrets import get_secret_value

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    # Connecto to Shlink API
    shlink = Shlink(
                url = get_secret_value('shlink_url'), 
                api_key = get_secret_value('shlink_api_key'))

    #Extract the list of short urls with the information
    short_urls = shlink.list_short_urls()

    # Extract the 'data' section
    data_list = short_urls['shortUrls']['data']

    # Create a DataFrame
    urls_df = pd.DataFrame(data_list)

    # Drop unwanted columns
    unwanted_columns = ['deviceLongUrls', 'meta', 'domain', 'crawlable', 'forwardQuery', 'visitsCount']
    urls_df = urls_df.drop(columns=unwanted_columns, errors='ignore')

    # Separate 'visitsSummary' into individual columns
    urls_df[['total', 'nonBots', 'bots']] = urls_df['visitsSummary'].apply(lambda x: pd.Series([x['total'], x['nonBots'], x['bots']]))

    # Drop the original 'visitsSummary' column
    urls_df = urls_df.drop(columns='visitsSummary')

    # convert string to timestamp
    urls_df['dateCreated'] = pd.to_datetime(urls_df['dateCreated'])

    # Assuming urls_df is your DataFrame
    urls_df.columns = urls_df.columns.str.lower()

    return urls_df
# Recuerda tratar de extraer
# Limit access to the short URL
# Maximum number allowed
# enable since
# enable until

    


# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'