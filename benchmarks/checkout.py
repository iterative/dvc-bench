import shutil

from benchmarks.base import BaseBench


class CheckoutBench(BaseBench):
    repeat = 3

    params = ["copy", "symlink", "hardlink"]
    param_names = ["link_type"]

    def setup(self, link_type):
        super().setup()

        self.init_git()
        self.init_dvc()

        self.dvc("config", "cache.type", link_type, "--quiet")

        self.gen("data", template="cats_dogs")
        self.dvc("add", "data", "--quiet")
        shutil.rmtree("data")

    def time_cats_dogs(self, link_type):
        self.dvc("checkout", "data.dvc", proc=True)
