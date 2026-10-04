import pandas as pd


def text_columns(df: pd.DataFrame) -> list:
    # In pandas 3.0, text columns are inferred as the "str" dtype by default,
    # so they are no longer selected by include="object".
    return df.select_dtypes(include=["str"]).columns.tolist()
