#!/bin/bash
for repo in `echo */`; do
    cd $repo
    FIRST_TAG=`git tag --sort version:refname | head -n1`
    LAST_TAG=`git tag --sort version:refname | tail -n1`
    printf "\nEvaluating $repo from $FIRST_TAG to $LAST_TAG\n"
    cd ..
    autobump python -r $repo -f $FIRST_TAG -t $LAST_TAG -e -d -cstdout > "$repo"mismatches.txt 2>> megadebug.txt
done
