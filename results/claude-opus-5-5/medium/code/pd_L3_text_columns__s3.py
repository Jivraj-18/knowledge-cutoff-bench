import pandas as pd
from pandas.api.types import infer_dtype


def text_columns(df):
    """Return the names of the columns that hold text, in their original order.

    With default dtype inference in pandas 2.3.x, string columns are stored as
    ``object`` dtype (or the ``string`` dtype if ``future.infer_string`` is
    enabled). ``object`` columns can also hold non-text values, such as mixed
    types, lists or dicts. So each candidate column is also checked to confirm
    that its non-missing values are actually strings.
    """
    candidates = df.select_dtypes(include=["object", "string"])
    return [
        name
        for name in candidates.columns
        if infer_dtype(candidates[name], skipna=True) == "string"
    ]
