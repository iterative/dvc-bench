import shortuuid

from benchmarks.base import BaseBench


class PushBench(BaseBench):
    repeat = 1
    timeout = 12000

    def setup(self):
        super().setup()

        self.directory.init_git()
        self.directory.init_dvc()

        self.remote_url = (
            f"s3://dvc-temp/dvc-bench/tmp-benchmarks-cache-{shortuuid.uuid()}"
        )
        self.dvc("remote", "add", "-d", "storage", self.remote_url)

        self.directory.gen("data", template="cats_dogs")
        self.dvc("add", "data", "--quiet")

    def time_cats_dogs(self):
        self.dvc("push", "-j", "2", proc=True)
