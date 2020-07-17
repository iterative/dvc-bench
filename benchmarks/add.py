import logging
import os
import shutil

from benchmarks.base import BaseBench, init_dvc
from dvc.main import main

logger = logging.getLogger(__name__)


class Add(BaseBench):
    repeat = 3

    params = ["copy", "symlink", "hardlink"]
    param_names = ["link_type"]

    def setup(self, link_type):
        super().setup()
        self.repo = init_dvc(self.test_directory.name)
        dataset_path = os.path.join(
            os.environ["ASV_CONF_DIR"], "data", "cats_dogs"
        )
        shutil.copytree(dataset_path, "data")
        assert main(["config", "cache.type", link_type]) == 0

    def time_cats_dogs(self, link_type):
        assert main(["add", "data"]) == 0
