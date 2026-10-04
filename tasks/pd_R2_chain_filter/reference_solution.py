def top_after_discount(df, threshold):
    return df.assign(net=lambda d: d['price'] * (1 - d['discount'])).loc[lambda d: d['net'] > threshold]
