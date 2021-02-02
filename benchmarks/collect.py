from benchmarks.base import BaseBench


class CollectBench(BaseBench):
    repeat = 1
    number = 30

    def setup(self):
        super().setup()

        self.directory.init_dvc()

        self.directory.gen("data", template="small")
        self.dvc("add", "-R", "data", "--quiet")

        self.dvc("status", "--quiet")

    def time_stages_collection(self):
        self.dvc("status", "--quiet", proc=True)


class TraverseGitRepoBench(BaseBench):
    repeat = 1
    number = 10
    timeout = 1200

    def clone(self, url, tag):
        # clone only branch containing the tag
        self.proc("git", "clone", "--branch", tag, "--single-branch", url, ".")

    def setup(self):
        super().setup()
        self.clone("https://github.com/iterative/dvc.git", tag="0.10.0")

    def time_repo_traversing(self):
        # DVC has no metrics, hence return_code==1
        self.dvc("metrics", "show", "--all-commits", return_code=1, proc=True)
