#!/bin/bash

set -e
set -x

tree .benchmarks
rm -rf html
mkdir html
echo bench.dvc.org > html/CNAME
echo > raw
echo "$(date)" >> raw
echo "dataset: ${DATASET}" >> raw
echo "project: example-get-started" >> raw
cat raw | ansi2html -W > html/index.html

for file in $(find .benchmarks -type f);
do
  rm -rf tmp_html results.csv raw
  PY_COLORS=1 py.test-benchmark compare $file --histogram histograms/ --group-by func --csv results.csv --sort name >> raw
  dvc repro --no-run-cache
  dvc plots show -o tmp_html
  cat tmp_html/index.html >> html/index.html
  cat raw | ansi2html -W >> html/index.html
done
