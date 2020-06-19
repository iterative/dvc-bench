import os
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
from multiprocessing import cpu_count
from tempfile import gettempdir


def sources_dir():
    path = os.path.join(gettempdir(), "sources")
    os.makedirs(path, exist_ok=True)
    return path


class BaseBench:
    warmup_time = 0
    number = 1
    repeat = (3, 5, 60.0)
    processes = max(2, os.cpu_count() - 1)
    timeout = 300

    @property
    def fixtures(self):
        raise NotImplementedError

    def setup(self):
        self.fixture_stack = ExitStack()
        self.params = {}
        for fixture in self.fixtures:
            self.fixture_stack.enter_context(fixture(self.params))

    def teardown(self):
        self.fixture_stack.close()


def random_file(path, file_size):
    with open(path, "wb") as fobj:
        fobj.write(os.urandom(file_size))


def random_data_dir(num_files, file_size):
    dir_path = os.path.join(
        sources_dir(),
        "random_data",
        f"{num_files}_files",
        f"{file_size}_bytes",
    )

    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        fnames = [
            os.path.join(dir_path, "file_{}".format(str(i)))
            for i in range(num_files)
        ]
        with ThreadPoolExecutor(max_workers=max(cpu_count() / 2, 2)) as pool:
            pool.map(random_file, fnames, len(fnames) * [file_size])
    return dir_path
