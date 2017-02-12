#!/bin/bash
#
# Clone all repositories found in a
# (reponame, url, popularity) file.
#
[[ $1 == "" ]] && exit 1

for repo in `cat $1 | awk '{print $2}'`; do
    git clone $repo
done
