def top_after_discount(df, threshold):
    return df.assign(net=df["price"] * (1 - df["discount"])).query("net > @threshold")
