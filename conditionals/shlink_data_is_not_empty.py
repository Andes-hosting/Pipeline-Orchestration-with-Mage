import pandas as pd

@condition
def is_data_emtpy(data, *args, **kwargs) -> bool:

    result = True

    if isinstance(data, list):
        if not data:
            result = False
    elif isinstance(data, pd.DataFrame):
        if data.empty:
            result = False

    return result