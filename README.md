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
$ pytest
```

### Running one benchmark
```console
$ pytest tests/benchmarks/cli/commands/test_add.py
```

### CLI options
```
$ pytest -h
...
  --size={tiny,small,large,mnist}
                        Size of the dataset/datafile to use in tests
  --remote={azure,gdrive,gs,hdfs,http,oss,s3,ssh,webdav}
                        Remote type to use in tests
  --dvc-bin=DVC_BIN     Path to dvc binary
  --dvc-revs=DVC_REVS   Comma-separated list of DVC revisions to test (overrides `--dvc-bin`)
  --dvc-git-repo=DVC_GIT_REPO
                        Path or url to dvc git repo
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
tests/benchmarks structure:
- cli: should be able to run these with any dvc (rpm, deb, pypi, snap, etc) (could be used in dvc-test repo too)
  - commands: granular tests for individual commands. These should have a cached setup, so that we could use them during rapid development instead of our hand-written scripts. Every test could be run in a separate machine.
  - stories: multistage start-to-end benchmarks, useful for testing workflows (e.g. in documentation, see test_sharing inspired by [sharing-data-and-models use-case](https://dvc.org/doc/use-cases/sharing-data-and-model-files). Every full story could be run in a separate machine.
- api: for python api only.
  - methods: granular tests for individual methods (e.g. `api.open/read`). Same reasoning as in `cli.commands`
  - stories: same as `cli.stories` but for our api. E.g. imagine using our api with pandas or smth like that.
