def test_exp_run(bench_dvc, tmp_dir, scm, dvc, make_dataset, pipeline):
    make_dataset(files=True, dvcfile=True, cache=True)
    bench_dvc("exp", "run")
    bench_dvc("exp", "run", name="noop")
