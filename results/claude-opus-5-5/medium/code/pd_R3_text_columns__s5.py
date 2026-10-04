import pandas as pd
from pandas.api.types import infer_dtype


def text_columns(df: pd.DataFrame) -> list:
    """Return the names of the columns in ``df`` that hold text, in their original order.

    Under pandas 2.x default inference, string columns get the ``object``
    dtype. ``object`` columns can also hold non-text values, such as lists,
    dicts, or mixed types, so each ``object`` column is checked to make sure
    its values are actually strings. Columns with a dedicated string dtype
    (``"string"``, for example when ``future.infer_string`` is enabled) are
    always text.
    """
    candidates = df.select_dtypes(include=["object", "string"])

    result = []
    for i, name in enumerate(candidates.columns):
        col = candidates.iloc[:, i]  # positional access keeps duplicate column names safe
        if col.dtype == object and infer_dtype(col, skipna=True) not in ("string", "empty"):
            continue
        result.append(name)
    return result
