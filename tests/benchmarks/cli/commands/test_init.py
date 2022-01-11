import os
import shutil


def remove_dvc_root():
    dvc_root = ".dvc"
    if os.path.isdir(dvc_root):
        shutil.rmtree(".dvc")


def test_init(bench_dvc, tmp_dir, scm):
    bench_dvc("init", setup=remove_dvc_root, rounds=10, warmup_rounds=1)
