## dvc-bench
Benchmarking [dvc](https://github.com/iterative/dvc) with pytest-benchmark.

### Daily benchmark results

Visit [bench.dvc.org](http://bench.dvc.org/)

### Dispatch workflow

Trigger a [dispatch workflow](https://github.com/iterative/dvc-bench/actions/workflows/build.yml) with desired dataset and revisions and see results in [bench.dvc.org/run_ID_ATTEMPT.html](http://bench.dvc.org), where `ID` is `github.run_id` and `ATTEMPT` is `github.run_attempt`. For example, for https://github.com/iterative/dvc-bench/actions/runs/7119039172/attempts/2 it would be http://bench.dvc.org/run_7119039172_2.html

### Setting up
```
$ uv pip install -r requirements.txt
$ dvc pull # optional, otherwise will pull datasets dynamically
```

### Running all benchmarks
```console
$ pytest --pyargs dvc.testing.benchmarks
```

### Running one benchmark
```console
$ pytest --pyargs dvc.testing.benchmarks.cli.commands.test_add
```

### CLI options
```
$ pytest -h
...
  --dataset=DATASET
                        Dataset name to use in tests (e.g. tiny/small/large/mnist/etc)
  --dvc-bin=DVC_BIN     Path to dvc binary
  --dvc-revs=DVC_REVS   Comma-separated list of DVC revisions to test (overrides `--dvc-bin`)
  --dvc-repo=DVC_GIT_REPO
                        Path or url to dvc git repo
  --dvc-bench-repo=DVC_BENCH_GIT_REPO
                        Path or url to dvc-bench git repo (for loading benchmark dataset)
  --dvc-install-deps=DVC_INSTALL_DEPS
                        Comma-separated list of DVC installation packages
  --project-rev=PROJECT_REV
                        Project revision to test
  --project-repo=PROJECT_GIT_REPO
                        Path or url to dvc project
...
```

### Comparing results
```
$ pytest-benchmark compare --histogram histograms/ --group-by name --sort name --csv results.csv
```

and if you want beautiful plots:

```
$ dvc repro
$ dvc plots show
```

### Contributing

Benchmark test definitions are now part of [dvc.testing](https://github.com/iterative/dvc/tree/main/dvc/testing).
