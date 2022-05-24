import os
from distutils.version import StrictVersion

import pandas as pd

df = pd.read_csv("results.csv")
df["test"] = df["name"].str.extract("::(.*)\[")


def version(x):
    try:
        return StrictVersion(x)
    except:
        return StrictVersion("99.99.99")
    
os.makedirs("plots", exist_ok=True)
for test, test_df in df.groupby("test"):
    test_df["ver_sort"] = test_df["param:dvc_rev"].apply(version)
    test_df = test_df.sort_values("ver_sort").reset_index(drop=True)
    test_df.index.name = "index"
    test_df.to_csv(f"plots/{test}.csv")
