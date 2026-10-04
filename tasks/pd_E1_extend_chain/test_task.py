
import pandas as pd, solution
df = pd.DataFrame({"item":["a","b","c","d"],"price":[10.0,20.0,30.0,5.0],"cost":[9.0,10.0,20.0,1.0],"qty":[1,2,3,0]})
out = solution.summarize(df)
assert list(out["item"]) == ["c","b"], list(out["item"])
assert abs(out["margin"].iloc[1] - 0.5) < 1e-9
print("PASS")
