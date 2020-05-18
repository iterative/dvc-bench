from dvc.main import main
from tempfile import TemporaryDirectory, gettempdir
import os
from git import Repo as GitRepo
from dvc.repo import Repo as DvcRepo
import shutil

DATA_SOURCES_DIR = os.path.join(gettempdir(), "data_sources")


class BaseBench:
    def setup(self):
        self.cwd = os.getcwd()
        self.test_directory = TemporaryDirectory(prefix="HelpSuite")
        os.chdir(self.test_directory.name)

    def teardown(self):
        os.chdir(self.cwd)
        self.test_directory.cleanup()


class InitNoScmBench(BaseBench):
    def time_init(self):
        main(["init", "--no-scm"])


class InitScmBench(BaseBench):
    def setup(self):
        super().setup()

        git = GitRepo.init(self.test_directory.name)
        git.close()

    def time_init(self):
        main(["init"])


class AITABench(BaseBench):
    def _download_resources(self):
        from dvc.repo import Repo

        os.makedirs(DATA_SOURCES_DIR, exist_ok=True)

        self.dataset_path = os.path.join(DATA_SOURCES_DIR, "aita.csv")
        if not os.path.exists(self.dataset_path):
            Repo.get(
                "https://github.com/iterative/aita_dataset",
                "aita_clean.csv",
                out=self.dataset_path,
                rev="lightweight",
            )

    def setup(self):
        super().setup()
        self._download_resources()

        git = GitRepo.init(self.test_directory.name)
        git.close()

        self.repo = DvcRepo.init(self.test_directory.name)

        self.data_path = os.path.join(self.test_directory.name, "aita.csv")

        shutil.copy(self.dataset_path, self.data_path)

    def time_add_copy(self):
        self.repo.add([self.data_path])
