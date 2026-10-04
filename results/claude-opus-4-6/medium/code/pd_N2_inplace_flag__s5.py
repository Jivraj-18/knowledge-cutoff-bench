def flag_large(df):
    df.loc[df["amount"] > 100, "flag"] = True
