def test_list(bench_dvc, tmp_dir, scm, dvc, make_dataset, remote):
    make_dataset(
        cache=False, files=False, dvcfile=True, commit=True, remote=True
    )
    bench_dvc("list", tmp_dir)
    bench_dvc("list", tmp_dir, "--dvc-only", name="dvc-only")
