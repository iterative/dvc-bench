import os
import shutil
import stat
from tempfile import TemporaryDirectory

from git import Repo as GitRepo

from dvc.main import main
from dvc.repo import Repo as DvcRepo


class Fixture:
    def requires(self, *fixture_classes):
        for cls in fixture_classes:
            assert self[cls.__name__]

    def __init__(self, params):
        self.params = params

    def __getitem__(self, item):
        return self.params[item]

    def __setitem__(self, key, value):
        self.params[key] = value

    def store(self, val):
        self[self.__class__.__name__] = val

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class TmpDir(Fixture):
    def __enter__(self):
        self.startup_dir = os.getcwd()
        self.benchmark_dir = TemporaryDirectory(prefix="dvc_benchmark")
        self.store(self.benchmark_dir.name)
        os.chdir(self.benchmark_dir.name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.startup_dir)

        if os.name == "nt":
            # Windows does not allow to remove read only files
            for root, _, files in os.walk(self.benchmark_dir.name):
                for file in files:
                    path = os.path.join(root, file)
                    perm = os.stat(path).st_mode | stat.S_IWRITE
                    os.chmod(path, perm)

        self.benchmark_dir.cleanup()


class DVC(Fixture):
    def __enter__(self):
        self.requires(TmpDir)
        if "Git" in self.params.keys():
            self.dvc = DvcRepo.init()
        else:
            self.dvc = DvcRepo.init(no_scm=True)
        self.store(self.dvc)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dvc.close()


class Git(Fixture):
    def __enter__(self):
        self.requires(TmpDir)
        self.git = GitRepo.init(self["TmpDir"])
        self.store(self.git)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.git.close()


def data_in_repo(path, path_in_repo="data"):
    class DataInRepo(Fixture):
        def __enter__(self):
            self.requires(TmpDir)
            shutil.copytree(path, os.path.join(self["TmpDir"], path_in_repo))

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    return DataInRepo


def cache_type(type):
    class CacheType(Fixture):
        def __enter__(self):
            self.requires(TmpDir, DVC)
            assert main(["config", "cache.type", type]) == 0
            self["DVC"] = DvcRepo(self["TmpDir"])

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    return CacheType
