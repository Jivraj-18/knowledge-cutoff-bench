import pandas as pd


def text_columns(df: pd.DataFrame) -> list:
    """Return the names of columns that hold text, in their original order.

    Under pandas 2.x default inference, text columns get ``object`` dtype,
    but ``object`` can also hold other Python objects (lists, dicts,
    Decimals, mixed types). So candidates are selected via
    ``select_dtypes`` and object columns are then checked to contain only
    strings (ignoring missing values). The ``string`` dtype is included as
    well so this also works when ``future.infer_string`` is enabled.
    """
    candidates = df.select_dtypes(include=["object", "string"])

    result = []
    for name in candidates.columns:
        col = candidates[name]
        if isinstance(col.dtype, pd.StringDtype):
            result.append(name)
            continue
        non_null = col.dropna()
        if all(isinstance(value, str) for value in non_null):
            result.append(name)
    return result
