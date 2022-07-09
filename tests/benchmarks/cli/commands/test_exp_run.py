def test_exp_run(make_project, monkeypatch, bench_dvc):
    url = "https://github.com/dberenbaum/lstm_seq2seq"
    rev = "dvc"
    path = make_project(url, rev=rev)
    monkeypatch.chdir(path)

    bench_dvc("exp", "run")
    bench_dvc("exp", "run", name="noop")
