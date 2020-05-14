import os

from dvc.main import main
from tempfile import TemporaryDirectory


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
        from git import Repo

        git = Repo.init(self.test_directory.name)
        git.close()

    def time_init(self):
        main(["init"])
