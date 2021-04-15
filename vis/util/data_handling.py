import numpy as np
import pandas as pd


def Compactify(df, num_you, num_mark):
    aggregate = {
        "q_you_pre": [],
        "q_you_post": [],
        "q_expert_pre": [],
        "q_expert_post": [],
        "q_mark": []
    }
    for _, student in df.iterrows():
        """
        aggregate["course_id"].append(student["course_id"])
        aggregate["experience_id"].append(student["experience_id"])
        aggregate["program_id"].append(student["program_id"])
        aggregate["course_type_id"].append(student["course_type_id"])
        aggregate["traditional_id"].append(student["traditional_id"])
        """
        aggregate["q_you_pre"].append(
            [student["q_you_pre_" + str(x)] for x in range(1, num_you + 1)]
        )
        aggregate["q_you_post"].append(
            [student["q_you_post_" + str(x)] for x in range(1, num_you + 1)]
        )
        aggregate["q_expert_pre"].append(
            [student["q_expert_pre_" + str(x)] for x in range(1, num_you + 1)]
        )
        aggregate["q_expert_post"].append(
            [student["q_expert_post_" + str(x)] for x in range(1, num_you + 1)]
        )
        aggregate["q_mark"].append(
            [student["q_mark_" + str(x)] for x in range(1, num_mark + 1)]
        )
    return pd.DataFrame(aggregate)


def AggregateAnswers(compact):
    q_you_pre = []
    q_you_post = []
    q_expert_pre = []
    q_expert_post = []
    q_mark = []
    for _, row in compact.iterrows():
        q_you_pre += [x for x in row["q_you_pre"] if x != -998]
        q_you_post += [x for x in row["q_you_post"] if x != -998]
        q_expert_pre += [x for x in row["q_expert_pre"] if x != -998]
        q_expert_post += [x for x in row["q_expert_post"] if x != -998]
        q_mark += [x for x in row["q_mark"] if x != -998]
    q_you_pre = np.array(q_you_pre)
    q_you_post = np.array(q_you_post)
    q_expert_pre = np.array(q_expert_pre)
    q_expert_post = np.array(q_expert_post)
    q_mark = np.array(q_mark)
    return q_you_pre, q_you_post, q_expert_pre, q_expert_post, q_mark


def AggregateAnswersQuestionwise(data, num_you):
    answers_pre = []
    for col in ["q_you_pre_" + str(i) for i in range(1, num_you + 1)]:
        q_answers = np.array([x for x in data[col] if x != -998])
        answers_pre.append(q_answers)
    answers_post = []
    for col in ["q_you_post_" + str(i) for i in range(1, num_you + 1)]:
        q_answers = np.array([x for x in data[col] if x != -998])
        answers_post.append(q_answers)
    answers_expert_pre = []
    for col in ["q_expert_pre_" + str(i) for i in range(1, num_you + 1)]:
        q_answers = np.array([x for x in data[col] if x != -998])
        answers_expert_pre.append(q_answers)
    answers_expert_post = []
    for col in ["q_expert_post_" + str(i) for i in range(1, num_you + 1)]:
        q_answers = np.array([x for x in data[col] if x != -998])
        answers_expert_post.append(q_answers)
    return answers_pre, answers_post, answers_expert_pre, answers_expert_post
