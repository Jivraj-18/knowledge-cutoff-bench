import pandas as pd


def text_columns(df: pd.DataFrame) -> list:
    """Return the names of columns holding text, in their original order.

    Under pandas 2.3.3's default inference, string columns get ``object``
    dtype. Opting into ``future.infer_string`` gives them a ``string`` dtype
    instead, so both are selected. Object columns can also hold non-text
    values (mixed types, lists, dicts, ...), so each object column is kept
    only if all of its non-null values are ``str``.
    """
    candidates = df.select_dtypes(include=["object", "string"])

    result = []
    for name in candidates.columns:
        col = candidates[name]
        if isinstance(col.dtype, pd.StringDtype):
            result.append(name)
            continue
        non_null = col.dropna()
        if non_null.map(lambda v: isinstance(v, str)).all():
            result.append(name)
    return result
