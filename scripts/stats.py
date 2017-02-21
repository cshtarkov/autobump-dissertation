#!/usr/bin/env python3
#
# Generates repository statistics in the form
# (all_compared_versions, mismatch_count, breaking_count)
#
import sys
from subprocess import Popen, PIPE
from autobump.common import Semver

assert len(sys.argv) == 3, "Not enough arguments"
mismatches_file = sys.argv[1]
all_versions_file = sys.argv[2]

# Get mismatch counts
mismatch_count = 0
breaking_count = 0
with open(mismatches_file) as f:
    for line in f.readlines():
        actual, proposed = line.split()
        proposed = Semver.from_string(proposed)
        mismatch_count += 1
        if proposed.minor == 0 and proposed.patch == 0:
            breaking_count += 1

# Get all versions
largest_major = 0
all_versions = 0
with open(all_versions_file) as f:
    for version in f.readlines():
        all_versions += 1
        major = Semver.guess_from_string(version).major
        if major > largest_major:
            largest_major = major
all_versions += 1

print(all_versions, mismatch_count, breaking_count, largest_major)
