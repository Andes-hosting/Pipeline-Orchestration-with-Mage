import pandas as pd

@transformer
def transform(data_list, *args, **kwargs):

    # Create a DataFrame
    urls_df = pd.DataFrame(data_list)

    # Drop unwanted columns
    unwanted_columns = ['deviceLongUrls', 'visitsSummary', 'domain', 'crawlable', 'forwardQuery']
    urls_df = urls_df.drop(columns=unwanted_columns, errors='ignore')

    # Separate 'meta' into individual columns
    urls_df[['maxVisits', 'validSince', 'validUntil']] = urls_df['meta'].apply(lambda x: pd.Series([x['maxVisits'], x['validSince'], x['validUntil']]))

    # Drop the original 'visitsSummary' column
    urls_df = urls_df.drop(columns='meta')

    # convert string to timestamp
    urls_df['dateCreated'] = pd.to_datetime(urls_df['dateCreated'])
    urls_df['validSince'] = pd.to_datetime(urls_df['validSince'])
    urls_df['validUntil'] = pd.to_datetime(urls_df['validUntil'])

    # Assuming urls_df is your DataFrame
    urls_df.columns = urls_df.columns.str.lower()

    return urls_df