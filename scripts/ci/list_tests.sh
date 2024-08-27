#!/bin/bash

set -e

pytest --collect-only -q $1 | grep test_ | sed 's/\[[^]]*\]//g' | jq -Rcs 'split("\n")[:-1] | map(. as $p | split("::") | {path: $p, name: .[1]})' | jq -c --arg names "$2" '
if ($names | length > 0) then
  ($names | split(",")) as $_names | map(select(.name | IN($_names[])))
else
  .
end
'
