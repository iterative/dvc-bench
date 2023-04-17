import glob
import os
import random
import shutil


def test_sharing(bench_dvc, tmp_dir, dvc, dataset, remote):
    # Move some files to create a partial dataset
    os.makedirs("partial-copy")
    for f in glob.glob("*", root_dir=dataset, recursive=True):
        if random.random() > 0.5:
            shutil.move(dataset / f, tmp_dir / "partial-copy" / f)

    # Add/push partial dataset
    dvc.add(str(dataset))
    dvc.push()

    # Add more files to the dataset
    shutil.copytree("partial-copy", dataset, dirs_exist_ok=True)

    # Benchmark operations for adding files to a dataset
    bench_dvc("add", dataset, name="partial-add")
    bench_dvc("push", name="partial-add")
    bench_dvc("gc", "-f", "-w", name="noop")
    bench_dvc("gc", "-f", "-w", "-c", name="cloud-noop")
