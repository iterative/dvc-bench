import pytest

from dvc.repo import Repo
from tests.benchmarks.conftest import pull


@pytest.mark.requires(
    minversion=(2, 34, 0), reason="top-level plots not supported"
)
def test_plots(project, bench_dvc):
    with Repo() as dvc:
        pull(dvc)

    bench_kwargs = {"rounds": 5, "iterations": 3, "warmup_rounds": 2}
    bench_dvc("plots", "show", name="show", **bench_kwargs)
    bench_dvc("plots", "show", "--json", name="show-json", **bench_kwargs)
    bench_dvc("plots", "diff", name="diff", **bench_kwargs)
    bench_dvc("plots", "diff", "--json", name="diff-json", **bench_kwargs)
