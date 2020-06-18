import logging
import os
from collections import defaultdict
from contextlib import ExitStack
from tempfile import TemporaryDirectory

from git import Repo as GitRepo

from dvc.repo import Repo as DvcRepo

logger = logging.getLogger(__name__)


class component:
    def __init__(self, params):
        self.params = params

    def __getitem__(self, item):
        return self.params[item]

    def __setitem__(self, key, value):
        self.params[key] = value


class tmp_dir(component):
    def __enter__(self):
        self.startup_dir = os.getcwd()
        self.benchmark_dir = TemporaryDirectory(prefix="dvc_benchmark")
        self["path"] = self.benchmark_dir.name
        os.chdir(self.benchmark_dir.name)
        logger.error(f"enter tmp_dir: {os.getcwd()}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.startup_dir)
        logger.error(f"exit tmp_dir: {os.getcwd()}")
        self.benchmark_dir.cleanup()


class dvc(component):
    def __enter__(self):
        if self["git"]:
            self["dvc"] = DvcRepo.init()
        else:
            self["dvc"] = DvcRepo.init(no_scm=True)
        logger.error(f"enter dvc: {str(self['dvc'])}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self["dvc"].close()
        logger.error(f"exit dvc: {str(self['dvc'])}")


class git(component):
    def __enter__(self):
        self["git"] = GitRepo.init(os.getcwd())
        logger.error(f"enter git: {str(self['git'])}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self["git"].close()
        logger.error(f"exit git")


class Bench:
    warmup_time = 0
    number = 1
    repeat = (6, 12, 60.0)
    processes = max(2, os.cpu_count() - 1)

    components = []

    def setup(self):
        self.manager = ExitStack()
        params = defaultdict(None)
        for c in self.components:
            self.manager.enter_context(c(params))

    def teardown(self):
        self.manager.close()


class TestBench(Bench):
    components = [tmp_dir, git, dvc]

    def time_anything(self):
        logger = logging.getLogger(__name__)
        logger.warning(os.getcwd())
