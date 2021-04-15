import pandas as pd
import matplotlib.pyplot as plt

import util
from util import e_class_util
from util import plot

num_you = 30
num_mark = 23

# plot colors
colors_ge = ["red", "blue"]
colors_e = ["black", "gray"]

#####
# GE-CLASS
#####

disagreement = pd.read_csv("export.csv")
# only consider physics majors
disagreement = disagreement[
        (disagreement["program_id"] == 1) |
        (disagreement["program_id"] == 2)
]
binary = disagreement.replace(-1, 0)
compact_binary = util.Compactify(binary, num_you, num_mark)
disagreement_compact = util.Compactify(disagreement, num_you, num_mark)


#####
# E-CLASS
#####

df_post = pd.read_csv("anon_post.csv")
df_pre = pd.read_csv("anon_pre.csv")
df_cis = pd.read_csv("anon_cis.csv")
disagreement_e_class, binary_e_class, compact_binary_e_class, \
        disagreement_compact_e_class = \
        e_class_util.PrepareMatchedData(df_post, df_pre, df_cis, num_you,
                                        num_mark)

#####
# Figure 1 - Overall Comparison
#####
"""
fig, ax = plt.subplots()
plot.PlotOverallCourseComparison(compact_binary, compact_binary_e_class,
                                 colors_ge, colors_e, ax)
plt.show()
"""

#####
# Figure 2 - Distribution Comparison
#####

fig, ax = plt.subplots(ncols=2, nrows=2)
plot.PlotDistributions(disagreement_compact, disagreement_compact_e_class, colors_ge, color_e, ax)
