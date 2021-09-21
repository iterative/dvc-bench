def test_checkout(bench_dvc, tmp_dir, dvc, make_dataset):
    dataset = make_dataset(dvcfile=True, cache=True, files=False)
    bench_dvc("checkout", dataset)
    bench_dvc("checkout", name="noop")
    (dataset / "new").write_text("new")
    bench_dvc("checkout", "--force", name="update")
