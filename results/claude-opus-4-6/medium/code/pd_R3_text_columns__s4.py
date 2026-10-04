def text_columns(df):
    return df.select_dtypes(include="object").columns.tolist()
