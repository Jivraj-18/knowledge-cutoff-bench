import pandas as pd


def top_after_discount(df: pd.DataFrame, threshold) -> pd.DataFrame:
    return (
        df.assign(net=lambda d: d["price"] * (1 - d["discount"]))
        .loc[lambda d: d["net"] > threshold]
    )
