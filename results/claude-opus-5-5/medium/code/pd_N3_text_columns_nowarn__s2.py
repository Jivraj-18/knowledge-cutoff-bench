import pandas as pd


def text_columns(df: pd.DataFrame) -> list:
    # pandas 3.x infers text columns as the dedicated "str" dtype (not object)
    return list(df.select_dtypes(include=["str"]).columns)
