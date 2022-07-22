import pytest
from shutil import rmtree


def test_data_status(dvc_bin, bench_dvc, tmp_dir, scm, dvc, make_dataset):
    if dvc_bin.version < (2, 15, 0):
        pytest.skip()

    dataset = make_dataset(cache=True, files=True, dvcfile=True, commit=False)
    rmtree(dvc.tmp_dir)

    bench_dvc("data", "status", name="new")
    bench_dvc("data", "status", name="noop")

    tmp_dir.scm_add(dataset.with_suffix(".dvc").name, commit="add dataset")

    (dataset / "new").write_text("new")
    bench_dvc("data", "status", name="changed")
    bench_dvc("data", "status", name="changed-noop")
