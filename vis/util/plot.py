import textwrap

import numpy as np
import matplotlib
import scipy.stats as stats

import util.data_handling as data_handling
import util.statistics as statistics
from util.static_variables import QUESTIONS


def label_axis(label, ax, position=(-0.1, 1.07)):
    text_func = getattr(ax, "text")
    text_func(
            *position, r"$\textbf{{({})}}$".format(label),
            transform=ax.transAxes)

def PlotCourse(compact, positions, colors, ax):
    q_you_pre, q_you_post, q_expert_pre, q_expert_post, q_mark = \
        data_handling.AggregateAnswers(compact)

    def PlotBar(x, data, color, ax, text_offset=0.015):
        bar_style = {
            "width": 0.5,
            "edgecolor": "black",
            "capsize": 5
        }
        y = np.mean(data)
        err = np.std(data)/np.sqrt(data.shape[0])
        print("{:.5f} +- {:.5f} -> [{:.5f}, {:.5f}]".format(y, err, y-err, y+err))
        ax.bar(x, y, yerr=err, color=color, **bar_style, alpha=0.75)
        ax.text(x - bar_style["width"]/2., y + text_offset, "{:.2f}".format(y))

    print("\t\tYou Pre: ", end="")
    PlotBar(positions[0], q_you_pre, color=colors[0], ax=ax)
    print("\t\tExpert Pre: ", end="")
    PlotBar(positions[1], q_expert_pre, color=colors[1], ax=ax)
    print("\t\tYou Post: ", end="")
    PlotBar(positions[2], q_you_post, color=colors[0], ax=ax)
    print("\t\tExpert Post: ", end="")
    PlotBar(positions[3], q_expert_post, color=colors[1], ax=ax)

    print("")
    print(f"\t\tCohen's d You: {statistics.CohensD(q_you_pre, q_you_post)}")
    print(f"\t\tMann-Whitney U You: {stats.mannwhitneyu(q_you_pre, q_you_post)[1]}")
    print("")
    print(f"\t\tCohen's d Expert: {statistics.CohensD(q_expert_pre, q_expert_post)}")
    print(f"\t\tMann-Whitney U Expert: {stats.mannwhitneyu(q_expert_pre, q_expert_post)[1]}")


def PlotOverallCourseComparison(compact_ge, compact_e, colors_ge, colors_e, ax):
    positions_ge = [0.75, 1.75, 3.75, 4.75]
    positions_e = [1.25, 2.25, 4.25, 5.25]
    ax.set_xticks([1.5, 4.5])
    ax.set_xticklabels(["Pre", "Post"])
    print("\tResults GE-Class:")
    PlotCourse(compact_ge, positions_ge, colors_ge, ax)
    print("\tResults E-Class:")
    PlotCourse(compact_e, positions_e, colors_e, ax)
    ax.set_ylabel("Agreement with Experts")
    legend_labels = [
        matplotlib.lines.Line2D([0], [0], color=colors_ge[0], alpha=0.75, lw=6),
        matplotlib.lines.Line2D([0], [0], color=colors_e[0], alpha=0.75, lw=6),
        matplotlib.lines.Line2D([0], [0], color=colors_ge[1], alpha=0.75, lw=6),
        matplotlib.lines.Line2D([0], [0], color=colors_e[1], alpha=0.75, lw=6),
    ]
    ax.legend(legend_labels,
            ["GE: YOU", "E: YOU", "GE: EXPERTS", "E: EXPERTS"],
              loc="lower left")
    ax.set_ylim(0., 1.)
    statistics.CompareCourseStatistics(compact_ge, compact_e)


def PlotCumulativeDistribution(disagreement_compact, you_expert, colors, labels,
                               ax):
    agreement_pre = []
    agreement_post = []

    def GetPoints(row, col):
        ans = np.array([x for x in row[col] if x != -998])
        return np.sum(ans)

    for _, student in disagreement_compact.iterrows():
        agreement_pre.append(
            GetPoints(student, "q_{}_pre".format(you_expert))
        )
        agreement_post.append(
            GetPoints(student, "q_{}_post".format(you_expert))
        )

    style = {
        "density": True,
        "bins": np.linspace(-30., 30., 61),
        "range": (0., 1.),
        "cumulative": True,
        "histtype": "step",
    }
    ax.hist(agreement_pre, color=colors[0], **style, label=labels[0])
    ax.hist(agreement_post, color=colors[1], **style, label=labels[1])


