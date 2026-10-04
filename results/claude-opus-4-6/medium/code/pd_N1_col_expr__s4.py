# solution.py
import pandas as pd

def add_total(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(total=pd.col("price") * pd.col("qty"))
