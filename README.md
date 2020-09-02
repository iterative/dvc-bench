## dvc-bench
Benchmarking [dvc](https://github.com/iterative/dvc) with Airspeed Velocity.


### Setting up
1. Clone this repository.
2. `cd dvc-bench`
3. Create a virtual env and install requirements:
   ```console
   $ pip install -r requirements.txt
   ```
   > `virtualenv` has to be 16

### Running benchmarks
```console
$ dvc pull data/cats_dogs.dvc
$ dvc repro run_benchmarks.dvc
```

### Visualizing results
```console
$ asv publish && asv preview
```

### Testing local changes against dvc master
1. Set up this project
2. Change `repo` value in `asv.conf.json` to point to your local `dvc` repository.
3. Put target git hash and master hash to `file.txt`
4. Run benchmark(s): `asv run HASHFILE:file.txt`
5. To run specific benchmark, use `--bench {benchmark_name}` option.
