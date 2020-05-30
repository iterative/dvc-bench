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
$ dvc repro run_benchmarks.dvc
```

### Visualizing results
```console
$ asv publish && asv preview
```