def PlotHistogramDistribution(disagreement_compact, you_expert, colors, ax):
    agreement_pre = []
    agreement_post = []

    def GetPoints(row, col):
        ans = np.array([x for x in row[col] if x != -998])
        return np.sum(ans)

    for _, student in disagreement_compact.iterrows():
        agreement_pre.append(
            GetPoints(student, "q_{}_pre".format(you_expert))
        )
        agreement_post.append(
            GetPoints(student, "q_{}_post".format(you_expert))
        )
    style = {
        "density": True,
        "bins": np.linspace(-30., 30., 12),
        "facecolor": "None"
    }
    ax.hist(agreement_pre, edgecolor=colors[0], **style)
    ax.hist(agreement_post, edgecolor=colors[1], **style)


def PlotDistributions(disagreement_compact_ge, disagreement_compact_e,
                      colors_ge, colors_e, axes):
    PlotCumulativeDistribution(
            disagreement_compact_e, "you", colors=colors_e,
            labels=["E: Pre", "E: Post"], ax=axes[0]
    )
    PlotCumulativeDistribution(
            disagreement_compact_ge, "you", colors=colors_ge,
            labels=["GE: Pre", "GE: Post"], ax=axes[0]
    )
    PlotCumulativeDistribution(
            disagreement_compact_e, "expert", colors=colors_e,
            labels=["E: Pre", "E: Post"], ax=axes[1]
    )
    PlotCumulativeDistribution(
            disagreement_compact_ge, "expert", colors=colors_ge,
            labels=["GE: Pre", "GE: Post"], ax=axes[1]
    )


def PlotQuestionComparison(binary, num_you, colors, ax,
                           order=None, significance=0.05):
    answers_pre, answers_post, answers_expert_pre, answers_expert_post = \
        data_handling.AggregateAnswersQuestionwise(binary, num_you)
    p = statistics.CalculateYouSignificance(binary, num_you)
    mean_pre = np.array([np.mean(x) for x in answers_pre])
    mean_post = np.array([np.mean(x) for x in answers_post])
    sorted_indx = np.argsort(mean_pre)
    if order is not None:
        sorted_indx = order
    rejected_null = np.where(p[sorted_indx] < significance)[0]
    ax.set_xticks(np.arange(num_you))
    ax.set_xticklabels(sorted_indx + 1)
    for tick in ax.xaxis.get_major_ticks():
                    tick.label.set_fontsize(8)
    ax.plot(np.arange(num_you), mean_post[sorted_indx], linestyle="-",
            marker="o", color=colors[0], linewidth=0.5, label="Post")
    ax.plot(np.arange(num_you), mean_pre[sorted_indx], linestyle="--",
            marker="s", color=colors[1], linewidth=0.5, markerfacecolor="white",
            label="Pre")
    offset = 0.1
    ax.plot(rejected_null,
            np.maximum(mean_post[sorted_indx], mean_pre[sorted_indx])[rejected_null] + offset,
            marker="*", color="black", linestyle="None")
    return np.argsort(mean_pre)


def PlotQuestionWiseComparison(binary_ge, binary_e, num_you, colors_ge, colors_e,
                               axes, significance=0.05):
    order = PlotQuestionComparison(binary_ge, num_you, colors_ge, axes[1])
    order_e = PlotQuestionComparison(binary_e, num_you, colors_e, axes[0],
                                     order=order)
    print("\tOrder GE-Class: ", end="")
    print([f"{i + 1:02d}" for i in order])
    print("\tOrder E-Class:  ", end="")
    print([f"{i + 1:02d}" for i in order_e])
    return order


def PlotQuestionPoint(height, data_pre, data_post, color, ax, threshold=1e-3):
    err = statistics.CalcConfidence(data_pre, data_pre.shape[0])
    ax.plot(np.mean(data_pre), height, "s", color=color, markerfacecolor="white", zorder=3)
    ax.errorbar(np.mean(data_pre), height, xerr=err, color=color, alpha=0.5, elinewidth=5, zorder=0)
    if np.abs(np.mean(data_post) - np.mean(data_pre)) > threshold:
        ax.arrow(
            np.mean(data_pre),
            height,
            np.mean(data_post) - np.mean(data_pre),
            0,
            head_width=.1,
            head_length=.01,
            facecolor=color,
            length_includes_head=True,
            zorder=2
        )


