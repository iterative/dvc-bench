import os

import pandas as pd
from distutils.version import StrictVersion

df = pd.read_csv("results.csv")
df["test"] = df["name"].str.extract(r"::(.*)\[")


def version(x):
    try:
        return StrictVersion(x)
    except ValueError:
        return StrictVersion("99.99.99")


os.makedirs("plots", exist_ok=True)
for test, test_df in df.groupby("test"):
    test_df["ver_sort"] = test_df["param:dvc_rev"].apply(version)
    test_df = test_df.sort_values("ver_sort").reset_index(drop=True)
    test_df.index.name = "index"
    test_df.to_csv(f"plots/{test}.csv")
