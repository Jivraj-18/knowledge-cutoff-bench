import pandas as pd

def top_after_discount(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    return df.assign(net=lambda d: d["price"] * (1 - d["discount"])).query("net > @threshold")
