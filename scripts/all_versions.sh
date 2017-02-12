#!/bin/bash
[[ $1 == "" ]] && exit
grep $1 -e "\!EVAL Start diffing " |
    sed s'/!EVAL Start diffing \(.*\) and .*$/\1/'
