import shutil
from subprocess import Popen

import pytest


@pytest.fixture
def dvc_bin(test_config):
    def _dvc_bin(*args):
        proc = Popen([test_config.dvc_bin, *args])
        proc.communicate()
        assert proc.returncode == 0

    return _dvc_bin


@pytest.fixture(scope="function")
def make_bench(request):
    def _make_bench(name):
        import pytest_benchmark.plugin

        # hack from https://github.com/ionelmc/pytest-benchmark/issues/166
        bench = pytest_benchmark.plugin.benchmark.__pytest_wrapped__.obj(
            request
        )
        bench.name += f"-{name}"
        return bench

    return _make_bench


@pytest.fixture(scope="function")
def bench_dvc(dvc_bin, make_bench):
    def _bench_dvc(*args, **kwargs):
        name = kwargs.pop("name", None)
        name = f"-{name}" if name else ""
        bench = make_bench(args[0] + name)
        return bench.pedantic(dvc_bin, args=args, **kwargs)

    return _bench_dvc


@pytest.fixture
def make_dataset(request, test_config, tmp_dir, pytestconfig):
    def _make_dataset(
        dvcfile=False, files=True, cache=False, commit=False, remote=False
    ):
        from dvc.repo import Repo
        from dvc.exceptions import CheckoutError, DownloadError

        path = tmp_dir / "dataset"
        root = pytestconfig.rootpath
        src = root / "data" / test_config.size / "dataset"
        src_dvc = src.with_suffix(".dvc")

        dvc = Repo(root)

        while True:
            try:
                dvc.pull([str(src_dvc)])
                break
            except (CheckoutError, DownloadError):
                pass

        if files:
            shutil.copytree(src, path)
        if dvcfile:
            shutil.copy(src.with_suffix(".dvc"), path.with_suffix(".dvc"))
        if cache:
            shutil.copytree(
                root / ".dvc" / "cache", tmp_dir / ".dvc" / "cache"
            )
        if remote:
            assert dvcfile
            assert not cache
            assert tmp_dir.dvc
            # FIXME temporary hack, we should try to push from home repo
            # directly to this remote instead
            shutil.copytree(
                root / ".dvc" / "cache", tmp_dir / ".dvc" / "cache"
            )
            tmp_dir.dvc.push(
                [str(path.with_suffix(".dvc").relative_to(tmp_dir))]
            )
            shutil.rmtree(tmp_dir / ".dvc" / "cache")
        if commit:
            assert dvcfile
            assert tmp_dir.scm
            tmp_dir.scm.add(
                [str(path.with_suffix(".dvc").relative_to(tmp_dir))]
            )
            tmp_dir.scm.commit("add dataset")
        return path

    return _make_dataset


@pytest.fixture
def dataset(make_dataset):
    return make_dataset(dvcfile=False, files=True, cache=False)


@pytest.fixture
def remote_dataset(test_config):
    pytest.skip("fixme")
