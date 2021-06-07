import os
import shutil

from benchmarks.base import BaseRemoteBench


class PullBench(BaseRemoteBench):
    def setup(self, remote):
        super().setup(remote)

        self.gen("data", "cats_dogs")
        self.dvc("add", "data", "--quiet")
        self.dvc("push", "data", "--quiet")

        shutil.rmtree("data")
        shutil.rmtree(os.path.join(".dvc", "cache"))

    def time_cats_dogs(self, _):
        self.dvc("pull", "-j", "2", proc=True)
