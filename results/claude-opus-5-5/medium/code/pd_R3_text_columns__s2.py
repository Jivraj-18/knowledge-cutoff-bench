import pandas as pd


def text_columns(df: pd.DataFrame) -> list:
    """Return the names of text columns in their original order.

    With pandas 2.x default inference, text is stored as ``object`` dtype;
    ``"string"`` covers the dedicated StringDtype (e.g. when
    ``future.infer_string`` is enabled or columns were converted explicitly).
    """
    return df.select_dtypes(include=["object", "string"]).columns.tolist()
