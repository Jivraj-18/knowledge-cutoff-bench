import pandas as pd


def text_columns(df: pd.DataFrame) -> list:
    """Return the names of columns holding text, in their original order.

    With default inference in pandas 2.x, string columns get ``object`` dtype
    (or a string dtype if ``future.infer_string`` is enabled). Because
    ``object`` columns can also hold non-text values, object columns are kept
    only if every non-missing value is a ``str``.
    """
    candidates = df.select_dtypes(include=["object", "string"])

    result = []
    for name in candidates.columns:
        col = candidates[name]
        if isinstance(col.dtype, pd.StringDtype):
            result.append(name)
            continue
        values = col.dropna()
        if values.map(lambda v: isinstance(v, str)).all():
            result.append(name)
    return result
