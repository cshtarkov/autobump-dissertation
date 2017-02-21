#!/usr/bin/env python3
#
# Generates graphs from Autobump's evaluation log
# by using some scripts as data sources.
#
# Run like this:
# cumulative_mismatches.py <(mismatches.sh file) <(tags_with_dates.sh | grep desired_version -B30000)
#
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
from datetime import datetime
from autobump.common import Semver

COLORS = {
    "blue": "#5da5da",
    "red": "#f15854",
    "green": "#60bd68",
    "gray": "#4d4d4d",
    "purple": "#b276b2"
}

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
all_versions = list()
for date_a, date_b in zip(dates, dates[1:]):
    date_diff = (date_b - date_a).days
    total_diff = dates_mismatches[date_b][0] - dates_mismatches[date_a][0]
    breaking_diff = dates_mismatches[date_b][1] - dates_mismatches[date_a][1]
    if breaking_diff > 0:
        diffs.append(date_diff)
    all_versions.append(date_diff)
diffs = sorted(diffs)
all_versions = sorted(all_versions)
for diff in diffs:
    print("diff", diff)
for all_version in all_versions:
    print("all_version", all_version)

# Plot cumulative mismatches
total = [total for (total, _) in dates_mismatches.values()]
breaking = [breaking for (_, breaking) in dates_mismatches.values()]

plt.clf()
plt.xlabel("Release date")
plt.ylabel("Cumulative number of mismatches")
total_plt = plt.scatter(dates, total, s=25, label="Total", color=COLORS["blue"])
breaking_plt = plt.scatter(dates, breaking, s=25, label="Just breaking", color=COLORS["red"])
plt.legend(handles=[total_plt, breaking_plt])
plt.gcf().autofmt_xdate()
plt.yticks(range(min(total), math.ceil(max(total))+1, 2))
# plt.annotate(xy=(datetime(2013, 4, 12), 7), s="v5.1.0",
#              textcoords="offset pixels", xytext=(50,-40),
#              arrowprops=dict(facecolor="black", shrink=0.03, width=2, headwidth=12),
#              verticalalignment="bottom", horizontalalignment="right")
plt.savefig("cumulative_mismatches.pdf")

# Plot histogram of time intervals
plt.clf()
plt.xlabel("Time interval (in days)")
plt.ylabel("Released versions")
plt.hist((all_versions, diffs),
         bins=np.logspace(0, 3, 10),
         color=[COLORS["blue"], COLORS["red"]],
         label=["All", "Unnoted breaking change(s)"])
plt.gca().set_xscale("log")
plt.legend()
plt.savefig("introduced_changes.pdf")

# Calculate frequency of releases in some intervals
# total_freq = len(dates) / float(((dates[-1] - dates[0]).days)) * 100
# print("Total frequency: ", total_freq)
# dates_between = list(filter(lambda d: d >= datetime(2012, 1, 1), filter(lambda d: d <= datetime(2013, 1, 1), dates)))
# dates_between_freq = len(dates_between) / float(((dates_between[-1] - dates_between[0]).days)) * 100
# print("dates_between frequency: ", dates_between_freq)
