import pandas as pd


def flag_large(df: pd.DataFrame) -> None:
    """Set df['flag'] to True in place for every row where amount > 100."""
    mask = df["amount"] > 100
    # Use a single .loc assignment; chained assignment does not modify the
    # original DataFrame under pandas 3.x Copy-on-Write semantics.
    df.loc[mask, "flag"] = True
    return None
