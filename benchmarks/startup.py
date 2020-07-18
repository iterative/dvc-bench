from benchmarks.base import BaseBench


class StartupBench(BaseBench):
    number = 100
    repeat = 1

    def time_startup(self):
        self.dvc("--help", proc=True)
