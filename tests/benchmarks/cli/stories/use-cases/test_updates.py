import os


def test_changes(bench_dvc, tmp_dir, dvc, make_dataset):
    dataset = make_dataset(
        cache=False, files=True, dvcfile=False, commit=False, remote=False
    )
    bench_dvc("import-url", str(dataset), "new")

    # Remove one file
    for path in dataset.rglob("*"):
        if path.is_file():
            os.remove(path)
            break
    bench_dvc("update", "new.dvc")
    bench_dvc("update", "new.dvc", name="noop")
