import pandas as pd


def text_columns(df: pd.DataFrame) -> list:
    """Return the names of the columns in ``df`` that hold text, in their original order.

    Under pandas 2.x default inference, string columns get the ``object`` dtype.
    If the ``future.infer_string`` option is enabled, they get the dedicated
    ``string`` dtype instead, so both are selected. ``object`` columns can also
    hold non-text values such as lists, dicts or mixed types, so each candidate
    is checked to confirm that its non-missing values are strings.
    """
    candidates = df.select_dtypes(include=["object", "string"])
    return [
        name
        for name in candidates.columns
        if pd.api.types.infer_dtype(candidates[name], skipna=True) == "string"
    ]
