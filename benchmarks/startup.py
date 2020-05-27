from subprocess import PIPE, Popen

from benchmarks.base import BaseBench


class StartupBench(BaseBench):
    def time_startup(self):
        proc = Popen(["dvc", "--help"], stdout=PIPE)
        proc.communicate()
        assert proc.returncode == 0
