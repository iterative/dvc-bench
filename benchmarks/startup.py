from subprocess import PIPE, Popen

from benchmarks.base import BaseBench
from benchmarks.fixtures import TmpDir


class StartupBench(BaseBench):
    fixtures = [TmpDir]

    def time_startup(self):
        proc = Popen(["dvc", "--help"], stdout=PIPE)
        proc.communicate()
        assert proc.returncode == 0
