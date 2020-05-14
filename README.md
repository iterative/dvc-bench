## How to play around with DVC and asv?

1. Clone `dvc-bench` repository.
2. `cd dvc-bench`
3. `pip install -r requirements.txt`  (`virtualenv` has to be 16)
4. `dvc repro dvc.yaml:run_benchmarks`
5. `asv publish && asv preview`
