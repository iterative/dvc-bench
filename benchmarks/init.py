from benchmarks.base import BaseBench
from benchmarks.fixtures import Git, TmpDir
from dvc.main import main


class InitNoScmBench(BaseBench):
    fixtures = [TmpDir]

    def time_init(self):
        assert main(["init", "--no-scm"]) == 0


class InitScmBench(BaseBench):
    fixtures = [TmpDir, Git]

    def time_init(self):
        assert main(["init"]) == 0
