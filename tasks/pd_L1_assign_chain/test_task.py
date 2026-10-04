import pandas as pd, solution
df = pd.DataFrame({"item":["a","b","c"],"price":[10.0,20.0,30.0],"qty":[1,2,3],"discount":[0.0,0.5,0.1]})
out = solution.add_total(df)
assert list(out["total"]) == [10.0, 40.0, 90.0], list(out["total"])
assert "total" not in df.columns
print("PASS")
