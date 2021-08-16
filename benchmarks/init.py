from benchmarks.base import BaseBench


class InitNoScmBench(BaseBench):
    def time_init(self):
        self.dvc("init", "--no-scm", proc=True)


class InitScmBench(BaseBench):
    def setup(self):
        super().setup()
        self.init_git()

    def time_init(self):
        self.dvc("init", proc=True)
