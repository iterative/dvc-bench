import glob
import os
import random
import shutil


def test_sharing(bench_dvc, tmp_dir, dvc, dataset, remote):
    bench_dvc("add", dataset)
    bench_dvc("add", dataset, name="noop")

    bench_dvc("push")
    bench_dvc("push", name="noop")

    shutil.rmtree(dataset)
    bench_dvc("checkout")
    shutil.rmtree(dataset)
    shutil.rmtree(tmp_dir / ".dvc" / "cache")

    bench_dvc("pull")
    bench_dvc("pull", name="noop")

    bench_dvc("checkout", name="noop")
    bench_dvc("remove", str(dataset) + ".dvc")

    os.makedirs("partial-copy")
    for f in glob.glob("*", root_dir=dataset, recursive=True):
        if random.random() > 0.5:
            shutil.move(dataset / f, tmp_dir / "partial-copy" / f)

    bench_dvc("add", dataset, name="partial-remove")
    bench_dvc("push", name="partial-remove")
    bench_dvc("gc", "-f", "-w")
    bench_dvc("gc", "-f", "-w", "-c", name="cloud")

    shutil.copytree("partial-copy", dataset, dirs_exist_ok=True)

    bench_dvc("add", dataset, name="partial-add")
    bench_dvc("push", name="partial-add")
    bench_dvc("gc", "-f", "-w", name="noop")
    bench_dvc("gc", "-f", "-w", "-c", name="cloud-noop")
