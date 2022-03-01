#!/bin/bash

set -e
set -x

export PIPENV_IGNORE_VIRTUALENVS=1

REVS=( "2.9.5" "2.8.3" "2.7.3" "2.6.3" )

if [ ! -d "dvc" ]; then
  git clone https://github.com/iterative/dvc
fi

for REV in ${REVS[@]}; do
  python -m venv dvc/.venv

  pushd dvc
  git checkout $REV
  ./.venv/bin/pip install -e '.[all,tests]'
  popd

  pytest --benchmark-save $REV $@ --dvc-bin "$(pwd)/dvc/.venv/bin/dvc"

  rm -rf dvc/.venv
done