def LabelQuestions(total_size, half_size, sorted_indx, questions, ax):
    question_labels = ["Q{:d}: {}".format(i+1, q) for i, q in zip(sorted_indx, questions[sorted_indx])]
    question_labels = ["\n".join(textwrap.wrap(q, 30)) for q in question_labels]
    ax[1].yaxis.tick_right()
    ax[0].set_yticks([i for i in range(total_size - half_size + 2)])
    ax[1].set_yticks([i for i in range(half_size + 2)])
    ax[0].set_yticklabels(
        ["", *question_labels[:total_size - half_size], ""],
        fontdict={"fontsize": "5"}
    )
    ax[1].set_yticklabels(
        ["", *question_labels[total_size - half_size:], ""],
        fontdict={"fontsize": "5"}
    )
    ax[0].set_ylim(total_size - half_size + 1., 0.)
    ax[1].set_ylim(half_size + 1., 0.)


def PlotQuestionConfidenceComparison(binary_ge, binary_e, num_you, colors_ge, colors_e, ax):
    answers_pre, answers_post, answers_expert_pre, answers_expert_post = \
        data_handling.AggregateAnswersQuestionwise(binary_ge, num_you)
    answers_pre_e, answers_post_e, answers_expert_pre_e, answers_expert_post_e = \
        data_handling.AggregateAnswersQuestionwise(binary_e, num_you)
    mean_pre = [np.mean(x) for x in answers_pre]
    mean_pre_e = [np.mean(x) for x in answers_pre_e]
    sorted_indx = np.argsort(mean_pre)
    total_size = len(answers_pre)
    half_size = total_size // 2
    LabelQuestions(total_size, half_size, sorted_indx, QUESTIONS, ax)

    for i in range(total_size - half_size):
        PlotQuestionPoint(
            height=i+0.875,
            data_pre=answers_pre[sorted_indx[i]],
            data_post=answers_post[sorted_indx[i]],
            color=colors_ge[0],
            ax=ax[0]
        )
        PlotQuestionPoint(
            height=i+0.625,
            data_pre=answers_expert_pre[sorted_indx[i]],
            data_post=answers_expert_post[sorted_indx[i]],
            color=colors_ge[1],
            ax=ax[0]
        )
        PlotQuestionPoint(
            height=i+1.375,
            data_pre=answers_pre_e[sorted_indx[i]],
            data_post=answers_post_e[sorted_indx[i]],
            color=colors_e[0],
            ax=ax[0]
        )
        PlotQuestionPoint(
            height=i+1.125,
            data_pre=answers_expert_pre_e[sorted_indx[i]],
            data_post=answers_expert_post_e[sorted_indx[i]],
            color=colors_e[1],
            ax=ax[0]
        )
        ax[0].axhline(i+1.5, color="black", linewidth=0.5)

    for i in range(half_size):
        PlotQuestionPoint(
            height=i+0.875,
            data_pre=answers_pre[sorted_indx[i + half_size]],
            data_post=answers_post[sorted_indx[i + half_size]],
            color=colors_ge[0],
            ax=ax[1]
        )
        PlotQuestionPoint(
            height=i+0.625,
            data_pre=answers_expert_pre[sorted_indx[i + half_size]],
            data_post=answers_expert_post[sorted_indx[i + half_size]],
            color=colors_ge[1],
            ax=ax[1]
        )
        PlotQuestionPoint(
            height=i+1.375,
            data_pre=answers_pre_e[sorted_indx[i + half_size]],
            data_post=answers_post_e[sorted_indx[i + half_size]],
            color=colors_e[0],
            ax=ax[1]
        )
        PlotQuestionPoint(
            height=i+1.125,
            data_pre=answers_expert_pre_e[sorted_indx[i + half_size]],
            data_post=answers_expert_post_e[sorted_indx[i + half_size]],
            color=colors_e[1],
            ax=ax[1]
        )
        ax[1].axhline(i+1.5, color="black", linewidth=0.5)


def PlotCohensD(disagreement, num_you, order, ax):
    d = statistics.CalculateCohensD(disagreement, num_you)
    ax.bar(np.arange(num_you), np.abs(d[order]), width=0.8, color="gray", alpha=0.5)
