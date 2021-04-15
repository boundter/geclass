import numpy as np
import scipy.stats as stats

import util.data_handling as data_handling


def CalcConfidence(data, n_total, significance=0.05):
    confidence = []
    n_likert = 4
    B = stats.chi2.ppf(1 - significance / n_likert, 2)
    n = np.sum(data)
    return np.sqrt(((B**2) / 4. + B*n*(1. - float(n)/n_total)) / (n_total + B)**2)


def CalculateYouSignificance(data, num_you):
    significance = []
    for i in range(1, num_you + 1):
        ans_pre = []
        ans_post = []
        for pre, post in zip(data["q_you_pre_" + str(i)], data["q_you_post_" + str(i)]):
            if pre == -998 or post == -998:
                continue
            ans_pre.append(pre)
            ans_post.append(post)
        #res = stats.ttest_rel(ans_pre, ans_post)
        res = stats.mannwhitneyu(ans_pre, ans_post)
        significance.append(res[1])
    return np.array(significance)


def CohensD(data_1, data_2):
    mean_1 = np.mean(data_1)
    mean_2 = np.mean(data_2)
    std_1 = np.std(data_1)
    std_2 = np.std(data_2)
    n_1 = data_1.shape[0]
    n_2 = data_2.shape[0]
    s = np.sqrt(((n_1 - 1)*std_1**2 + (n_2 - 1)*std_2**2)/(n_1 + n_2 - 2))
    return (mean_1 - mean_2) / s


def CalculateCohensD(data, num_you):
    d = []
    for i in range(1, num_you + 1):
        ans_pre = []
        ans_post = []
        for pre, post in zip(data["q_you_pre_" + str(i)], data["q_you_post_" + str(i)]):
            if pre != -998:
                ans_pre.append(pre)
            if post != -998:
                ans_post.append(post)
        d.append(CohensD(np.array(ans_pre), np.array(ans_post)))
    return np.array(d)


def CompareCourseStatistics(compact_ge, compact_e):
    q_you_pre, q_you_post, q_expert_pre, q_expert_post, q_mark = \
        data_handling.AggregateAnswers(compact_ge)
    q_you_pre_e, q_you_post_e, q_expert_pre_e, q_expert_post_e, q_mark_e = \
        data_handling.AggregateAnswers(compact_e)

    print("\tComparison GE-Class to E-Class You Pre: ")
    print(f"\t\tCohen's d: {CohensD(q_you_pre, q_you_pre_e)}")
    print(f"\t\tMann-Whitney U: {stats.mannwhitneyu(q_you_pre, q_you_pre_e)[1]}")
    print("\tComparison GE-Class to E-Class Expert Pre: ")
    print(f"\t\tCohen's d: {CohensD(q_expert_pre, q_expert_pre_e)}")
    print(f"\t\tMann-Whitney U: {stats.mannwhitneyu(q_expert_pre, q_expert_pre_e)[1]}")
    print("\tComparison GE-Class to E-Class You Post: ")
    print(f"\t\tCohen's d: {CohensD(q_you_post, q_you_post_e)}")
    print(f"\t\tMann-Whitney U: {stats.mannwhitneyu(q_you_post, q_you_post_e)[1]}")
    print("\tComparison GE-Class to E-Class Expert Post: ")
    print(f"\t\tCohen's d: {CohensD(q_expert_post, q_expert_post_e)}")
    print(f"\t\tMann-Whitney U: {stats.mannwhitneyu(q_expert_post, q_expert_post_e)[1]}")
