"""Containers to handle the responses to the questionnaire."""

import numpy as np

class Responses:
    """Responses of a single student as compared to the experts.

    1 is agreement, 0 is no agreement and -998 is no answer given.
    Inputs are in Likert-Scale (1 - 5), internally they are converted to
    agreement with experts (0 and 1).

    Args:
        q_you_pre (np.array): The answers to the you questions pre course.
        q_you_post (np.array): The answers to the you questions post course.
        q_expert_pre (np.array): The answers to the expert questions pre
            course.
        q_expert_post (np.array): The answers to the expert questions post
            course.
        q_mark (np.array): The answers to the mark questions post course.
        disagreement (bool): Determines if the Likert scale is redued to binary,
            i.e., 1 and 0 for agreement with experts or to 1, 0, -1 to include
            disagreement.

    Attributes:
        q_you_pre (np.array): Agreement with experts for q_you_pre.
        q_you_post (np.array): Agreement with experts for q_you_post.
        q_expert_pre (np.array): Agreement with experts for q_expert_pre.
        q_expert_post (np.array): Agreement with experts for q_expert_post.
        q_mark (np.array): Agreement with experts for q_mark.

    """
    experts = np.array([1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1,
                        -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1])
    experts_marks = np.array([1, -1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1,
                              1, -1, 1, 1, -1, 1, -1, -1])

    def __init__(self, q_you_pre, q_you_post, q_expert_pre, q_expert_post,
                 q_mark, disagreement=False):
        self.q_mark = self._compare_expert(q_mark, self.experts_marks, disagreement)
        self.q_you_pre = self._compare_expert(q_you_pre, self.experts, disagreement)
        self.q_you_post = self._compare_expert(q_you_post, self.experts, disagreement)
        self.q_expert_pre = self._compare_expert(q_expert_pre, self.experts, disagreement)
        self.q_expert_post = self._compare_expert(q_expert_post, self.experts, disagreement)

    def _likert_reduce(self, responses):
        """Reduce Likert from 5 to 3 levels."""
        translation = {1 : -1, 2: -1, 3: 0, 4: 1, 5: 1, -998: -998, -997: -998,
                       -999: -998}
        likert = np.vectorize(translation.get)(responses)
        return likert

    def _compare_expert(self, q_student, a_expert, disagreement):
        """Compare responses of students to experts."""
        compared = []
        q_student = self._likert_reduce(q_student)
        for response_student, response_experts in zip(q_student, a_expert):
            if response_student == -998:
                compared.append(-998)
            else:
                if disagreement:
                    compared.append(int(response_student * response_experts))
                else:
                    compared.append(int(response_student == response_experts))
        return np.array(compared)


class ResponseAggregate:
    """Aggregate of multiple students for one type of questions.

    The length of a ResponseAggregate is the number of valid answers
    (excluding answers not given). Access to one element returns a cut through
    all answers at the given position, excluding answers not given.

    Args:
        responses (list): List of one type of answers (q_mark, q_you_pre, ...).

    Attributes:
        responses (np.array): All the responses.

    >>> q_mark_1 = np.array([0, 1, -998, 1, 0])
    >>> q_mark_2 = np.array([1, -998, 0, 0, -998])
    >>> x = ResponseAggregate([q_mark_1, q_marks_2])
    >>> x[0]
    np.array([0, 1])
    >>> x[1]
    np.array([1])
    >>> len(x)
    7

    """
    def __init__(self, responses):
        self.responses = np.array(responses)

    def __getitem__(self, k):
        aggregate = []
        for response in self.responses:
            if response[k] != -998:
                aggregate.append(response[k])
        return np.array(aggregate)

    def __len__(self):
        count_invalid = (self.responses == -998).sum()
        return self.responses.size - count_invalid

    def size(self):
        """Return the total number of students."""
        return len(self.responses)


class QuestionnaireResponses:
    """Aggregate of all type of answers for multiple students.

    Args:
        responses (list): A list of Responses fro multiple students.

    Attributes:
        q_you_pre (ResponseAggregate): All answers for the q_you_pre questions.
        q_you_post (ResponseAggregate): All answers for the q_you_post
            questions.
        q_expert_pre (ResponseAggregate): All answers for the q_expert_pre
            questions.
        q_expert_post (ResponseAggregate): All answers for the q_expert_post
            questions.
        q_mark (ResponseAggregate): All answers for the q_mark questions.

    """
    def __init__(self, responses):
        self.q_mark = self._load_responses(responses, 'q_mark')
        self.q_you_pre = self._load_responses(responses, 'q_you_pre')
        self.q_you_post = self._load_responses(responses, 'q_you_post')
        self.q_expert_pre = self._load_responses(responses, 'q_expert_pre')
        self.q_expert_post = self._load_responses(responses, 'q_expert_post')

    def _load_responses(self, responses, attr):
        aggregate = []
        for response in responses:
            aggregate.append(getattr(response, attr))
        return ResponseAggregate(aggregate)

    def size(self):
        """Return the total number of students."""
        return len(self.q_mark.responses)

    def _append_responses(self, responses, attr):
        if getattr(self, attr).responses.size == 0:
            return np.copy(getattr(responses, attr).responses)
        if getattr(responses, attr).responses.size == 0:
            return getattr(self, attr).responses
        return np.append(getattr(self, attr).responses, getattr(responses, attr).responses, axis=0)

    def append(self, responses):
        """Append two QuestionnaireResponses to another."""
        self.q_mark.responses = self._append_responses(responses, 'q_mark')
        self.q_you_pre.responses = self._append_responses(responses, 'q_you_pre')
        self.q_you_post.responses = self._append_responses(responses, 'q_you_post')
        self.q_expert_pre.responses = self._append_responses(responses, 'q_expert_pre')
        self.q_expert_post.responses = self._append_responses(responses, 'q_expert_post')
