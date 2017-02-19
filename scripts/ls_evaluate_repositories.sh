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
    autobump python -r $repo -f $FIRST_TAG -t $LAST_TAG -e -d -cstdout &> "$repo"mismatches.txt
    stats.py <(mismatches.sh "$repo"mismatches.txt) <(all_versions.sh "$repo"mismatches.txt) > "$repo"stats.txt
    cd $repo
    cumulative_mismatches.py <(mismatches.sh mismatches.txt) <(tags_with_dates.sh) > intervals.txt
    cd ..
done
