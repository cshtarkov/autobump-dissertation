#!/bin/bash
[[ $1 == "" ]] && exit
for repo in `cat $1 | awk '{print $2}'`; do
    git clone $repo
done
