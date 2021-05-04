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


class ImportUrlBench(BaseRemoteBench):
    repeat = 1
    timeout = 12000

    def setup(self):
        super().setup()
        self.data_url = self._remote_prefix + self.setup_data("100x1024")

    def time_import_url(self):
        self.dvc("import-url", self.data_url, proc=True)


class ImportUrlToRemoteBench(BaseRemoteBench):
    repeat = 1
    timeout = 12000

    def setup(self):
        super().setup()
        self.data_url = self._remote_prefix + self.setup_data("100x1024")

    def time_import_url_to_remote(self):
        self.dvc("import-url", self.data_url, "--to-remote", proc=True)
