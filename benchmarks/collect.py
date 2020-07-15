from benchmarks.base import BaseBench


class CollectBench(BaseBench):
    repeat = 1
    number = 3

    def setup(self):
        super().setup()

        self.init_dvc()

        self.gen("data", template="small")
        self.dvc("add", "-R", "data", "--quiet")

        self.dvc("status", "--quiet")

    def time_stages_collection(self):
        self.dvc("status", "--quiet")
