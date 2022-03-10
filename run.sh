#!/bin/bash

set -e
set -x

export PIPENV_IGNORE_VIRTUALENVS=1

REVS=("fix/7414-hang-on-pull")

if [ ! -d "dvc" ]; then
  git clone https://github.com/dtrifiro/dvc
  python -m venv dvc/.venv
fi

for REV in ${REVS[@]}; do
  pushd dvc
  git checkout $REV
  ./.venv/bin/pip install -e '.[all,tests]'
  popd

  pytest --benchmark-save $(echo $REV | sed 's|/|_|') $@ --dvc-bin "$(pwd)/dvc/.venv/bin/dvc"
done
