from subprocess import PIPE, Popen

from benchmarks.base import BaseBench


class StartupBench(BaseBench):
    number = 50
    repeat = (50, 100, 120.0)

    def time_startup(self):
        proc = Popen(["dvc", "--help"], stdout=PIPE)
        proc.communicate()
        assert proc.returncode == 0
