from dvc.main import main

from benchmarks.base import BaseBench, init_git


class InitNoScmBench(BaseBench):
    def time_init(self):
        assert main(["init", "--no-scm"]) == 0


class InitScmBench(BaseBench):
    def setup(self):
        super().setup()
        init_git(self.test_directory.name)

    def time_init(self):
        assert main(["init"]) == 0
