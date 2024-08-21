#!/bin/bash

set -e

pytest --collect-only -q $1 | head -n -2 | sed 's/\[[^]]*\]//g' | jq -Rcs 'split("\n")[:-1] | map(. as $p | split("::") | {path: $p, name: .[1]})'
