import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

# TODO: Use styelsheet

colors = {'your_course_you': 'red',
          'your_course_expert': 'blue',
          'similar_course': 'gray'}


def comparing_barplot(
        left_mean, right_mean, title, labels, left_error=None,
        right_error=None):
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_ylabel('Anteil der Studenten')
    ax.set_xticks(np.arange(0, len(labels)))
    ax.set_xticklabels(labels)

    BAR_WIDTH = 0.3
    left_bar_location = np.arange(-BAR_WIDTH/2., len(labels)-1, step=1)
    right_bar_location = np.arange(BAR_WIDTH/2., len(labels), step=1)

    ax.bar(
        left_bar_location, left_mean, width=BAR_WIDTH, yerr=left_error,
        color="red", label="Ihr Kurs")
    ax.bar(
        right_bar_location, right_mean, width=BAR_WIDTH, yerr=right_error,
        color="gray", label="Ähnliche Kurse")

    ax.set_ylim(0., 1.)
    ax.set_xlim(-0.8, len(labels) - 0.2)

    ax.legend()
    return fig, ax


def change_plot(
        pre_course_upper, pre_course_lower, post_course_upper, post_course_lower,
        type_upper, type_lower, questions):
    indx_sorted = np.argsort(pre_course_upper.mean)

    fig, ax = plt.subplots(ncols=2, nrows=1, sharex=True)

    # questions as labels
    ax[1].yaxis.tick_right()
    ax[1].set_yticks(np.arange(-len(indx_sorted)/2, -len(indx_sorted), -1))
    ax[0].set_yticks(np.arange(0, -len(indx_sorted)/2, -1))
    ax[0].set_yticklabels(indx_sorted[:len(indx_sorted)//2])
    ax[1].set_yticklabels(indx_sorted[len(indx_sorted)//2:])

    def add_point(ax_indx, indx, course_pre, course_post, course_type, offset):
        axindx = 0 if ax_indx < len(indx_sorted)/2 else 1
        ax[axindx].errorbar(
            course_pre.mean[indx], -ax_indx+offset,
            xerr=course_pre.confidence[indx].reshape((2, 1)),
            fmt="o",
            markerfacecolor=colors[course_type],
            markeredgecolor=colors[course_type],
            ecolor=to_rgba(colors[course_type], alpha=0.8),
            zorder=5,
            elinewidth=5)
        ax[axindx].arrow(course_pre.mean[indx], -ax_indx+offset,
                         dx=course_post.mean[indx] - course_pre.mean[indx],
                         dy=0,
                         facecolor=colors[course_type],
                         zorder=6,
                         head_width=0.12,
                         head_length=0.01)

    for ax_indx, indx in enumerate(indx_sorted):
        add_point(ax_indx, indx, pre_course_upper,
                  post_course_upper, type_upper, -0.2)
        add_point(ax_indx, indx, pre_course_lower,
                  post_course_lower, type_lower, 0.2)

    ax[0].set_xlim(0., 1.)
    return fig, ax

if __name__ == "__main__":
    left = [0.5, 0.6]
    right = [0.7, 0.8]
    title = "I don't know what to write"
    label = ["pre", "post"]
    left_err = [0.2, 0.3]
    right_err = [0.1, 0.05]
    #fig, ax = comparing_barplot(left, right, title, label, left_err, right_err)
    #plt.show()

    from report_data import CoursePartData
    n = 30
    upper_pre = CoursePartData(np.random.random(n), np.random.rand(n, 2))
    upper_post = CoursePartData(np.random.random(n), np.random.rand(n, 2))
    lower_pre = CoursePartData(np.random.random(n), np.random.rand(n, 2))
    lower_post = CoursePartData(np.random.random(n), np.random.rand(n, 2))
    fig, ax = change_plot(upper_pre, lower_pre, upper_post, lower_post, 'your_course_you', 'your_course_expert', None)
    plt.show()