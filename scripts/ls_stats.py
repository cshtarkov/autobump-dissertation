#!/usr/bin/env python3
#
# Read in stats.txt for all repositories and aggregate the data.
#
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from matplotlib_venn import venn3

COLORS = {
    "blue": "#5da5da",
    "red": "#f15854",
    "green": "#60bd68",
    "gray": "#4d4d4d",
    "purple": "#b276b2"
}

all_stats = []

for repo in os.listdir("."):
    stats_filename = os.path.join(".", repo, "stats.txt")
    try:
        with open(stats_filename) as stats:
            versions, mismatches, breaking, largest_major = map(int, stats.readline().split())
            if int(versions) < 2:
                continue
            print("Accepted ",repo)
            all_stats.append(list((repo, versions, mismatches, breaking, largest_major)))
    except:
        print("Missing stats file for", repo, file=sys.stderr)


def get_nums(st, dset):
    cum_p_mismatches = 0
    cum_p_breaking = 0
    max_p_mismatches = 0
    max_p_breaking = 0
    min_p_mismatches = 101
    min_p_breaking = 101
    min_versions = float("+inf")
    max_versions = float("-inf")

    for stats in st:
        versions = stats[1]
        mismatches = stats[2]
        breaking = stats[3]
        if versions > max_versions:
            max_versions = versions
        if versions < min_versions:
            min_versions = versions
        p_mismatches = float(mismatches) / versions * 100
        p_breaking = float(breaking) / versions * 100
        cum_p_mismatches += p_mismatches
        cum_p_breaking += p_breaking
        if p_mismatches > max_p_mismatches:
            max_p_mismatches = p_mismatches
        if p_mismatches < min_p_mismatches:
            min_p_mismatches = p_mismatches
        if p_breaking > max_p_breaking:
            max_p_breaking = p_breaking
        if p_breaking < min_p_breaking:
            min_p_breaking = p_breaking
        stats.append(p_mismatches)
        stats.append(p_breaking)

    avg_p_mismatches = cum_p_mismatches / len(st)
    avg_p_breaking = cum_p_breaking / len(st)

    print()
    print("Dataset:", dset)
    print("Total projects:", len(st))
    print("Min. versions:", min_versions)
    print("Max. versions:", max_versions)
    print("Min. mismatches: ", min_p_mismatches)
    print("Min. breaking: ", min_p_breaking)
    print("Max. mismatches: ", max_p_mismatches)
    print("Max. breaking: ", max_p_breaking)
    print("Avg. mismatches: ", avg_p_mismatches)
    print("Avg. breaking: ", avg_p_breaking)
    print("Projects with min. mismatches: ", len(list(filter(lambda p: p[5] == min_p_mismatches, st))))
    print("Projects with min. breaking: ", len(list(filter(lambda p: p[6] == min_p_breaking, st))))
    print()


dset1 = all_stats
dset2 = deepcopy(list(filter(lambda p: p[4] > 0, all_stats)))
dset3 = deepcopy(list(filter(lambda p: p[1] >= 10, all_stats)))
get_nums(all_stats, "all_stats")
get_nums(dset2, "major_1")
get_nums(dset3, "versions_10")

plt.clf()
plt.boxplot([list(map(lambda p: p[5], dset1)),
             list(map(lambda p: p[5], dset2)),
             list(map(lambda p: p[5], dset3))],
            vert=True,
            labels=["All projects",
                    "Published API",
                    "At least 10 releases"])
plt.yticks(np.arange(0, 101, 5))
plt.savefig("boxplots_mismatches.pdf")
plt.clf()
plt.boxplot([list(map(lambda p: p[6], dset1)),
             list(map(lambda p: p[6], dset2)),
             list(map(lambda p: p[6], dset3))],
            vert=True,
            flierprops=dict(marker='o', markersize=1),
            labels=["All projects",
                    "Published API",
                    "At least 10 releases"])
plt.yticks(np.arange(0, 101, 5))
plt.savefig("boxplots_breaking.pdf")

plt.clf()
plt.figure(figsize=(5,4))
venn3([set(map(lambda x: tuple(x), dset1)),
       set(map(lambda x: tuple(x), dset2)),
       set(map(lambda x: tuple(x), dset3))],
      set_labels=("All projects", "   Published API", "At least 10 releases"))
plt.savefig("datasets.pdf")

sample_versions = list(map(lambda p: p[1], all_stats))

plt.clf()
plt.xlabel("Number of released versions")
plt.ylabel("Number of projects")
plt.hist(sample_versions,
         bins=np.arange(min(sample_versions), max(sample_versions)+5, 5),
         color=[COLORS["blue"]])
plt.gca().set_yscale("log")
plt.savefig("distribution_all_versions.pdf")

sample_mismatches = list(map(lambda p: p[5], all_stats))
sample_breaking = list(map(lambda p: p[6], all_stats))

plt.clf()
plt.xlabel("Percentage")
plt.ylabel("Frequency")
plt.hist((sample_mismatches, sample_breaking),
         bins=np.arange(0, 105, 5),
         color=[COLORS["blue"], COLORS["red"]],
         label=["Mismatches", "Breaking mismatches"])
plt.legend()
plt.gca().set_yscale("log")
plt.savefig("distribution_all_mismatches_breaking.pdf")

gtN = list(filter(lambda p: p[1]>=10, all_stats))
print("gt10:", len(gtN))
sample_mismatches = list(map(lambda p: p[5], gtN))
sample_breaking = list(map(lambda p: p[6], gtN))

plt.clf()
plt.xlabel("Percentage")
plt.ylabel("Frequency")
plt.hist((sample_mismatches, sample_breaking),
         bins=np.arange(0, 105, 5),
         color=[COLORS["blue"], COLORS["red"]],
         label=["Mismatches", "Breaking mismatches"])
plt.legend()
plt.gca().set_yscale("log")
plt.savefig("distribution_gtn_all_mismatches_breaking.pdf")

major_one_or_better = list(filter(lambda p: p[4]>0, all_stats))
print("majoroneorbetter: ", len(major_one_or_better))
sample_mismatches = list(map(lambda p: p[5], major_one_or_better))
sample_breaking = list(map(lambda p: p[6], major_one_or_better))

plt.clf()
plt.xlabel("Percentage")
plt.ylabel("Frequency")
plt.hist((sample_mismatches, sample_breaking),
         bins=np.arange(0, 105, 5),
         color=[COLORS["blue"], COLORS["red"]],
         label=["Mismatches", "Breaking mismatches"])
plt.legend()
plt.gca().set_yscale("log")
plt.savefig("distribution_major_version_1_or_better.pdf")
majors = list(filter(lambda m: m < 100, map(lambda p: p[4], all_stats)))

plt.clf()
plt.xlabel("Largest major version")
plt.ylabel("Occurences")
bins = np.arange(0, max(majors)+1, 1)
plt.hist(majors,
         bins=bins,
         color=[COLORS["blue"]])
plt.xticks(bins + 0.5, bins)
plt.savefig("distribution_major_versions.pdf")
