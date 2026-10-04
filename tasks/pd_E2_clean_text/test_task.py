
import pandas as pd, solution
df = pd.DataFrame({"name":["  Ann ","BOB"],"city":[" Pune","DELHI "],"n":[1,2]})
out = solution.clean_text(df)
assert list(out["name"]) == ["ann","bob"] and list(out["city"]) == ["pune","delhi"], out
assert list(out["n"]) == [1,2]
assert list(out["n_text_cols"]) == [2,2], list(out["n_text_cols"])
print("PASS")
