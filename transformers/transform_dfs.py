import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(final_df_filtered, *args, **kwargs):
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

    # Return both DataFrames
    return nodes_df, servers_df
    
    # Print the DataFrames
    print("Nodes:")
    print(nodes_df)

    print("\nServers:")
    print(servers_df)



    


# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'