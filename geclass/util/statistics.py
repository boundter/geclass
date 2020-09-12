import math

import numpy as np
import scipy.stats as stats


def aggregate_mean(aggregate):
    """Calculate the mean over all the cols of a ResponseAggregate."""
    total = 0
    for col in aggregate:
        total += sum(col)
    return total/len(aggregate)


def aggregate_stderr(aggregate, mean=None):
    """Calculate the standard error of the mean of all the cols of a
    ResponseAggregate."""
    if mean is None:
        mean = aggregate_mean(aggregate)
    total = 0
    for col in aggregate:
        for point in col:
            total += (point - mean)**2
    return math.sqrt(1./(len(aggregate) - 1.)*total)/math.sqrt(len(aggregate))


def aggregate_mean_colwise(aggregate, significance=0.05):
    """Calculate the colwise mean of a ResponseAggregate."""
    mean = []
    n_likert = 2  # agree or disagree with experts
    B = stats.chi2.ppf(1 - significance / n_likert, 2)
    for col in aggregate:
        mean.append((sum(col) + B / 2.) / (aggregate.size() + B))
    return np.array(mean)


def aggregate_confidence_colwise(aggregate, significance=0.05):
    """Calculate the colwise confidence of a ResponseAggregate."""
    confidence = []
    n_likert = 2  # agree or disagree with experts
    B = stats.chi2.ppf(1 - significance / n_likert, 2)
    for col in aggregate:
        n = sum(col)
        n_total = aggregate.size()
        confidence.append(np.sqrt(
            ((B**2) / 4. + B * n * (1. - float(n) / n_total))
            / (n_total + B)**2
        ))
    return np.array(confidence)

