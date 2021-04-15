#!/usr/bin/env python
# coding: utf-8
import textwrap

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import util
from util import e_class_util
from util import plot

plt.style.use("paper.mplstyle")

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
print(disagreement.experience_id.value_counts())
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

print("Start Figure 1")
plt.rcParams.update({"font.size": 9})
plt.rcParams.update({"axes.labelsize": 12})
fig, ax = plt.subplots()
plot.PlotOverallCourseComparison(compact_binary, compact_binary_e_class,
                                 colors_ge, colors_e, ax)
#plt.show()
fig.tight_layout()
fig.savefig("fig_1_overall")
plt.rcdefaults()
plt.style.use("paper.mplstyle")

#####
# Figure 2 - Distribution Comparison
#####

print("Start Figure 2")
fig, ax = plt.subplots(nrows=2, figsize=(6.75, 4.75), sharex="col")
ax[1].set_xlabel("Reached Total Score")
ax[0].set_ylabel("\n".join(textwrap.wrap("Cumulative Likelihood for YOU-Questions", width=20)))
ax[1].set_ylabel("\n".join(textwrap.wrap("Cumulative Likelihood for EXPERT-Questions", width=20)))
plot.PlotDistributions(disagreement_compact, disagreement_compact_e_class, colors_ge,
                       colors_e, ax)
plot.label_axis("a", ax[0], position=(0.03, 0.875))
plot.label_axis("b", ax[1], position=(0.03, 0.875))
ax[1].legend(bbox_to_anchor=(0.2, 0.8), loc='upper left')
ax[0].set_xlim(-5., 30.)
#plt.show()
fig.tight_layout()
fig.savefig("fig_2_distribution")

#####
# Figure 3 - Question Comparison
#####

print("Start Figure 3")
plt.rcParams.update({"legend.fontsize": 8})
fig, ax = plt.subplots(ncols=2, sharex=True, figsize=(6.75, 8.5))
fig.suptitle("What do YOU think ... vs What do EXPERTS think ...")
np.vectorize(lambda x: x.set_xticks([0., 0.2, 0.4, 0.6, 0.8, 1.]))(ax)
np.vectorize(lambda x: x.set_xlim(0., 1.))(ax)
ax[0].set_xlabel("Agreement with Experts")
ax[1].set_xlabel("Agreement with Experts")
np.vectorize(lambda x: x.grid(linestyle="--"))(ax)
plot.PlotQuestionConfidenceComparison(binary, binary_e_class, num_you, colors_ge, colors_e, ax)
ax[0].set_ylim(15.5, 0.5)
ax[1].set_ylim(15.5, 0.5)
legend_labels = [
    matplotlib.lines.Line2D([0], [0], color=colors_ge[1], lw=6),
    matplotlib.lines.Line2D([0], [0], color=colors_ge[0], lw=6),
    matplotlib.lines.Line2D([0], [0], color=colors_e[1], lw=6),
    matplotlib.lines.Line2D([0], [0], color=colors_e[0], lw=6)
]
ax[1].legend(legend_labels, ["GE: EXPERT", "GE: YOU", "E: EXPERT", "E: YOU"], loc="lower left")
fig.tight_layout()
#plt.show()
fig.savefig("fig_3_questions")
plt.rcdefaults()
plt.style.use("paper.mplstyle")

#####
# Figure 4 - QuestionWise Comparison
#####

print("Start Figure 4")
fig, ax = plt.subplots(nrows=2, figsize=(6.75, 4.75), sharex=True, sharey=True)
d_ax = [a.twinx() for a in ax]
ax[1].set_xlabel("Question")
ax[1].set_ylabel("\n".join(textwrap.wrap("GE-CLASS: Average Agreement with Experts", width=25)))
ax[0].set_ylabel("\n".join(textwrap.wrap("E-CLASS: Average Agreement with Experts", width=25)))
d_ax[0].set_ylabel(r"$\vert$ Cohen's d $\vert$")
d_ax[1].set_ylabel(r"$\vert$ Cohen's d $\vert$")
order = plot.PlotQuestionWiseComparison(disagreement, disagreement_e_class, num_you, colors_ge, colors_e, ax)
plot.PlotCohensD(disagreement_e_class, num_you, order, d_ax[0])
plot.PlotCohensD(disagreement, num_you, order, d_ax[1])
d_ax[0].set_ylim(0., 0.6)
d_ax[1].set_ylim(0., 0.6)
ax[0].legend(loc='best')
ax[1].legend(bbox_to_anchor=(0.12, 0.95), loc='upper left')
plot.label_axis("a", ax[0], position=(0.93, 0.2))
plot.label_axis("b", ax[1], position=(0.93, 0.2))
ax[0].xaxis.grid(True)
ax[1].xaxis.grid(True)
ax[0].set_zorder(1)
ax[0].patch.set_visible(False)
ax[1].set_zorder(1)
ax[1].patch.set_visible(False)
#plt.show()
fig.tight_layout()
fig.savefig("fig_4_significance")
