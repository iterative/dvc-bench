#!/bin/bash
sudo apt update
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo add-apt-repository ppa:git-core/ppa -y
sudo apt install software-properties-common python3.7 python3.7-dev git -y

mkdir ~/actions-runner 
cd ~/actions-runner
curl -O -L https://github.com/actions/runner/releases/download/v2.272.0/actions-runner-linux-x64-2.272.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.272.0.tar.gz
rm actions-runner-linux-x64-2.272.0.tar.gz
./config.sh --url https://github.com/iterative/dvc-bench --token $1 --name dvc-runner --labels 'dvc-runner' --work '_work' --replace
