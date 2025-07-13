#!/bin/bash
set -euo pipefail

if [ ! -z "$(git status --porcelain)" ]; then
    echo uncommitted changes
    exit 1
fi

git branch -f publish master
git checkout publish

./build.py
echo "rje.li" >docs/CNAME
touch docs/.nojekyll

git add -f docs
git commit -am "publish"
git push -f
git checkout master
