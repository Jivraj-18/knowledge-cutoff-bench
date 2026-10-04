import pandas as pd, solution
df = pd.DataFrame({"amount":[50,150,300],"flag":[False,False,False]})
r = solution.flag_large(df)
assert r is None
assert list(df["flag"]) == [False, True, True], list(df["flag"])
print("PASS")
