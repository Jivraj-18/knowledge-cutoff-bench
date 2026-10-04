import pandas as pd, solution, inspect
src = inspect.getsource(solution)
assert "pd.col(" in src or "pandas.col(" in src, "must use pd.col"
assert "lambda" not in src, "must not use lambda"
df = pd.DataFrame({"item":["a","b","c"],"price":[10.0,20.0,30.0],"qty":[1,2,3],"discount":[0.0,0.5,0.1]})
out = solution.add_total(df)
assert list(out["total"]) == [10.0, 40.0, 90.0], list(out["total"])
print("PASS")
