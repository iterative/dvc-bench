from benchmarks.base import BaseBench


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


class AddToCache(BaseBench):
    def setup(self):
        super().setup()
        self.data_url = self._remote_prefix + self.setup_data("mini")

    def time_add_to_cache(self):
        self.dvc("add", self.data_url, "-o", "mini", proc=True)
