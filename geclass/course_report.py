import numpy as np
import matplotlib.pyplot as plt

# TODO: Use styelsheet

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

if __name__ == "__main__":
    left = [0.5, 0.6]
    right = [0.7, 0.8]
    title = "I don't know what to write"
    label = ["pre", "post"]
    left_err = [0.2, 0.3]
    right_err = [0.1, 0.05]
    fig, ax = comparing_barplot(left, right, title, label, left_err, right_err)
    plt.show()


