def test_repro(bench_dvc, tmp_dir, scm, dvc, make_dataset, pipeline):
    make_dataset(files=True, dvcfile=True, cache=True)
    bench_dvc("repro")
    bench_dvc("repro", name="noop")
