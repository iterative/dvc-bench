from subprocess import Popen

import shortuuid

from benchmarks.base import BaseBench


class PushBench(BaseBench):
    repeat = 1
    timeout = 1000

    def setup(self):
        super().setup()

        self.init_git()
        self.init_dvc()

        self.remote_url = (
            f"s3://dvc-bench/tmp-benchmarks-cache-{shortuuid.uuid()}"
        )
        self.dvc("remote", "add", "-d", "storage", self.remote_url)

        self.gen("data", template="cats_dogs")
        self.dvc("add", "data", "--quiet")

    def teardown(self, *params):
        Popen(
            ["aws", "s3", "rm", self.remote_url, "--recursive"], close_fds=True
        )

    def time_cats_dogs(self):
        self.dvc("push", "-j", "2")
