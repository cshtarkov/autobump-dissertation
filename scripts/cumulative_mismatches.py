#!/usr/bin/env python
#
# Run like this:
# cumulative_mismatches.py <(mismatches.sh file) <(tags_with_dates.sh | grep desired_version -B30000)
#
import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
from datetime import datetime
from autobump.common import Semver

# Parse mismatches
assert len(sys.argv) == 3, "Not enough arguments"
mismatches_file = sys.argv[1]
tags_with_dates_file = sys.argv[2]

mismatches = dict()
with open(mismatches_file) as f:
    mismatches = {actual: Semver.from_string(proposed)
                  for (actual, proposed) in
                  [line.split() for line in f.readlines()]}
assert len(mismatches) > 0

# Parse tags with dates
iso_format = "%Y-%m-%d"
with open(tags_with_dates_file) as f:
    dates_tags = dict()
    for date, version in [line.split() for line in f.readlines()]:
        dates_tags.setdefault(datetime.strptime(date, iso_format), list()).append(version)
assert len(dates_tags) > 0

# Accumulate total and breaking mismatches
dates_mismatches = OrderedDict()
total_mismatches = 0
total_breaking = 0
for date in sorted(dates_tags.keys()):
    versions = dates_tags.get(date)
    mismatches_count = len([v for v in versions if v in mismatches])
    breaking_count = len([v for v in versions if v in mismatches and mismatches[v].minor == 0 and mismatches[v].patch == 0])
    assert breaking_count <= mismatches_count
    total_mismatches += mismatches_count
    total_breaking += breaking_count
    dates_mismatches[date] = total_mismatches, total_breaking
assert len(dates_mismatches) > 0

# Measure time between releases
dates = list(dates_mismatches.keys())
diffs = list()
for date_a, date_b in zip(dates, dates[1:]):
    date_diff = (date_b - date_a).days
    total_diff = dates_mismatches[date_b][0] - dates_mismatches[date_a][0]
    breaking_diff = dates_mismatches[date_b][1] - dates_mismatches[date_a][1]
    if breaking_diff > 0:
        diffs.append(date_diff)
diffs = sorted(diffs)

# Plot cumulative mismatches
total = [total for (total, _) in dates_mismatches.values()]
breaking = [breaking for (_, breaking) in dates_mismatches.values()]

plt.clf()
plt.xlabel("Release date")
plt.ylabel("Cumulative number of mismatches")
total_plt = plt.scatter(dates, total, s=5, label="Total")
breaking_plt = plt.scatter(dates, breaking, s=5, label="Just breaking")
plt.legend(handles=[total_plt, breaking_plt])
plt.savefig("cumulative_mismatches.png")

# Plot histogram of time intervals
plt.clf()
plt.xlabel("Time interval (in days)")
plt.ylabel("Breaking changes introduced")
plt.hist(diffs, bins=np.logspace(0, 3, 10))
plt.gca().set_xscale("log")
plt.savefig("introduced_changes.png")
