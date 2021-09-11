def test_diff(bench_dvc, tmp_dir, scm, dvc, make_dataset):
    make_dataset(cache=True, files=True, dvcfile=True, commit=True)
    bench_dvc("diff")
    bench_dvc("diff", name="noop")
