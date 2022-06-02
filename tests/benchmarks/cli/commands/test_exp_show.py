import pytest


def test_exp_show(project, bench_dvc, dvc_bin):
    if dvc_bin.version < (2, 10, 0):
        pytest.skip()

    dvc_bin("exp", "pull", "-A", "--no-cache", "origin")

    bench_dvc("exp", "show", "-A", "--no-pager")
