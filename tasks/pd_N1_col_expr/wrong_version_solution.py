def add_total(df):
    return df.assign(total=lambda d: d['price'] * d['qty'])
