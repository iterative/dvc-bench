import os
import shutil

from benchmarks.base import DATA_TEMPLATES, BaseBench
from dvc.ignore import DvcIgnore


class DVCStatusBench(BaseBench):
    repeat = 1
    number = 100

    def setup(self):
        super().setup()
        self.directory.init_git()
        self.directory.init_dvc()
        data_path = DATA_TEMPLATES["large"]
        os.makedirs(os.path.join(self.directory.path, "data"), exist_ok=True)
        self.dvc("add", "data", "--quiet")
        shutil.copytree(data_path, os.path.join("data", "data"))
        # calculating md5
        self.dvc("status", "--quiet", return_code=1)

    def time_status(self):
        self.dvc("status", "--quiet", return_code=1, proc=True)


class DVCIgnoreBench(DVCStatusBench):
    @staticmethod
    def add_ignore_rules(path, number):
        with open(os.path.join(path, DvcIgnore.DVCIGNORE_FILE), "w",) as f_w:
            for i in range(number):
                f_w.write("{}\n".format(i))

    def setup(self):
        super().setup()
        self.add_ignore_rules(self.directory.path, 30)
