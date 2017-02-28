#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt

COLORS = {
    "blue": "#5da5da",
    "red": "#f15854"
}

assert len(sys.argv) == 5, "Not enough arguments"
diffs_file = sys.argv[1]
all_versions_file = sys.argv[2]
before_stable_file = sys.argv[3]
after_stable_file = sys.argv[4]

diffs = []
all_versions = []
with open(diffs_file) as f:
    diffs = [int(x) for x in [line.split()[0] for line in f.readlines()]]
with open(all_versions_file) as f:
    all_versions = [int(x) for x in [line.split()[0] for line in f.readlines()]]
with open(before_stable_file) as f:
    before_stable = [int(x) for x in [line.split()[1] for line in f.readlines()]]
with open(after_stable_file) as f:
    after_stable = [int(x) for x in [line.split()[1] for line in f.readlines()]]

assert len(diffs) > 0
assert len(all_versions) > 0
assert len(before_stable) > 0
assert len(after_stable) > 0

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

print("Total before stable:", sum(before_stable))
print("Total after stable:", sum(after_stable))

proportions = list()
for b, a in zip(before_stable, after_stable):
    if a == 0 and b == 0:
        continue
    if b == 0:
        continue
    if a == 0:
        a = 1
    proportions.append(float(b)/a)

plt.clf()
plt.xlabel("Mismatches before stable API over breaking mismatches after")
plt.ylabel("Count")
plt.hist(proportions,
         bins=np.arange(0,7.55,0.05),
         color=[COLORS["blue"]])
#plt.gca().set_yscale("log")
plt.savefig("ls_stable_boundary.pdf")
