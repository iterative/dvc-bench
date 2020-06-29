from subprocess import PIPE, Popen

from benchmarks.base import BaseBench


class StartupBench(BaseBench):
    number = 50
    repeat = 1

    def time_startup(self):
        proc = Popen(["dvc", "--help"], stdout=PIPE)
        proc.communicate()
        assert proc.returncode == 0
