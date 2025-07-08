#! /bin/bash

# Create local branch for all revs except the current branch and tags
# All the branches are assumed to have been fetched from the remote already.
IFS=',' read -r -a branch_array <<< "$1"
for branch in "${branch_array[@]}"; do
  git fetch origin $branch
  if ! git rev-parse --verify $branch &>/dev/null; then
    git branch "${branch}" origin/"${branch}"
  fi
done
