def test_exp_run(make_project, monkeypatch, dvc_bin, bench_dvc):
    url = "https://github.com/iterative/example-dvc-experiments"
    rev = "main"
    path = make_project(url, rev=rev)
    monkeypatch.chdir(path)

    dvc_bin("pull")

    bench_dvc("exp", "run")
    bench_dvc("exp", "run", name="noop")
