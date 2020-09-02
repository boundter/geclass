import math

import numpy as np


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


def aggregate_mean_colwise(aggregate):
    """Calculate the colwise mean of a ResponseAggregate."""
    mean = []
    for col in aggregate:
        mean.append(np.mean(col))
    return np.array(mean)


def aggregate_confidence_colwise(aggregate):
    """Calculate the colwise confidence of a ResponseAggregate."""
    confidence = []
    for col in aggregate:
        confidence.append(np.std(col))
    return np.array(confidence)

