import os
import shutil
import stat
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from multiprocessing import cpu_count
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory, gettempdir

import shortuuid
from funcy import cached_property

from dvc.main import main


def sources_dir():
    path = os.path.join(gettempdir(), "sources")
    os.makedirs(path, exist_ok=True)
    return path


@lru_cache(None)
def get_data_for_file(path, file_size):
    # This function will generate the same data for the same path,
    # which would allow to make datasets grow on top of the existing
    # ones. The `path` is a key to this function's caching system, and
    # even if it is not used, it needs to be present in the signature to
    # allow cache lookups.
    return os.urandom(file_size)


def random_file(path, file_size):
    with open(path, "wb") as fobj:
        fobj.write(get_data_for_file(path, file_size))


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
    "100x1024": random_data_dir(100, 1024),
    "200x1024": random_data_dir(200, 1024),
    "small": random_data_dir(2000, 1024),
    "medium": random_data_dir(5000, 1024),
    "large": random_data_dir(10000, 1024),
    "cats_dogs": os.path.join(os.environ["ASV_CONF_DIR"], "data", "cats_dogs"),
}


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
        self.test_directory = TemporaryDirectory(
            prefix="benchmark_{}_".format(self.__class__.__name__)
        )
        os.chdir(self.path)

    @property
    def path(self):
        return self.test_directory.name

    def teardown(self, *params):
        os.chdir(self.cwd)

        if hasattr(self, "repo"):
            self.repo.close()

        if os.name == "nt":
            # Windows does not allow to remove read only files
            for root, _, files in os.walk(self.path):
                for file in files:
                    path = os.path.join(root, file)
                    perm = os.stat(path).st_mode | stat.S_IWRITE
                    os.chmod(path, perm)

        self.test_directory.cleanup()

    def dvc(self, *args, return_code=0, proc=False):
        if proc:
            self.proc(*["dvc", *args], return_code=return_code)
        else:
            assert main(args) == return_code

    def proc(self, *args, return_code=0):
        p = Popen(args, stdout=PIPE, env=os.environ)
        p.communicate()
        assert p.returncode == return_code

    def init_git(self):
        from git import Repo

        Repo.init(self.path).close()

    def init_dvc(self):
        from dvc.repo import Repo

        no_scm = not os.path.exists(".git")
        Repo.init(self.path, no_scm=no_scm).close()

    def gen(self, repo_path, template, exist_ok=False):
        shutil.copytree(
            DATA_TEMPLATES[template], repo_path, dir_exist_ok=exist_ok
        )

    def _cleanup_tmp(self):
        assert self.processes == 1

        tmp = gettempdir()
        tmp_ls = os.listdir(tmp)
        for path in tmp_ls:
            if path.startswith("benchmark_") and os.path.isdir(path):
                shutil.rmtree(os.path.join(tmp, path))
            elif path.startswith("tmp") and os.path.isfile(path):
                os.remove(os.path.join(tmp, path))


class BaseRemoteBench(BaseBench):

    _remote_prefix = "s3://"
    _remote_dir = "dvc-temp/dvc-bench"

    def setup(self):
        super().setup()

        self.init_git()
        self.init_dvc()

        remote_url = (
            self._remote_prefix
            + self._remote_dir
            + f"/temp-benchmarks-cache-{shortuuid.uuid()}"
        )
        self.dvc("remote", "add", "-d", "storage", remote_url)

    def setup_data(self, template, name=None):
        if name is None:
            name = template
        else:
            name = f"data-{name}-{shortuuid.uuid()}"

        data_url = self._remote_dir + f"/tmp-benchmarks-data/{name}"
        if self.fs.exists(data_url):
            return data_url

        local_url = f"_tmp_data_{template}"
        self.gen(local_url, template, exist_ok=True)

        self.fs.put(local_url, data_url, recursive=True)
        shutil.rmtree(local_url)
        return data_url

    @cached_property
    def fs(self):
        from s3fs import S3FileSystem

        return S3FileSystem()
