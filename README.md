## dvc-bench
Benchmarking [dvc](https://github.com/iterative/dvc) with pytest-benchmark.

### Daily benchmark results

Visit [bench.dvc.org](http://bench.dvc.org/)

### Setting up
```
$ pip install -r requirements.txt
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
  --remote={azure,gdrive,gs,hdfs,http,oss,s3,ssh,webdav}
                        Remote type to use in tests
  --dvc-bin=DVC_BIN     Path to dvc binary
  --dvc-revs=DVC_REVS   Comma-separated list of DVC revisions to test (overrides `--dvc-bin`)
  --dvc-git-repo=DVC_GIT_REPO
                        Path or url to dvc git repo
  --dvc-bench-git-repo=DVC_BENCH_GIT_REPO
                        Path or url to dvc-bench git repo (for loading benchmark dataset)
  --project-rev=PROJECT_REV
                        Project revision to test
  --project-git-repo=PROJECT_GIT_REPO
                        Path or url to dvc project
...
```

### Comparing results
```
$ py.test-benchmark compare --histogram histograms/ --group-by name --sort name --csv results.csv
```

and if you want beautiful plots:

```
$ dvc repro
$ dvc plots show
```

### Contributing

Benchmark test definitions are now part of [dvc.testing](https://github.com/iterative/dvc/tree/main/dvc/testing).
