import pytest


def test_exp_show(make_project, monkeypatch, bench_dvc, dvc_bin):
    if dvc_bin.version < (2, 10, 0):
        pytest.skip()

    url = "https://github.com/dberenbaum/lstm_seq2seq"
    rev = "e24a469cbbf869a2eb0e6e5df57264f05d0ad654"
    path = make_project(url, rev=rev)
    monkeypatch.chdir(path)

    dvc_bin("exp", "pull", "-A", "--no-cache", "origin")

    bench_dvc("exp", "show", "-A", "--no-pager")
