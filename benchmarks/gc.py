from benchmarks.base import BaseRemoteBench


class GCBench(BaseRemoteBench):
    repeat = 1
    timeout = 12000

    def setup(self):
        super().setup()

        self.gen("data", "cats_dogs")
        self.dvc("add", "data", "--quiet")
        self.dvc("push", "data", "--quiet")

        # remove everything from the local system
        self.dvc("remove", "data.dvc")
        self.dvc("gc", "-w")

    def time_gc(self):
        self.dvc("gc", "-f", "-w", proc=True)


class CloudGCBench(BaseRemoteBench):
    repeat = 1
    timeout = 12000

    def setup(self):
        super().setup()

        self.gen("data", "large")
        self.dvc("add", "data", "--quiet")
        self.dvc("push", "data", "--quiet")

        # remove everything from the local system
        self.dvc("remove", "data")
        self.dvc("gc", "-w")

    def time_gc_cloud(self):
        self.dvc("gc", "-c", "-f", "-w", proc=True)
