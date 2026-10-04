import pandas as pd


def flag_large(df: pd.DataFrame) -> None:
    df.loc[df["amount"] > 100, "flag"] = True
