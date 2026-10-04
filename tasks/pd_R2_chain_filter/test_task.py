import pandas as pd, solution
df = pd.DataFrame({"item":["a","b","c"],"price":[10.0,20.0,30.0],"qty":[1,2,3],"discount":[0.0,0.5,0.1]})
out = solution.top_after_discount(df, 12)
assert list(out["item"]) == ["c"], list(out["item"])
assert abs(out["net"].iloc[0] - 27.0) < 1e-9
print("PASS")
