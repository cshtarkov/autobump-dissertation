#!/bin/bash
[[ $1 == "" ]] && exit
grep $1 -e MISMATCH \
    | sed s'/^!EVAL MISMATCH: .*-- \(.*\) should.*-- \(.*\)$/\1 \2/'
