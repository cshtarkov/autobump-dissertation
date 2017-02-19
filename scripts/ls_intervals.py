#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt

COLORS = {
    "blue": "#5da5da",
    "red": "#f15854"
}

assert len(sys.argv) == 3, "Not enough arguments"
diffs_file = sys.argv[1]
all_versions_file = sys.argv[2]

diffs = []
all_versions = []
with open(diffs_file) as f:
    diffs = [int(x) for x in [line.split()[0] for line in f.readlines()]]
with open(all_versions_file) as f:
    all_versions = [int(x) for x in [line.split()[0] for line in f.readlines()]]

assert len(diffs) > 0
assert len(all_versions) > 0

plt.clf()
plt.xlabel("Time interval (in days)")
plt.ylabel("Released versions")
plt.hist((all_versions, diffs),
         bins=np.logspace(0, 3, 10),
         color=[COLORS["blue"], COLORS["red"]],
         label=["All", "Unnoted breaking change(s)"])
plt.gca().set_xscale("log")
plt.legend()
plt.savefig("ls_introduced_changes.pdf")
