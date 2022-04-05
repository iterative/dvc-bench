def test_status(bench_dvc, tmp_dir, dvc, make_dataset):
    dataset = make_dataset(files=True, dvcfile=True, cache=True)
    bench_dvc("status")

    (dataset / "new").write_text("new")
    bench_dvc("status", name="changed")
    bench_dvc("status", name="changed-noop")
