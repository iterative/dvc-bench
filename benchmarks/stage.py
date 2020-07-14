import shutil

from benchmarks.base import BaseBench, init_dvc, random_data_dir
from dvc.main import main


class CollectBench(BaseBench):
    repeat = 1
    number = 3

    def setup(self):
        super().setup()
        self.repo = init_dvc(self.test_directory.name)
        dataset_path = random_data_dir(2000, 1024 ** 2)
        shutil.copytree(dataset_path, "data")
        assert main(["add", "-R", "data", "--quiet"]) == 0
        assert main(["status", "--quiet"]) == 0

    def time_stages_collection(self):
        assert main(["status", "--quiet"]) == 0
