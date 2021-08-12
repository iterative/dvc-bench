def test_status(bench_dvc, tmp_dir, dvc, make_dataset):
    make_dataset(files=True, dvcfile=True, cache=True)
    bench_dvc("status")
