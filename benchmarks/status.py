import os
import shutil

from benchmarks.base import BaseBench, init_dvc, random_data_dir
from dvc.ignore import DvcIgnore
from dvc.main import main


class DVCIgnoreEmpty(BaseBench):
    def add_ignore_rules(self, path, number):
        with open(os.path.join(path, DvcIgnore.DVCIGNORE_FILE), "w",) as f_w:
            for i in range(number):
                f_w.write("{}\n".format(i))

    def setup(self):
        super().setup()
        self.repo = init_dvc(self.test_directory.name)
        dataset_path = random_data_dir(10000, 10)
        os.makedirs(
            os.path.join(self.test_directory.name, "data"), exist_ok=True
        )
        assert main(["add", "data", "--quiet"]) == 0
        shutil.copytree(dataset_path, "data/data")
        # calculating md5
        assert main(["status", "--quiet"]) == 1

    def time_status(self):
        assert main(["status", "--quiet"]) == 1


class DVCIgnore3Rules(DVCIgnoreEmpty):
    def setup(self):
        super().setup()
        self.add_ignore_rules(self.test_directory.name, 3)

    def time_status(self):
        assert main(["status", "--quiet"]) == 1


class DVCIgnore30Rules(DVCIgnoreEmpty):
    def setup(self):
        super().setup()
        self.add_ignore_rules(self.test_directory.name, 30)

    def time_status(self):
        assert main(["status", "--quiet"]) == 1


class DVCIgnore3x10Rules(DVCIgnoreEmpty):
    def setup(self):
        super().setup()
        data_path = os.path.join(self.test_directory.name, "data")
        data_data_path = os.path.join(data_path, "data")
        self.add_ignore_rules(self.test_directory.name, 10)
        self.add_ignore_rules(data_path, 10)
        self.add_ignore_rules(data_data_path, 10)

    def time_status(self):
        assert main(["status", "--quiet"]) == 1
