#!/bin/bash

set -e

PLUGIN="dvc_$1"
pytest --collect-only -q --pyargs "$PLUGIN.tests.benchmarks" | grep test_ | sed -E "s/::([A-Za-z0-9_]+).*/$PLUGIN.tests.benchmarks::\\1 \\1/" | sed 's/\//./g' | jq -R -s -c 'split("\n")[:-1] | map({path: . | split(" ")[0], name: . | split(" ")[-1]})'
