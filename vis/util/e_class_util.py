import util
from util.static_variables import QUESTION_TRANSPOSITION, MARK_TRANSPOSITION


def PrepareMatchedData(df_pre, df_post, df_cis, num_you, num_mark):
    df_post.dropna(subset=["ResponseId"], inplace=True)
    df_pre.dropna(subset=["ResponseId"], inplace=True)
    matched = df_pre.merge(df_post, on=["anon_student_id", "ResponseId"],
                           suffixes=["_pre", "_post"])
    matched.fillna(-998, inplace=True)
    matched.drop(["q40a_pre", "q40b_pre"], axis=1, inplace=True)
    matched = matched[
            (matched["Q47"] == 1) |
            (matched["Q47"] == 6)
    ]
    columns = {}
    for key_e, key_ge in QUESTION_TRANSPOSITION.items():
        columns["q{:02d}a_pre".format(key_e)] = "q_you_pre_{}".format(key_ge)
        columns["q{:02d}b_pre".format(key_e)] = "q_expert_pre_{}".format(key_ge)
        columns["q{:02d}a_post".format(key_e)] = "q_you_post_{}".format(key_ge)
        columns["q{:02d}b_post".format(key_e)] = "q_expert_post_{}".format(key_ge)

    for key_e, key_ge in MARK_TRANSPOSITION.items():
        columns["q{:02d}c".format(key_e)] = "q_mark_{}".format(key_ge)

    matched.rename(columns=columns, inplace=True)

    # E-CLASS mark questions are not reduced
    for i in range(1, num_mark + 1):
        matched["q_mark_{}".format(i)].replace({2: 1, 4: 5}, inplace=True)

    disagreement = matched.replace({1: -1, 3: 0, 5: 1})
    binary = disagreement.replace(-1, 0)
    compact = util.Compactify(binary, num_you, num_mark)
    disagreement_compact = util.Compactify(disagreement, num_you, num_mark)
    return disagreement, binary, compact, disagreement_compact
