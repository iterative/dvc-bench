from benchmarks.base import BaseRemoteBench


class PushBench(BaseRemoteBench):
    def setup(self, remote):
        super().setup(remote)

        self.gen("data", template="cats_dogs")
        self.dvc("add", "data")

    def time_cats_dogs(self, _):
        self.dvc("push", "-j", "2", proc=True)
