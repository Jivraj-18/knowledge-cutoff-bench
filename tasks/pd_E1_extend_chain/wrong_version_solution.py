
import pandas as pd

def summarize(df):
    return (
        df.assign(revenue=pd.col("price") * pd.col("qty"),
                  margin=(pd.col("price") - pd.col("cost")) / pd.col("price"))
          .loc[(pd.col("revenue") > 0) & (pd.col("margin") > 0.2)]
          .sort_values("revenue", ascending=False)
    )
