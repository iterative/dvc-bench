import pytest

from benchmarks.base import BaseBench, BaseRemoteBench


@pytest.mark.parametrize(
    "link_type", ("copy", "symlink", "hardlink"),
)
def benchmark_add_cats_dogs(benchmark, git, dvc, link_type, data_cats_dogs):
    dvc("config", "cache.type", link_type)

    benchmark.pedantic(
        dvc, setup=dvc.reset, args=("add", "cats_dogs"), kwargs={"proc": True},
    )


class Add(BaseBench):
    repeat = 3

    params = ["copy", "symlink", "hardlink"]
    param_names = ["link_type"]

    def setup(self, link_type):
        super().setup()

        self.init_git()
        self.init_dvc()

        self.gen("data", template="cats_dogs")

        self.dvc("config", "cache.type", link_type, "--quiet")

    def time_cats_dogs(self, link_type):
        self.dvc("add", "data", "--quiet", proc=True)


class AddToCache(BaseRemoteBench):
    def setup(self, remote):
        super().setup(remote)
        self.data_url = self.setup_data("100x1024")

    def time_add_to_cache(self, _):
        self.dvc("add", self.data_url, "-o", "mini", proc=True)
