import glob
import os
import random


def test_partial_remove(bench_dvc, tmp_dir, dvc, dataset, remote):
    # Add/push full dataset
    dvc.add(str(dataset))
    dvc.push()

    # Remove some files
    for f in glob.glob("*", root_dir=dataset, recursive=True):
        if random.random() > 0.5:
            os.remove(dataset / f)

    # Benchmark operations for removing files from dataset
    bench_dvc("add", dataset)
    bench_dvc("push")
    bench_dvc("gc", "-f", "-w")
    bench_dvc("gc", "-f", "-w", "-c", name="cloud")
