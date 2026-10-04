import pandas as pd


def text_columns(df: pd.DataFrame) -> list:
    """Return the names of the text columns of ``df``, in their original order.

    With pandas 3.0's default dtype inference, text columns get the dedicated
    ``str`` dtype (a ``StringDtype``) rather than ``object``. Selecting with
    ``"string"`` matches every ``StringDtype`` variant. It avoids
    ``include="object"``, which would only match ``str`` columns through a
    deprecated compatibility path that emits a warning.
    """
    return df.select_dtypes(include="string").columns.tolist()
