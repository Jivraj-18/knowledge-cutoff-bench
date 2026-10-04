def flag_large(df):
    df['flag'][df['amount'] > 100] = True
