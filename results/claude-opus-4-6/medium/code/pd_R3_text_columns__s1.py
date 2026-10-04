import pandas as pd


def text_columns(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include=["object", "string"]).columns.tolist()
