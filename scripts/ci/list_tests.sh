#!/bin/bash

set -e

pytest --collect-only -q --pyargs dvc.testing.benchmarks | grep partial | sed -E 's/([A-Za-z\/_]+)(\.py)(::([A-Za-z0-9_]+))?.*/dvc.testing.benchmarks.\1\3 \4/' | sed 's/\//./g' | jq -R -s -c 'split("\n")[:-1] | map({path: . | split(" ")[0], name: . | split(" ")[-1]})'
