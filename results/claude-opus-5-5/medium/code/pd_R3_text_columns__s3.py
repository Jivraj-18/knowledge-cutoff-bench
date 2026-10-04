import pandas as pd


def text_columns(df: pd.DataFrame) -> list:
    # Under pandas 2.x default inference, text columns are stored as `object`;
    # include "string" too so StringDtype columns (or future.infer_string) are covered.
    return list(df.select_dtypes(include=["object", "string"]).columns)
