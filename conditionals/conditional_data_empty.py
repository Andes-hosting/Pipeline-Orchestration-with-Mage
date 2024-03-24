import pandas as pd

@condition
def is_data_emtpy(data, *args, **kwargs) -> bool:

    result = False

    if isinstance(data, list):
        if not data:
            result = True
    elif isinstance(data, pd.DataFrame):
        if data.empty:
            result = True

    return result