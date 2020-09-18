"""Functions to generate the plots for the report.

Only generate_plots is needed to create all the plots.
"""

from enum import Enum
import textwrap

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from geclass.util.questions import questions, q_marks
from geclass.util.statistics import (
        aggregate_mean, aggregate_stderr, aggregate_mean_colwise,
        aggregate_confidence_colwise
)

plt.rcParams['pgf.texsystem'] = 'pdflatex'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['text.usetex'] = True
plt.rcParams['pgf.rcfonts'] = False
plt.rcParams['pgf.preamble'] = '\\usepackage[utf8x]{inputenc}'
plt.rcParams['savefig.format'] = 'pgf'

def _get_total_fraction_expertlike(responses):
    """Get the mean and standard error over all q_you questions.

    Args:
        responses (QuestionnaireResponses): The answers to the questionnaire.

    Returns:
        (mean, stderr) for all answers.

    """
    mean = (
        aggregate_mean(responses.q_you_pre),
        aggregate_mean(responses.q_you_post)
    )
    stderr = (
        aggregate_stderr(responses.q_you_pre, mean=mean[0]),
        aggregate_stderr(responses.q_you_post, mean=mean[1])
    )
    return mean, stderr


def overall_score_plot(responses_course, responses_similar, outfile=None):
    """Plot a barplot of the fraction of all expertlike responses.

    Args:
        responses_course (QuestionnaireResponses): The answers to the
            questionnaire for the course.
        responses_similar (QuestionnaireResponses): The answers to the
            questionnaire for similar courses.
        outfile (str, optional): The file name to save the plot to. If it is
            None the plot will be shown.

    """
    mean, stderr = _get_total_fraction_expertlike(responses_course)
    mean_sim, stderr_sim = _get_total_fraction_expertlike(responses_similar)
    color_you = 'red'
    color_similar = 'gray'

    fig, ax = plt.subplots(figsize=(5.5, 5))
    ax.set_title('Gesamtergebnisse der GE-CLASS für\ndie "`Was denken Sie..."\''
                 'Antworten')
    ax.set_xticks([1., 2.75])
    ax.set_xticklabels(['Prä', 'Post'])
    ax.set_ylabel('Anteil der gleichen\nAntworten wie Experten')
    ax.set_ylim(0., 1.)

    def plot_bar(x, y, yerr, color, text_offset=0.01):
        bar_style = {
            'width': 0.5,
            'edgecolor': 'black',
            'capsize': 5,
        }
        ax.bar(x, y, yerr=yerr, color=color, **bar_style)
        ax.text(x - bar_style['width']/2, y + text_offset, '{:.2f}'.format(y))

    plot_bar(0.75, mean_sim[0], stderr_sim[0], color_similar)
    plot_bar(1.25, mean[0], stderr[0], color_you)
    plot_bar(2.5, mean_sim[1], stderr_sim[1], color_similar)
    plot_bar(3., mean[1], stderr[1], color_you)

    legend_labels = [
        matplotlib.lines.Line2D([0], [0], color=color_you, lw=6),
        matplotlib.lines.Line2D([0], [0], color=color_similar, lw=6),
    ]
    ax.legend(legend_labels, ['Dieser Kurs', 'Ähnliche Kurse'],
              loc='lower left')
    fig.tight_layout()
    if outfile is None:
        plt.show()
    else:
        fig.savefig(outfile)
        plt.close()


def _response_statistics(responses, you_expert):
    """Get the mean of pre, shift of mean and confidence interval of pre.

    Args:
        responses (QuestionnaireResponses): The answers to the questionnaire.
        you_expert (str): Can be either 'you' or 'expert' and for which types
            of answers to compute the statistics.

    Returns:
        (mean, d_mean, confidence) statistics for the questionnaire.

    """
    mean_pre = aggregate_mean_colwise(
            getattr(responses, 'q_{}_pre'.format(you_expert)))
    mean_post = aggregate_mean_colwise(
            getattr(responses, 'q_{}_post'.format(you_expert)))
    d_mean = mean_post - mean_pre
    confidence = aggregate_confidence_colwise(
            getattr(responses, 'q_{}_pre'.format(you_expert)))
    return mean_pre, d_mean, confidence


