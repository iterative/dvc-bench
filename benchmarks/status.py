import os
import shutil

from benchmarks.base import BaseBench, init_dvc, random_data_dir
from dvc.ignore import DvcIgnore
from dvc.main import main


class DVCIgnore(BaseBench):
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
        os.makedirs(os.path.join(self.test_directory.name, 'data'), exist_ok=True)
        assert main(["add", "data", "--quiet"]) == 0
        shutil.copytree(dataset_path, "data/data")
        # calculating md5
        assert main(["status", "--quiet"]) == 1

    def time_status_empty(self):
        self.add_ignore_rules(0)
        assert main(["status", "--quiet"]) == 1

    def time_status_3_rules(self):
        self.add_ignore_rules(3)
        assert main(["status", "--quiet"]) == 1

    def time_status_20_rules(self):
        self.add_ignore_rules(20)
        assert main(["status", "--quiet"]) == 1

