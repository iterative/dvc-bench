import shutil

import pytest


def test_sharing(bench_dvc, tmp_dir, dvc, dataset, remote):
    bench_dvc("add", dataset)
    bench_dvc("add", dataset, name="noop")

    bench_dvc("push")
    bench_dvc("push", name="noop")

    shutil.rmtree(dataset)
    shutil.rmtree(dvc.odb.local.cache_dir)

    bench_dvc("pull")
    bench_dvc("pull", name="noop")

    bench_dvc("checkout", name="noop")


@pytest.mark.parametrize("jobs", [None, 1, 2, 4])
def test_jobs(bench_dvc, tmp_dir, dvc, dataset, remote, jobs):
    if jobs:
        args = ("-j", str(jobs))

    bench_dvc("add", dataset)
    bench_dvc("push", *args)

    shutil.rmtree(dataset)
    shutil.rmtree(dvc.odb.local.cache_dir)

    bench_dvc("pull", *args)
