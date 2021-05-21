from benchmarks.base import BaseRemoteBench


class PushBench(BaseRemoteBench):
    repeat = 1
    timeout = 12000

    def setup(self, remote):
        super().setup(remote)

        self.gen("data", template="cats_dogs")
        self.dvc("add", "data", "--quiet")

    def time_cats_dogs(self, _):
        self.dvc("push", "-j", "2", proc=True)
