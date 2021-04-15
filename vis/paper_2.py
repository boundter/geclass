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
        disagreement_compact_e_class =  \
        e_class_util.PrepareMatchedData(df_post, df_pre, df_cis, num_you,
                                        num_mark)


#####
# Figure 1 - Overall Comparison
#####

fig, ax = plt.subplots()
plot.PlotOverallCourseComparison(compact_binary, compact_binary_e_class,
                                 colors_ge, colors_e, ax)
#plt.show()
fig.tight_layout()
fig.savefig("fig_1_overall.pdf")
plt.close()

#####
# Figure 2 - Distribution Comparison
#####

fig, ax = plt.subplots(nrows=2, figsize=(5, 4), sharex="col")
ax[1].set_xlabel("Reached Score")
ax[0].set_ylabel("\n".join(textwrap.wrap("Cumulative Likelihood for YOU-Questions", width=20)))
ax[1].set_ylabel("\n".join(textwrap.wrap("Cumulative Likelihood for EXPERT-Questions", width=20)))
plot.PlotDistributions(disagreement_compact, disagreement_compact_e_class, colors_ge,
                       colors_e, ax)
plot.label_axis("a", ax[0], position=(0.03, 0.875))
plot.label_axis("b", ax[1], position=(0.03, 0.875))
ax[0].legend(bbox_to_anchor=(1.05, 0.25), loc='upper left')
ax[0].set_xlim(-5., 30.)
#plt.show()
fig.tight_layout()
fig.savefig("fig_2_distribution.pdf")
plt.close()

#####
# Figure 3 - Question Comparison
#####

fig, ax = plt.subplots(ncols=2, sharex=True, figsize=(7, 7.5))
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
    matplotlib.lines.Line2D([0], [0], color=colors_ge[0], lw=6),
    matplotlib.lines.Line2D([0], [0], color=colors_ge[1], lw=6),
    matplotlib.lines.Line2D([0], [0], color=colors_e[0], lw=6),
    matplotlib.lines.Line2D([0], [0], color=colors_e[1], lw=6)
]
ax[1].legend(legend_labels, ["GE-YOU", "GE-EXPERT", "E-YOU", "E-EXPERT"], loc="lower left")
fig.tight_layout()
#plt.show()
fig.tight_layout()
fig.savefig("fig_3_questions.pdf")
plt.close()

#####
# Figure 4 - QuestionWise Comparison
#####

fig, ax = plt.subplots(nrows=2, figsize=(6.5, 5), sharex=True, sharey=True)
ax[1].set_xlabel("Question")
ax[1].set_ylabel("\n".join(textwrap.wrap("GE-CLASS: Average Agreement with Experts", width=25)))
ax[0].set_ylabel("\n".join(textwrap.wrap("E-CLASS: Average Agreement with Experts", width=25)))
plot.PlotQuestionWiseComparison(binary, binary_e_class, num_you, colors_ge, colors_e, ax)
ax[0].legend(loc='best')
ax[1].legend(loc='best')
plot.label_axis("a", ax[0], position=(0.93, 0.1))
plot.label_axis("b", ax[1], position=(0.93, 0.1))
ax[0].grid()
ax[1].grid()
#plt.show()
fig.tight_layout()
fig.savefig("fig_4_significance.pdf")
plt.close()
