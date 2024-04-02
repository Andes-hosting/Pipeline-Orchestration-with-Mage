import pandas as pd

@transformer
def transform(final_df_filtered, *args, **kwargs):

    # Convert 'server_name' to string type (necessary for further comparisons)
    final_df_filtered['server_name'] = final_df_filtered['server_name'].astype(str)

    # Separate the DataFrame into nodes and servers
    nodes_df = final_df_filtered[
        final_df_filtered['server_name'].apply(
            lambda x: str(x).split(' | ')[0].isdigit() and int(str(x).split(' | ')[0]) <= 100
        )
    ]
    nodes_df['server_name'] = nodes_df['server_name'].apply(lambda x: str(x).split(' | ')[0])
    nodes_df.rename(columns={'server_name': 'node_id'}, inplace=True)

    servers_df = final_df_filtered[
        ~final_df_filtered['server_name'].apply(
            lambda x: str(x).split(' | ')[0].isdigit() and int(str(x).split(' | ')[0]) <= 100
        )
    ]
    servers_df['server_name'] = servers_df['server_name'].apply(lambda x: str(x).split(' | ')[0])
    servers_df.rename(columns={'server_name': 'server_identifier'}, inplace=True)

    # Filter out the row with 'Nodes' in servers_df
    servers_df = servers_df[servers_df['server_identifier'] != 'Nodes']

    # Print the DataFrames
    print("Nodes:")
    print(nodes_df)

    print("\nServers:")
    print(servers_df)

    # Return both DataFrames
    return nodes_df, servers_df