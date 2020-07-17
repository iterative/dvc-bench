import os
import shutil

from benchmarks.base import BaseBench, init_dvc, random_data_dir
from dvc.ignore import DvcIgnore


class DVCStatusBench(BaseBench):
    repeat = 1
    number = 100

    def setup(self):
        super().setup()
        self.repo = init_dvc(self.test_directory.name)
        dataset_path = random_data_dir(10000, 10)
        os.makedirs(
            os.path.join(self.test_directory.name, "data"), exist_ok=True
        )
        self.dvc("add", "data", "--quiet")
        shutil.copytree(dataset_path, "data/data")
        # calculating md5
        self.dvc("status", "--quiet", return_code=1)

    def time_status(self):
        self.dvc("status", "--quiet", return_code=1)


class DVCIgnoreBench(DVCStatusBench):
    @staticmethod
    def add_ignore_rules(path, number):
        with open(os.path.join(path, DvcIgnore.DVCIGNORE_FILE), "w",) as f_w:
            for i in range(number):
                f_w.write("{}\n".format(i))

    def setup(self):
        super().setup()
        self.add_ignore_rules(self.test_directory.name, 30)
