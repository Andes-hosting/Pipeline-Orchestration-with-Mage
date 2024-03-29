from mage_ai.data_preparation.shared.secrets import get_secret_value
from datetime import datetime, timedelta
from shlink import Shlink
import pandas as pd

@data_loader
def load_data(data, *args, **kwargs):

    # Create an empty DataFrame to store visit data
    visits_info_df = pd.DataFrame()

    # Connecto to Shlink API
    shlink = Shlink(
                url = get_secret_value('shlink_url'), 
                api_key = get_secret_value('shlink_api_key'))

    # Loop through the urls_df and use each 'shortCode' in list_visit function
    for index, row in data.iterrows():
        short_url_id = row['id']
        shortCode = row['shortcode']
        latest_date = row['latest_date']
        
        # Get today's date
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        visits_data = shlink.list_visit_data(short_code = shortCode, startDate = latest_date, endDate = yesterday, excludeBots = True)

        if 'visits' in visits_data and 'data' in visits_data['visits']:
            visits_data_list = visits_data['visits']['data']
            df_visits = pd.DataFrame(visits_data_list)
            df_visits['short_url_id'] = short_url_id  # Add short_url_id as a column

            # Check if 'visitLocation' is in columns before normalizing
            if 'visitLocation' in df_visits.columns:
                visit_location_df = pd.json_normalize(df_visits['visitLocation'])
                df_visits = pd.concat([df_visits, visit_location_df], axis=1)

                # Drop the original 'visitLocation' column
                df_visits = df_visits.drop(columns='visitLocation')

            if not df_visits.empty:
                df_visits[['potentialBot', 'isEmpty']] = df_visits[['potentialBot', 'isEmpty']].astype(bool)
                visits_info_df = pd.concat([visits_info_df, df_visits])

    return visits_info_df