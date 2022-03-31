#!/bin/bash

set -e
set -x

export PIPENV_IGNORE_VIRTUALENVS=1

REVS=("main" "2.10.0" "2.9.5" "2.8.3" "2.7.3" "2.6.3")

if [ ! -d "dvc" ]; then
  git clone https://github.com/iterative/dvc
  git fetch --tags
  python -m venv dvc/.venv
fi

for REV in ${REVS[@]}; do
  pushd dvc
  git checkout $REV
  ./.venv/bin/pip install -e '.[all,tests]'
  popd

  pytest --benchmark-save $REV $@ --dvc-bin "$(pwd)/dvc/.venv/bin/dvc"
done
