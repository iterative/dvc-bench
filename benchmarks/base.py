import os
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from tempfile import gettempdir, TemporaryDirectory


def sources_dir():
    path = os.path.join(gettempdir(), "sources")
    os.makedirs(path, exist_ok=True)
    return path


class BaseBench:
    def setup(self):
        self.cwd = os.getcwd()
        self.test_directory = TemporaryDirectory(prefix="DVCBenchmark")
        os.chdir(self.test_directory.name)

    def teardown(self):
        os.chdir(self.cwd)
        self.test_directory.cleanup()


def init_git(path):
    from git import Repo

    git = Repo.init(path)
    git.close()


def init_dvc(path, git=True):
    from dvc.repo import Repo
    from dvc.main import main

    if git:
        init_git(path)
        repo = Repo.init(path)
        repo.scm.commit("Init DVC repo")
    else:
        repo = Repo.init(path, no_scm=True)

    main(["config", "core.analytics", "false"])
    return repo


def random_file(path, file_size):
    with open(path, "wb") as fobj:
        fobj.write(os.urandom(file_size))


def random_data_dir(num_files, file_size):
    dirname = "data_{}_{}".format(num_files, file_size)
    dir_path = os.path.join(sources_dir(), dirname)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        filenames = [
            os.path.join(dir_path, "file_{}".format(str(i))) for i in range(num_files)
        ]
        with ThreadPoolExecutor(max_workers=max(cpu_count() / 2, 2)) as executor:
            executor.map(random_file, filenames, len(filenames) * [file_size])
    return dir_path