def _mark_statistics(responses):
    """Get the mean and confidence interval for the mark questions.

    Args:
        responses (QuestionnaireResponses): The answers to the questionnaire.

    Returns:
        (mean, confidence) statistics for the mark questions.

    """
    mean = aggregate_mean_colwise(responses.q_mark)
    confidence = aggregate_confidence_colwise(responses.q_mark)
    return mean, confidence


class OverviewPlotTypes(Enum):
    """Enumerator to decide the type of plot in question_overview_plot."""
    YOU_SIMILAR = 1
    EXPERT_SIMILAR = 2
    YOU_EXPERT = 3
    MARK = 4


def question_overview_plot(responses_1, responses_2, plot_type, outfile=None):
    """Plot fraction of expertlike answers split up by questions.

    Args:
        responses_1 (QuestionnaireResponses): The answers to the
            questionnaire for lower points (typically the current course).
        responses_2 (QuestionnaireResponses): The answers to the
            questionnaire for the upper points (typically similar courses).
        plot_type (OverviewPlotTypes): The type of the plot. This changes the
            colors, the legend, title and decides which type of questions to
            use (you, expert, mark).
        outfile (str, optional): The file name to save the plot to. If it is
            None the plot will be shown.

    """
    color = {
        'you': 'red',
        'expert': 'blue',
        'similar': 'gray'
    }
    if plot_type == OverviewPlotTypes.YOU_SIMILAR:
        title = 'Was denken Sie?'
        color_1 = color['you']
        color_2 = color['similar']
        legend_text = ['Dieser Kurs', 'Ähnliche Kurse']
        mean_1, d_mean_1, confidence_1 = _response_statistics(
                responses_1, 'you')
        mean_2, d_mean_2, confidence_2 = _response_statistics(
                responses_2, 'you')
        sorted_indx = np.argsort(mean_2)
        question_labels = [
            'Q{:d}: {}'.format(i+1, q)
            for i, q in zip(sorted_indx, np.array(questions)[sorted_indx])
        ]
    elif plot_type == OverviewPlotTypes.EXPERT_SIMILAR:
        title = 'Was denken Experten?'
        color_1 = color['expert']
        color_2 = color['similar']
        legend_text = ['Dieser Kurs', 'Ähnliche Kurse']
        mean_1, d_mean_1, confidence_1 = _response_statistics(
                responses_1, 'expert')
        mean_2, d_mean_2, confidence_2 = _response_statistics(
                responses_2, 'expert')
        sorted_indx = np.argsort(mean_2)
        question_labels = [
            'Q{:d}: {}'.format(i+1, q)
            for i, q in zip(sorted_indx, np.array(questions)[sorted_indx])
        ]
    elif plot_type == OverviewPlotTypes.YOU_EXPERT:
        title = 'Was denken Sie? vs. Was denken Experten?'
        color_1 = color['you']
        color_2 = color['expert']
        legend_text = ['Was denken Sie?', 'Was denken Experten?']
        mean_1, d_mean_1, confidence_1 = _response_statistics(
                responses_1, 'you')
        mean_2, d_mean_2, confidence_2 = _response_statistics(
                responses_2, 'expert')
        sorted_indx = np.argsort(mean_2)
        question_labels = [
            'Q{:d}: {}'.format(i+1, q)
            for i, q in zip(sorted_indx, np.array(questions)[sorted_indx])
        ]
    elif plot_type == OverviewPlotTypes.MARK:
        title = 'Wie wichtig für eine gute Note im Praktikum war ...'
        color_1 = color['you']
        color_2 = color['similar']
        legend_text = ['Dieser Kurs', 'Ähnliche Kurse']
        mean_1, confidence_1 = _mark_statistics(responses_1)
        d_mean_1 = np.zeros_like(mean_1)
        mean_2, confidence_2 = _mark_statistics(responses_2)
        d_mean_2 = np.zeros_like(mean_2)
        sorted_indx = np.argsort(mean_2)
        question_labels = [
            'Q{:d}: {}'.format(i+1, q)
            for i, q in zip(sorted_indx, np.array(q_marks)[sorted_indx])
        ]
    else:
        raise ValueError('plot_type unknown for question_overview_plot.')

    total_size = len(sorted_indx)
    half_size = total_size // 2

    fig, ax = plt.subplots(ncols=2, sharex=True, figsize=(7, 7.5))
    fig.suptitle(title)
    np.vectorize(lambda x: x.set_xticks([0., 0.2, 0.4, 0.6, 0.8, 1.]))(ax)
    np.vectorize(lambda x: x.set_xlim(0., 1.))(ax)
    ax[1].yaxis.tick_right()
    ax[0].set_yticks([i for i in range(total_size - half_size + 2)])
    ax[1].set_yticks([i for i in range(half_size + 2)])
    question_labels = ['\n'.join(textwrap.wrap(q, 40)) for q in question_labels]
    ax[0].set_yticklabels(
        ['', *question_labels[:total_size - half_size], ''],
        fontdict={'fontsize': '5'}
    )
    ax[1].set_yticklabels(
        ['', *question_labels[total_size - half_size:], ''],
        fontdict={'fontsize': '5'}
    )
    ax[0].set_ylim(total_size - half_size + 1, 0)
    ax[1].set_ylim(half_size + 1, 0)
    np.vectorize(lambda x: x.grid(linestyle='--'))(ax)

    def plot_point(mean, d_mean, confidence, height, color, ax):
        ax.plot(mean, height, 'o', color=color, zorder=2)
        ax.errorbar(
            mean, height, xerr=confidence, color=color, alpha=0.5,
            elinewidth=5, zorder=0
        )
        if d_mean != 0:
            ax.arrow(
                mean, height, d_mean, 0, head_width=.1, head_length=.05,
                facecolor=color, length_includes_head=True, zorder=1)

    for i in range(total_size - half_size):
        plot_point(
            mean_1[sorted_indx][i],
            d_mean_1[sorted_indx][i],
            confidence_1[sorted_indx][i],
            i + 1.12,
            color_1,
            ax[0],
        )
        plot_point(
            mean_2[sorted_indx][i],
            d_mean_2[sorted_indx][i],
            confidence_2[sorted_indx][i],
            i + 0.88,
            color_2,
            ax[0],
        )
    for i in range(half_size):
        plot_point(
            mean_1[sorted_indx][i + half_size],
            d_mean_1[sorted_indx][i + half_size],
            confidence_1[sorted_indx][i + half_size],
            i + 1.12,
            color_1,
            ax[1],
        )
        plot_point(
            mean_2[sorted_indx][i + half_size],
            d_mean_2[sorted_indx][i + half_size],
            confidence_2[sorted_indx][i + half_size],
            i + 0.88,
            color_2,
            ax[1],
        )

    legend_labels = [
        matplotlib.lines.Line2D([0], [0], color=color_1, lw=6),
        matplotlib.lines.Line2D([0], [0], color=color_2, lw=6)
    ]
    ax[0].legend(
        legend_labels, legend_text, loc='upper right', fontsize=8,
        bbox_to_anchor=(0., 1.02))

    fig.tight_layout()
    if outfile is None:
        plt.show()
    else:
        fig.savefig(outfile)
        plt.close()


def generate_plots(responses_course, responses_similar):
    """Generate all plots needed for the report."""
    overall_score_plot(responses_course, responses_similar, 'overall_score')
    question_overview_plot(
            responses_course, responses_similar, OverviewPlotTypes.YOU_SIMILAR,
            'overview_you')
    question_overview_plot(
            responses_course, responses_similar,
            OverviewPlotTypes.EXPERT_SIMILAR, 'overview_expert')
    question_overview_plot(
            responses_course, responses_course, OverviewPlotTypes.YOU_EXPERT,
            'overview_you_expert')
    question_overview_plot(
            responses_course, responses_similar, OverviewPlotTypes.MARK,
            'overview_mark')
