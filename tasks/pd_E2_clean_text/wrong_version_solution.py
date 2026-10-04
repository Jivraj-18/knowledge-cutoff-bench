
import pandas as pd

def clean_text(df):
    out = df.copy()
    text_cols = out.select_dtypes(include="str").columns
    for col in text_cols:
        out[col] = out[col].str.strip().str.lower()
    out["n_text_cols"] = len(text_cols)
    return out
