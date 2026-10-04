import pandas as pd
def add_total(df):
    return df.assign(total=pd.col('price') * pd.col('qty'))
