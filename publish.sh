#!/bin/bash
set -euo pipefail

git branch -f publish master
git checkout publish
./build.py
git add -f docs
git commit -am "publish"
git push
git checkout master
