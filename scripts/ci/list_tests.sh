#!/bin/bash

set -e

echo $(pytest --collect-only tests/benchmarks -q | head -n -2 | jq -R -s -c 'split("\n")[:-1] | map({path: ., name: . | split(":")[-1]})')
