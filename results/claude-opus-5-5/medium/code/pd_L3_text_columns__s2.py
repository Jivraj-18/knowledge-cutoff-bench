import pandas as pd
from pandas.api.types import infer_dtype


def text_columns(df):
    """Return the names of the columns that hold text, in their original order.

    With default inference in pandas 2.x, text columns get ``object`` dtype
    (or a ``string`` dtype when ``future.infer_string`` is enabled). ``object``
    columns can also hold non-text values, so each candidate's contents are
    checked as well.
    """
    candidates = df.select_dtypes(include=["object", "string"])
    return [
        name
        for name, col in candidates.items()
        if infer_dtype(col, skipna=True) == "string"
    ]
