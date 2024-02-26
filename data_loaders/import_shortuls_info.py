from mage_ai.data_preparation.shared.secrets import get_secret_value
from shlink import Shlink

@data_loader
def load_data_from_api(*args, **kwargs):

    # Connecto to Shlink API
    shlink = Shlink(
                url = get_secret_value('shlink_url'), 
                api_key = get_secret_value('shlink_api_key'))

    #Extract the list of short urls with the information
    short_urls = shlink.list_short_urls()

    # Extract the 'data' section
    data_list = short_urls['shortUrls']['data']

    return data_list