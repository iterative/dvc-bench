from benchmarks.base import BaseBench


class ImportBench(BaseBench):
    repeat = 1
    timeout = 2000

    def setup(self):
        super().setup()

        self.init_git()
        self.init_dvc()

    def time_imports(self):
        repo = f"file://{self.project_dir}"
        path = "data/cats_dogs"
        self.dvc("import", repo, path)
