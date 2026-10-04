Our project's requirements.txt:
```
pandas>=2.2,<3
numpy
```

Here is the current `solution.py` from our project:
```python
import pandas as pd

def summarize(df):
    return (
        df.assign(revenue=lambda d: d["price"] * d["qty"])
          .loc[lambda d: d["revenue"] > 0]
          .sort_values("revenue", ascending=False)
    )
```

Extend the chain in `summarize`: after computing `revenue`, also add a column
 `margin` = `(price - cost) / price`, and keep only rows where `margin > 0.2` (in addition to the existing filter).
 Keep it a single method chain.
Return the complete updated `solution.py`.

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than pandas.
