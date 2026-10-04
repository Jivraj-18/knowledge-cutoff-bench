import pandas as pd


def add_total(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(total=lambda d: d["price"] * d["qty"])
