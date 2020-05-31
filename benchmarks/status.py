import os
import shutil

from benchmarks.base import BaseBench, init_dvc, random_data_dir
from dvc.ignore import DvcIgnore
from dvc.main import main


class DVCIgnoreEmpty(BaseBench):
    def add_ignore_rules(self, number):
        with open(
            os.path.join(self.test_directory.name, DvcIgnore.DVCIGNORE_FILE),
            "w",
        ) as f_w:
            for i in range(number):
                f_w.write("{}\n".format(i))

    def setup(self):
        super().setup()
        self.repo = init_dvc(self.test_directory.name)
        dataset_path = random_data_dir(10000, 10)
        shutil.copytree(dataset_path, "data")
        assert main(["config", "cache.type", "symlink"]) == 0
        assert main(["add", "data"]) == 0

    def time_status(self):
        assert main(["status", "--quiet"]) == 0


class DVCIgnore3Rules(DVCIgnoreEmpty):
    def setup(self):
        super().setup()
        self.add_ignore_rules(3)


class DVCIgnore20Rules(DVCIgnoreEmpty):
    def setup(self):
        super().setup()
        self.add_ignore_rules(20)
