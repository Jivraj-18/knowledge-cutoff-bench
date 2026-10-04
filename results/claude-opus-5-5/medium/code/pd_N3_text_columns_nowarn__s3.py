import pandas as pd


def text_columns(df: pd.DataFrame) -> list:
    """Return the names of the text columns in ``df``, in their original order.

    In pandas 3.x, default dtype inference stores text in the dedicated
    ``str`` dtype rather than ``object``. Selecting with ``include="str"``
    targets those columns directly and avoids the deprecation warning that
    ``include="object"`` raises when it matches string columns.
    """
    return df.select_dtypes(include="str").columns.tolist()
