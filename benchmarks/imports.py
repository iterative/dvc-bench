from benchmarks.base import BaseBench, BaseRemoteBench


class ImportBench(BaseBench):
    repeat = 1
    timeout = 12000

    def setup(self):
        super().setup()

        self.init_git()
        self.init_dvc()

    def time_imports(self):
        repo = f"file://{self.project_dir}"
        path = "data/cats_dogs"
        self.dvc("import", repo, path, proc=True)


class ImportUrlToRemoteBench(BaseRemoteBench):
    repeat = 1
    timeout = 12000

    def __init__(self):
        super().__init__()
        self.data_url = self.setup_data("mini")

    def time_import_url_to_remote(self):
        print("STARTING", file=__import__("sys").stderr)
        self.dvc("import-url", self.data_url, "--to-remote")
