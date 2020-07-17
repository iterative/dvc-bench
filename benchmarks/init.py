from benchmarks.base import BaseBench, init_git


class InitNoScmBench(BaseBench):
    def time_init(self):
        self.dvc("init", "--no-scm")


class InitScmBench(BaseBench):
    def setup(self):
        super().setup()
        init_git(self.test_directory.name)

    def time_init(self):
        self.dvc("init", "--quiet")
