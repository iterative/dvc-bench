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
    
df["ver"] = df["param:dvc_rev"].apply(version)
df = df.sort_values("ver").reset_index()

os.makedirs("plots", exist_ok=True)
for test, test_df in df.groupby("test"):
    ax = test_df[["mean"]].plot(title=test)
    ax.set_xticks(test_df.index)
    ax.set_xticklabels(test_df["param:dvc_rev"])
    ax.legend([test])
    ax.figure.savefig(f"plots/{test}.png")
