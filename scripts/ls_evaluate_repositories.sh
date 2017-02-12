#!/bin/bash
#
# Generates evaluation log for every repository in the
# current directory. The log gets put in the file "mismatches.txt"
# in the same directory as the repository.
#
for repo in `echo */`; do
    cd $repo
    FIRST_TAG=`git tag --sort version:refname | head -n1`
    LAST_TAG=`git tag --sort version:refname | tail -n1`
    printf "\nEvaluating $repo from $FIRST_TAG to $LAST_TAG\n"
    cd ..
    autobump python -r $repo -f $FIRST_TAG -t $LAST_TAG -e -d -cstdout > "$repo"mismatches.txt 2>> megadebug.txt
done
