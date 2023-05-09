#!/bin/bash

set -e

pytest --collect-only -q --pyargs dvc_s3.tests.benchmarks | grep test_ | sed -E 's/::([A-Za-z0-9_]+).*/dvc_s3.tests.benchmarks::\1 \1/' | sed 's/\//./g' | jq -R -s -c 'split("\n")[:-1] | map({path: . | split(" ")[0], name: . | split(" ")[-1]})'
