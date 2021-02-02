from benchmarks.base import BaseBench, TmpDir

# class ImportBench(BaseBench):
#     repeat = 1
#     timeout = 12000
#
#     def setup(self):
#         super().setup()
#
#         self.init_git()
#         self.init_dvc()
#
#     def time_imports(self):
#         repo = f"file://{self.project_dir}"
#         path = "data/cats_dogs"
#         self.dvc("import", repo, path, proc=True)


class ImportBench(BaseBench):
    repeat = 1
    timeout = 12000

    def setup(self):
        super().setup()

        self.erepo = TmpDir(f"{self.__class__.__name__}_erepo")
        self.erepo.gen("data", "small")

        self.directory.init_git()
        self.directory.init_dvc()

    def time_imports(self):
        repo = f"file://{self.project_dir}"
        path = "data/cats_dogs"
        self.dvc("import", repo, path, proc=True)
