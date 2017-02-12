#!/bin/bash
#
# Generates only mismatched version numbers from
# Autobump's evaluation log.
#
[[ $1 == "" ]] && exit 1

grep $1 -e MISMATCH \
    | sed s'/^!EVAL MISMATCH: .*-- \(.*\) should.*-- \(.*\)$/\1 \2/'
