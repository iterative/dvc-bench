#!/bin/bash

set -e

echo $(pytest --collect-only tests/benchmarks -q | grep tests/benchmarks | sed 's/\[.*None.*\]//g' | jq -R -s -c 'split("\n")[:-1] | map({path: ., name: . | split(":")[-1]})')
