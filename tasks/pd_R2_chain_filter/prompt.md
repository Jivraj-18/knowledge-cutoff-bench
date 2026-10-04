Our project's requirements.txt:
```
pandas>=2.2,<3
numpy
```

Write a function `top_after_discount(df, threshold)` that, in a single method chain starting from `df`,
 first adds a column `net` = `price * (1 - discount)` and then keeps only rows where `net > threshold`.
 The function body must be a single `return` statement with no intermediate variables.

Respond with exactly one Python code block containing the complete contents of `solution.py`. No explanation outside the code block. Do not use any third-party packages other than pandas.
