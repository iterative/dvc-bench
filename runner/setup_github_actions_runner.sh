#!/bin/bash
sudo apt update
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo add-apt-repository ppa:git-core/ppa -y
sudo apt install software-properties-common python3.7 python3.7-dev git -y

mkdir ~/actions-runner
cd ~/actions-runner
curl -L https://github.com/actions/runner/releases/download/v$1/actions-runner-linux-x64-$1.tar.gz -o runner.tar.gz
tar xzf ./runner.tar.gz
rm runner.tar.gz
./config.sh --url https://github.com/iterative/dvc-bench --token $2 --name dvc-runner --labels 'dvc-runner' --work '_work' --replace
