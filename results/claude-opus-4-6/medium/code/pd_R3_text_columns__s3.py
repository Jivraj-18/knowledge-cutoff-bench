def text_columns(df):
    return list(df.select_dtypes(include="object").columns)
