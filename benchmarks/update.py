from benchmarks.base import BaseRemoteBench


class UpdateImportUrlBench(BaseRemoteBench):
    def setup(self, remote):
        super().setup(remote)
        data_url = self.setup_data("100x1024")
        self.dvc("import-url", data_url, "stage")
        self.setup_data("200x1024", url=data_url)

    def time_import_url_to_remote(self, _):
        self.dvc("update", "stage.dvc", proc=True)


class UpdateImportUrlToRemoteBench(BaseRemoteBench):
    def setup(self, remote):
        super().setup(remote)
        data_url = self.setup_data("100x1024")
        self.dvc(
            "import-url", data_url, "stage", "--to-remote",
        )
        self.setup_data("200x1024", url=data_url)

    def time_import_url_to_remote(self, _):
        self.dvc("update", "stage.dvc", "--to-remote", proc=True)
