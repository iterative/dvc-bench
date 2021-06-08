from benchmarks.base import BaseBench, BaseRemoteBench


class GCBench(BaseBench):
    repeat = 1
    timeout = 12000

    def setup(self):
        super().setup()

        self.init_git()
        self.init_dvc()

        self.gen("data", "cats_dogs")
        self.dvc("add", "data", "--quiet")
        self.dvc("push", "data", "--quiet")

        # remove everything from the local system
        self.dvc("remove", "data.dvc")
        self.dvc("gc", "-w")

    def time_gc(self):
        self.dvc("gc", "-f", "-w", proc=True)


class CloudGCBench(BaseRemoteBench):
    def setup(self, remote):
        super().setup(remote)

        self.gen("data", "large")
        self.dvc("add", "data", "--quiet")
        self.dvc("push", "data", "--quiet")

        # remove everything from the local system
        self.dvc("remove", "data.dvc")
        self.dvc("gc", "-w")

    def time_gc_cloud(self, _):
        self.dvc("gc", "-c", "-f", "-w", proc=True)
