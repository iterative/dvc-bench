import logging
import os
import shutil

from benchmarks.base import BaseBench, init_dvc
from dvc.main import main

logger = logging.getLogger(__name__)


class AddCopy(BaseBench):
    repeat = 3

    def setup(self):
        super().setup()
        self.repo = init_dvc(self.test_directory.name)
        dataset_path = os.path.join(
            os.environ["ASV_CONF_DIR"], "data", "cats_dogs"
        )
        shutil.copytree(dataset_path, "data")

    def time_cats_dogs(self):
        assert main(["add", "data"]) == 0


class AddSymlink(AddCopy):
    def setup(self):
        super().setup()
        assert main(["config", "cache.type", "symlink"]) == 0


class AddHardlink(AddCopy):
    def setup(self):
        super().setup()
        assert main(["config", "cache.type", "hardlink"]) == 0
