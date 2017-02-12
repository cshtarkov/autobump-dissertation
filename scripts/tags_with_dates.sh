#!/bin/bash
#
# Prints Git tags with their respective dates.
#
git log --tags --simplify-by-decoration --pretty="format:%ai %d" \
    | grep "tag: " \
    | awk '{print $1" "$5}' \
    | sed s'/.$//'
