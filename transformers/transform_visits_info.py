import pandas as pd
from user_agents import parse

@transformer
def transform(visits_info_df, *args, **kwargs):

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