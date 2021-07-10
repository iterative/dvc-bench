import shutil

import pytest

from benchmarks.base import BaseBench


@pytest.mark.parametrize(
    "link_type", ("copy", "symlink", "hardlink"),
)
def benchmark_checkout_cats_dogs(
    benchmark, git, dvc, link_type, data_cats_dogs
):
    dvc("config", "cache.type", link_type)
    dvc("add", "cats_dogs")

    benchmark.pedantic(
        dvc,
        setup=lambda: shutil.rmtree("cats_dogs"),
        args=("checkout", "cats_dogs.dvc"),
        kwargs={"proc": True},
    )


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
