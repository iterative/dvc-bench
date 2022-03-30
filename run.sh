#!/bin/bash

set -e
set -x

export PIPENV_IGNORE_VIRTUALENVS=1

REV=$1
shift

if [ ! -d "dvc" ]; then
  git clone https://github.com/iterative/dvc
  python -m venv dvc/.venv
fi

pushd dvc
git checkout $REV
./.venv/bin/pip install -e '.[all,tests]'
popd

if [[ $REV == "main" ]]; then
  REV="main@$(git rev-parse --short=7 HEAD)"
fi
pytest --benchmark-save "$REV" $@ --dvc-bin "$(pwd)/dvc/.venv/bin/dvc"
