import contextlib
import functools
import os.path
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

import pytest
from git import Repo as GitRepo

import dvc.main as dvc_main
from dvc.repo import Repo as DvcRepo


def sources_dir():
    path = os.path.join(tempfile.gettempdir(), "sources")
    os.makedirs(path, exist_ok=True)
    return path


@functools.lru_cache(None)
def get_data_for_file(path, file_size):
    # This function will generate the same data for the same path,
    # which would allow to make datasets grow on top of the existing
    # ones. The `path` is a key to this function"s caching system, and
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


@contextlib.contextmanager
def chdir(path):
    cur_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cur_dir)


def invoke_proc(*args, return_code=0):
    p = subprocess.Popen(args, env=os.environ)
    p.communicate()
    assert p.returncode == return_code


def invoke_git(*args, return_code=0):
    invoke_proc(*("git", *args), return_code=return_code)


root = os.path.abspath(os.path.join(__file__, "..", ".."))


# fixtures


@pytest.fixture
def git(tmpdir):
    GitRepo.init(tmpdir).close()

    yield invoke_git


@pytest.fixture
def git_clone(tmpdir, request):
    url, tag = request.param
    invoke_git(
        "clone", "--branch", tag, "--single-branch", url, tmpdir
    )

    yield invoke_git


@pytest.fixture
def dvc(tmpdir):
    no_scm = not os.path.exists(os.path.join(tmpdir, ".git"))

    def setup():
        DvcRepo.init(tmpdir, no_scm=no_scm).close()

    def invoke_dvc(*args, return_code=0, proc=False):
        if proc:
            invoke_proc(*("dvc", *args), return_code=return_code)
        else:
            assert dvc_main.main(args) == return_code

    def reset(proc=False):
        invoke_dvc("destroy", "-f", proc=proc)
        setup()

    invoke_dvc.reset = reset

    setup()

    return invoke_dvc


def generate_data_fixture(name, data):
    @pytest.fixture
    def fixture(tmpdir):
        path = tmpdir / name
        shutil.copytree(data, path)
        try:
            with chdir(tmpdir):
                yield name
        finally:
            # remove data because tmpdir is kept on disk after the run
            if os.path.exists(path):
                shutil.rmtree(path)

    return fixture


# generate data_100x1024, data_200x1024, etc. fixtures
# https://github.com/pytest-dev/pytest/issues/2424
for name, data in (
    ("100x1024", random_data_dir(100, 1024)),
    ("200x1024", random_data_dir(200, 1024)),
    ("small", random_data_dir(2000, 1024)),
    ("medium", random_data_dir(5000, 1024)),
    ("large", random_data_dir(10000, 1024)),
    ("cats_dogs", os.path.join(root, "data", "cats_dogs")),
):
    # need a generation function for this because `name` and `data` will be
    # bound to the current scope. if we declared the function here, `name` and
    # `data` would take the last value of the loop.
    globals()[f"data_{name}"] = generate_data_fixture(name, data)
