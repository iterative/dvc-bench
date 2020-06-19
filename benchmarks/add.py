from funcy import cached_property

from benchmarks.base import BaseBench, random_data_dir
from benchmarks.fixtures import DVC, TmpDir, cache_type, data_in_repo
from dvc.main import main


class Add_100_1M_copy(BaseBench):
    @cached_property
    def data_path(self):
        return random_data_dir(100, 1024 * 1024)

    @property
    def fixtures(self):
        return [TmpDir, DVC, data_in_repo(self.data_path, "data")]

    def time_add(self):
        assert main(["add", "data"]) == 0


class Add_100_1M_symlink(Add_100_1M_copy):
    @property
    def fixtures(self):
        return [
            TmpDir,
            DVC,
            data_in_repo(self.data_path, "data"),
            cache_type("symlink"),
        ]


class Add_100_1M_hardlink(Add_100_1M_copy):
    @property
    def fixtures(self):
        return [
            TmpDir,
            DVC,
            data_in_repo(self.data_path, "data"),
            cache_type("hardlink"),
        ]
