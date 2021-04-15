import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import util.data_handling as data_handling
import util.plot as plot
from util.static_variables import QUESTIONS, QUESTIONS_MARK

color_you = "black"
color_expert = "gray"
color_pre = "gray"
color_post = "black"


def PlotOverallComparison(compact, outfile=None):
    fig, ax = plt.subplots()
    ax.set_xticks([1., 2.75])
    ax.set_xticklabels(["Pre", "Post"])
    ax.set_ylabel("Agreement with Experts")
    plot.PlotCourse(compact, [0.75, 1.25, 2.5, 3.], [color_you, color_expert],
                    ax)

    legend_labels = [
        matplotlib.lines.Line2D([0], [0], color=color_you, alpha=0.75, lw=6),
        matplotlib.lines.Line2D([0], [0], color=color_expert, alpha=0.75, lw=6),
    ]
    ax.legend(legend_labels,
              ["What do YOU think ...", "What do EXPERTS think ..."],
              loc="lower left")

    ax.set_ylim(0., 1.)
    fig.tight_layout()
    if outfile is None:
        plt.show()
    else:
        fig.savefig(outfile)
    plt.close()


def PlotDistribution(disagreement_compact, you_expert, outfile=None):
    fig, ax = plt.subplots()
    ax.set_xlabel("Score")
    ax.set_ylabel("Cumulative Likelihood for {}-Questions".format(you_expert.upper()))
    plot.PlotCumulativeDistribution(
            disagreement_compact, you_expert, colors=[color_pre, color_post],
            labels=["Pre", "Post"], ax=ax
    )
    ax.set_xlim(-15., 30.)
    ax.legend(loc="upper left")
    fig.tight_layout()
    if outfile is None:
        plt.show()
    else:
        fig.savefig(outfile)
    plt.close()


def PlotFlatComparison(data, num_you, significance=0.05):
    fig, ax = plt.subplots(figsize=(7.5, 3.5))
    ax.set_xlabel("Question Number")
    ax.set_ylabel("Average Agreement with Experts")
    plot.PlotQuestionComparison(data, num_you, colors=[color_pre, color_post],
                                ax=ax, significance=significance)
    ax.legend(loc="best")
    plt.show()


def PlotComparison(data, num_you):
    answers_pre, answers_post, answers_expert_pre, answers_expert_post = \
        data_handling.AggregateAnswersQuestionwise(data, num_you)
    mean_pre = [np.mean(x) for x in answers_pre]
    sorted_indx = np.argsort(mean_pre)
    total_size = len(answers_pre)
    half_size = total_size // 2
    fig, ax = plt.subplots(ncols=2, sharex=True, figsize=(7, 7.5))
    fig.suptitle("What do YOU think ... vs. What do EXPERTS think")
    np.vectorize(lambda x: x.set_xticks([0., 0.2, 0.4, 0.6, 0.8, 1.]))(ax)
    np.vectorize(lambda x: x.set_xlim(0., 1.))(ax)
    ax[0].set_xlabel("Agreement with Experts")
    ax[1].set_xlabel("Agreement with Experts")
    plot.LabelQuestions(total_size, half_size, sorted_indx, QUESTIONS, ax)
    np.vectorize(lambda x: x.grid(linestyle="--"))(ax)

    for i in range(total_size - half_size):
        plot.PlotQuestionPoint(
            height=i+1.12,
            data_pre=answers_pre[sorted_indx[i]],
            data_post=answers_post[sorted_indx[i]],
            color=color_you,
            ax=ax[0]
        )
        plot.PlotQuestionPoint(
            height=i+0.88,
            data_pre=answers_expert_pre[sorted_indx[i]],
            data_post=answers_expert_post[sorted_indx[i]],
            color=color_expert,
            ax=ax[0]
        )

    for i in range(half_size):
        plot.PlotQuestionPoint(
            height=i+1.12,
            data_pre=answers_pre[sorted_indx[i + half_size]],
            data_post=answers_post[sorted_indx[i + half_size]],
            color=color_you,
            ax=ax[1]
        )
        plot.PlotQuestionPoint(
            height=i+0.88,
            data_pre=answers_expert_pre[sorted_indx[i + half_size]],
            data_post=answers_expert_post[sorted_indx[i + half_size]],
            color=color_expert,
            ax=ax[1]
        )

    legend_labels = [
        matplotlib.lines.Line2D([0], [0], color=color_you, lw=6),
        matplotlib.lines.Line2D([0], [0], color=color_expert, lw=6)
    ]
    ax[0].legend(legend_labels, ["YOU", "EXPERT"], loc="lower left")

    fig.tight_layout()
    plt.show()


def PlotMarkComparison(data, num_mark):
    answers = []
    for col in ["q_mark_" + str(i) for i in range(1, num_mark + 1)]:
        q_answers = np.array([x for x in data[col] if x != -998])
        answers.append(q_answers)
    mean = [np.mean(x) for x in answers]
    sorted_indx = np.argsort(mean)
    total_size = len(sorted_indx)
    half_size = total_size // 2

    fig, ax = plt.subplots(ncols=2, sharex=True, figsize=(7, 7.5))
    fig.suptitle("How important for earning a good grade in this class was ...")
    np.vectorize(lambda x: x.set_xticks([0., 0.2, 0.4, 0.6, 0.8, 1.]))(ax)
    np.vectorize(lambda x: x.set_xlim(0., 1.))(ax)
    ax[0].set_xlabel("Agreement with Experts")
    ax[1].set_xlabel("Agreement with Experts")
    plot.LabelQuestions(total_size, half_size, sorted_indx, QUESTIONS, ax)
    np.vectorize(lambda x: x.grid(linestyle="--"))(ax)

    for i in range(total_size - half_size):
        plot.PlotQuestionPoint(
            height=i+1,
            data_pre=answers[sorted_indx[i]],
            data_post=answers[sorted_indx[i]],
            color=color_you,
            ax=ax[0]
        )

    for i in range(half_size):
        plot.PlotQuestionPoint(
            height=i+1,
            data_pre=answers[sorted_indx[i + half_size]],
            data_post=answers[sorted_indx[i + half_size]],
            color=color_you,
            ax=ax[1]
        )
    fig.tight_layout()
    plt.show()
