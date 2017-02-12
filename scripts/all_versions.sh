#!/bin/bash
#
# Prints out all versions that were compared from
# Autobump's evaluation log (except the very last one).
#
[[ $1 == "" ]] && exit 1

grep $1 -e "\!EVAL Start diffing " |
    sed s'/!EVAL Start diffing \(.*\) and .*$/\1/'
