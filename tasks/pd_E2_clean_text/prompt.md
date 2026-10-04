Our project's requirements.txt:
```
pandas>=2.2,<3
numpy
```

Here is the current `solution.py` from our project:
```python
import pandas as pd

def clean_text(df):
    out = df.copy()
    for col in out.select_dtypes(include="object").columns:
        out[col] = out[col].str.strip()
    return out
```

Also lowercase every text column (after stripping), and add a column `n_text_cols`
 holding the number of text columns in the input. Numeric columns must stay unchanged.
Return the complete updated `solution.py`.

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than pandas.
