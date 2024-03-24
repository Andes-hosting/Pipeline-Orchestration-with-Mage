import pandas as pd

@custom
def transform_custom(data, *args, **kwargs):

    return pd.DataFrame(data)