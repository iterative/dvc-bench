import pytest


def test_exp_show(make_project, monkeypatch, bench_dvc, dvc_bin):
    if dvc_bin.version < (2, 10, 0):
        pytest.skip()

    url = "https://github.com/efiop/lstm_seq2seq"
    rev = "dvc-bench"
    path = make_project(url, rev=rev)
    monkeypatch.chdir(path)

    dvc_bin("exp", "pull", "-A", "--no-cache", "origin")

    bench_dvc("exp", "show", "-A", "--no-pager")
