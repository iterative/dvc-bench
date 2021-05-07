from benchmarks.base import BaseRemoteBench


class UpdateImportUrlBench(BaseRemoteBench):
    repeat = 1
    timeout = 12000

    def setup(self):
        super().setup()
        self.data_url = self.setup_data("100x1024", name="update-data")
        self.dvc("import-url", self._remote_prefix + self.data_url, "stage")
        self.setup_data("200x1024", name="update-data")

    def time_import_url(self):
        self.dvc("update", "stage.dvc", proc=True)


class UpdateImportUrlToRemoteBench(BaseRemoteBench):
    repeat = 1
    timeout = 12000

    def setup(self):
        super().setup()
        self.data_url = self.setup_data("100x1024", name="update-data")
        self.dvc(
            "import-url",
            self._remote_prefix + self.data_url,
            "stage",
            "--to-remote",
        )
        self.setup_data("200x1024", name="update-data")

    def time_import_url_to_remote(self):
        self.dvc("update", "stage.dvc", "--to-remote", proc=True)
