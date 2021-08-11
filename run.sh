#!/bin/bash

set -e
set -x

asv run --show-stderr --skip-existing-successful -v $@
