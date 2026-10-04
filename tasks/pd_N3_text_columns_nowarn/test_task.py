import warnings, pandas as pd, solution
df = pd.DataFrame({"name":["x","y"],"n":[1,2],"city":["p","q"],"f":[1.5,2.5]})
with warnings.catch_warnings():
    warnings.simplefilter("error")
    out = list(solution.text_columns(df))
assert out == ["name","city"], out
print("PASS")
