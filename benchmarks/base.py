import os
import shutil
import stat
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from multiprocessing import cpu_count
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory, gettempdir

import shortuuid

from benchmarks.config import config
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
        if exist_ok and os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        shutil.copytree(DATA_TEMPLATES[template], repo_path)

    def _cleanup_tmp(self):
        assert self.processes == 1

        tmp = gettempdir()
        tmp_ls = os.listdir(tmp)
        for path in tmp_ls:
            if path.startswith("benchmark_") and os.path.isdir(path):
                shutil.rmtree(os.path.join(tmp, path))
            elif path.startswith("tmp") and os.path.isfile(path):
                os.remove(os.path.join(tmp, path))


ALIASES = {"azure": "az"}


@lru_cache(32)
def get_fs(filesystem, **kwargs):
    import fsspec

    try:
        return fsspec.filesystem(ALIASES.get(filesystem, filesystem), **kwargs)
    except ImportError as exc:
        raise NotImplementedError from exc


class BaseRemoteBench(BaseBench):

    # For benchmarks that interact with remotes
    # only run them once
    repeat = 1
    timeout = 12_000

    params = config["remotes"].keys()

    DEFAULT_REMOTE = "storage"

    def setup(self, remote_type):
        super().setup()
        self.init_git()
        self.init_dvc()

        self.remote_type = remote_type
        self.remote_options = self.setup_remote(remote_type)

    def setup_remote(self, remote):
        # If setup raises a NotImplementedError, the
        # benchmark is marked as skipped.
        if remote not in config["remotes"]:
            raise NotImplementedError

        remote_map = {}
        remote_map["config"] = config["remotes"][remote].copy()
        remote_map["base"] = (
            f"{remote}://{remote_map['config'].pop('url')}"
            f"/temp-benchmarks-storage-{shortuuid.uuid()}"
        )
        remote_map["data"] = f"{remote_map['base']}/data"

        self.dvc(
            "remote", "add", "-d", self.DEFAULT_REMOTE, remote_map["base"]
        )
        for key, value in remote_map["config"].items():
            self.dvc("remote", "modify", "storage", key, value)

        return remote_map

    def wrap(self, url):
        """Wrap the normal URL in the form of azure://{url}/{something}
        to remote://{remote}/{something}"""
        from fsspec.utils import infer_storage_options

        url_params = infer_storage_options(url)
        remote_url_params = infer_storage_options(self.remote_options["base"])

        url = url_params["host"] + url_params["path"]
        remote_url = remote_url_params["host"] + remote_url_params["path"]

        if url.startswith(remote_url):
            return f"remote://{self.DEFAULT_REMOTE}/{url[len(remote_url):]}"
        else:
            raise ValueError(f"url {url!r} doesn't match with {remote_url!r}")

    def setup_data(self, template, url=None, wrap=False):
        fs = get_fs(self.remote_type, **self.remote_options["config"])
        if url is None:
            url = (
                f"{self.remote_options['data']}/{template}-{shortuuid.uuid()}"
            )

        fs.put(DATA_TEMPLATES[template], url, recursive=True)
        if wrap:
            url = self.wrap(url)
        return wrap
