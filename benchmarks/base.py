import os
import stat
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from tempfile import TemporaryDirectory, gettempdir


def sources_dir():
    path = os.path.join(gettempdir(), "sources")
    os.makedirs(path, exist_ok=True)
    return path


class BaseBench:
    warmup_time = 0
    number = 1
    repeat = (3, 5, 60.0)
    processes = max(2, cpu_count() - 1)
    timeout = 300

    def setup(self):
        self.cwd = os.getcwd()
        self.test_directory = TemporaryDirectory(prefix="DVCBenchmark")
        os.chdir(self.test_directory.name)

    def teardown(self):
        os.chdir(self.cwd)

        if hasattr(self, "repo"):
            self.repo.close()

        if os.name == "nt":
            # Windows does not allow to remove read only files
            for root, _, files in os.walk(self.test_directory.name):
                for file in files:
                    path = os.path.join(root, file)
                    perm = os.stat(path).st_mode | stat.S_IWRITE
                    os.chmod(path, perm)

        self.test_directory.cleanup()


def init_git(path):
    from git import Repo

    git = Repo.init(path)
    git.close()


def init_dvc(path, git=True):
    from dvc.repo import Repo

    if git:
        init_git(path)
        repo = Repo.init(path)
        repo.scm.commit("Init DVC repo")
    else:
        repo = Repo.init(path, no_scm=True).close()
    return repo


def random_file(path, file_size):
    with open(path, "wb") as fobj:
        fobj.write(os.urandom(file_size))


def random_data_dir(num_files, file_size):
    dirname = "data_{}_{}".format(num_files, file_size)
    dir_path = os.path.join(sources_dir(), dirname)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        fnames = [
            os.path.join(dir_path, "file_{}".format(str(i)))
            for i in range(num_files)
        ]
        with ThreadPoolExecutor(max_workers=max(cpu_count() / 2, 2)) as pool:
            pool.map(random_file, fnames, len(fnames) * [file_size])
    return dir_path
