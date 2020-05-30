import shutil
import os
from benchmarks.base import BaseBench, init_dvc, random_data_dir
from dvc.main import main
from dvc.ignore import DvcIgnore


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
        dataset_path = random_data_dir(40000, 10)
        shutil.copytree(dataset_path, "data")
        assert main(["add", "data"]) == 0

    def time_status(self):
        assert main(["status"]) == 0


class DVCIgnore10Rules(DVCIgnoreEmpty):
    def setup(self):
        super().setup()
        self.add_ignore_rules(10)


class DVCIgnore100Rules(DVCIgnoreEmpty):
    def setup(self):
        super().setup()
        self.add_ignore_rules(100)
