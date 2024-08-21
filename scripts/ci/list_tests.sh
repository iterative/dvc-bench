#!/bin/bash

set -e

pytest --collect-only -q $1 | head -n -2 | sed 's/\[[^]]*\]//g; s/\(.*::\)\(.*\)/\1\2 \2/' | jq -R -s -c 'split("\n")[:-1] | map(split(" ") | {path: .[0], name: .[1]})'
