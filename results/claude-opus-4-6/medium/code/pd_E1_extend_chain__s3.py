import pandas as pd

def summarize(df):
    return (
        df.assign(revenue=lambda d: d["price"] * d["qty"],
                  margin=lambda d: (d["price"] - d["cost"]) / d["price"])
          .loc[lambda d: (d["revenue"] > 0) & (d["margin"] > 0.2)]
          .sort_values("revenue", ascending=False)
    )
