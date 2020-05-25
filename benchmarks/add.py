import shutil

from dvc.main import main

from benchmarks.base import BaseBench, init_dvc, random_data_dir


class Add_100_1M_copy(BaseBench):
    def setup(self):
        super().setup()
        self.repo = init_dvc(self.test_directory.name)
        dataset_path = random_data_dir(100, 1024 * 1024)
        shutil.copytree(dataset_path, "data")

    def time_add(self):
        assert main(["add", "data"]) == 0


class Add_100_1M_symlink(Add_100_1M_copy):
    def setup(self):
        super().setup()
        assert main(["config", "cache.type", "symlink"]) == 0


class Add_100_1M_hardlink(Add_100_1M_copy):
    def setup(self):
        super().setup()
        assert main(["config", "cache.type", "hardlink"]) == 0
