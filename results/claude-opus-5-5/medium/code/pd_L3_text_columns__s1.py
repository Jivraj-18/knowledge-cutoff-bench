import pandas as pd
from pandas.api.types import infer_dtype, is_object_dtype


def text_columns(df):
    """Return the names of the columns in ``df`` that hold text, in order.

    With default inference in pandas 2.3.3, string columns get ``object``
    dtype, or the ``str`` dtype if ``future.infer_string`` is enabled.
    ``object`` columns can also hold non-text values (lists, dicts,
    Decimals, mixed types), so those candidates are checked to make sure
    their non-missing values are actually strings.
    """
    candidates = df.select_dtypes(include=["object", "string"])
    result = []
    for name in candidates.columns:
        col = candidates[name]
        if is_object_dtype(col.dtype):
            if infer_dtype(col, skipna=True) != "string":
                continue
        result.append(name)
    return result
