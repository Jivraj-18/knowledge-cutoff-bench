import pandas as pd
def top_after_discount(df, threshold):
    return df.assign(net=pd.col('price') * (1 - pd.col('discount'))).loc[pd.col('net') > threshold]
