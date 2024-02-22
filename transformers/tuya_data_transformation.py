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
    transformed_data = []

    for entry in data:
        power = entry['status_device']['result'][4]['value'] / 10
        timestamp = datetime.datetime.fromtimestamp(entry['status_device']['t'] / 1000)

        transformed_data.append({'device_uid': entry['device_uid'], 'name': entry['name'], 'power': power, 'timestamp': timestamp})

    df_energy_devices = pd.DataFrame(transformed_data)
    return df_energy_devices


#@test
#def test_output(output, *args) -> None:
#    """
#    Template code for testing the output of the block.
#    """
#    assert output is not None, 'The output is undefined'
