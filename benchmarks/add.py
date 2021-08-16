from benchmarks.base import BaseBench, BaseRemoteBench


class Add(BaseBench):
    repeat = 3

    params = ["copy", "symlink", "hardlink"]
    param_names = ["link_type"]

    def setup(self, link_type):
        super().setup()

        self.init_git()
        self.init_dvc()

        self.gen("data", template="cats_dogs")

        self.dvc("config", "cache.type", link_type)

    def time_cats_dogs(self, link_type):
        self.dvc("add", "data", proc=True)


class AddToCache(BaseRemoteBench):
    def setup(self, remote):
        super().setup(remote)
        self.data_url = self.setup_data("100x1024")

    def time_add_to_cache(self, _):
        self.dvc("add", self.data_url, "-o", "mini", proc=True)
