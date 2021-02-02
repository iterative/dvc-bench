import os
import shutil
import stat
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory, gettempdir

from dvc.main import main


def sources_dir():
    path = os.path.join(gettempdir(), "sources")
    os.makedirs(path, exist_ok=True)
    return path


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


DATA_TEMPLATES = {
    "small": random_data_dir(2000, 1024),
    "large": random_data_dir(10000, 1024),
    "cats_dogs": os.path.join(os.environ["ASV_CONF_DIR"], "data", "cats_dogs"),
}


class TmpDir:
    def __init__(self, name):
        self._tmp_dir = TemporaryDirectory(prefix="benchmark_{}_".format(name))

    @property
    def path(self):
        return self._tmp_dir.name

    def init_git(self):
        from git import Repo

        Repo.init(self.path).close()

    def init_dvc(self):
        from dvc.repo import Repo

        no_scm = not os.path.exists(".git")
        Repo.init(self.path, no_scm=no_scm).close()

    def gen(self, repo_path, template):
        shutil.copytree(DATA_TEMPLATES[template], repo_path)

    def cleanup(self):
        if hasattr(self, "repo"):
            self.repo.close()

        if os.name == "nt":
            # Windows does not allow to remove read only files
            for root, _, files in os.walk(self.path):
                for file in files:
                    path = os.path.join(root, file)
                    perm = os.stat(path).st_mode | stat.S_IWRITE
                    os.chmod(path, perm)
        self._tmp_dir.cleanup()


class BaseBench:
    warmup_time = 0
    number = 1
    repeat = 50
    processes = 1
    timeout = 300

    def __init__(self):
        os.environ["DVC_TEST"] = "1"

    def setup(self, *params):
        # workaround for gha not using teardown
        self._cleanup_tmp()
        self.project_dir = os.environ["ASV_CONF_DIR"]
        self.cwd = os.getcwd()
        self.directory = TmpDir(self.__class__.__name__)
        os.chdir(self.directory.path)

    def teardown(self, *params):
        os.chdir(self.cwd)
        self.directory.cleanup()

    def dvc(self, *args, return_code=0, proc=False):
        if proc:
            self.proc(*["dvc", *args], return_code=return_code)
        else:
            assert main(args) == return_code

    def proc(self, *args, return_code=0):
        p = Popen(args, stdout=PIPE, env=os.environ)
        p.communicate()
        assert p.returncode == return_code

    def _cleanup_tmp(self):
        assert self.processes == 1

        tmp = gettempdir()
        tmp_ls = os.listdir(tmp)
        for path in tmp_ls:
            if path.startswith("benchmark_") and os.path.isdir(path):
                shutil.rmtree(os.path.join(tmp, path))
            elif path.startswith("tmp") and os.path.isfile(path):
                os.remove(os.path.join(tmp, path))
