#!/bin/sh

if [ $# -eq 0 ]; then
  echo "Usage: $0 <libgit2_version>"
  exit 1
fi

LIBGIT2_VERSION=$1
wget https://github.com/libgit2/libgit2/archive/refs/tags/v"${LIBGIT2_VERSION}.tar.gz" -O "libgit2-${LIBGIT2_VERSION}.tar.gz"
tar xzf "libgit2-${LIBGIT2_VERSION}.tar.gz"
cd "libgit2-${LIBGIT2_VERSION}/" || exit 1
cmake .
make
sudo make install
