import shutil
import timeit
from collections import defaultdict
from statistics import median

from benchmarks.base import BaseBench


class SequentialBench(BaseBench):
    # NOTE: in case of `track` benchmarks this needs to be handled "by hand"
    repeat = 3
    timer = timeit.default_timer
    units = "seconds"

    def __init__(self):
        self.results = {}
        self.ran = False

    def measure(self, *args):
        start = self.timer()
        self.dvc(*args)
        return self.timer() - start

    def setup_cache(self):
        results = defaultdict(list)
        for _ in range(self.repeat):
            super().setup()

            self.init_git()
            self.init_dvc()

            self.gen("data", template="cats_dogs")

            # benchmark #1
            results["time_add"].append(self.measure("add", "data", "--quiet"))

            # setup #2
            shutil.rmtree("data")

            results["time_checkout"].append(
                self.measure("checkout", "data.dvc")
            )
            super().teardown()

        for key, measurements in results.items():
            results[key] = median(measurements)

        return results

    def track_time_add(self, results):
        return results["time_add"]

    def track_time_checkout(self, results):
        return results["time_checkout"]
