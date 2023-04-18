import shutil

def pytest_generate_tests(metafunc):
    if "remote" in metafunc.fixturenames:
        config = metafunc.config.dvc_config
        remotes = set(config.enabled_remotes)
        remotes.add(config.remote)
        metafunc.parametrize("remote", remotes, indirect=True)


def test_sharing(bench_dvc, tmp_dir, dvc, dataset, remote):
    bench_dvc("add", dataset)
    bench_dvc("add", dataset, name="noop")

    bench_dvc("push")
    bench_dvc("push", name="noop")

    shutil.rmtree(dataset)
    shutil.rmtree(tmp_dir / ".dvc" / "cache")

    bench_dvc("pull")
    bench_dvc("pull", name="noop")

    bench_dvc("checkout", name="noop")
