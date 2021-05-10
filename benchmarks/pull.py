from benchmarks.base import BaseRemoteBench


class DVCPullBench(BaseRemoteBench):
    repeat = 1
    timeout = 12000

    def setup(self):
        super().setup()

        self.setup_data("cats_dogs", name="data", fs="local")
        self.dvc("add", "data", "--quiet")
        self.dvc("push", "data", "--quiet")

    def time_cats_dogs(self):
        self.dvc("pull", "-j", "2", proc=True)
