import numpy as np

class Responses:
    """Single response of one student as compared to expert.
    1 is agreement, 0 is no agreement and -998 is no answer given."""
    experts = np.array([1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1,
                        -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1])
    experts_marks = np.array([1, -1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1,
                              1, -1, 1, 1, -1, 1, -1, -1])

    def __init__(self, q_you_pre, q_you_post, q_expert_pre, q_expert_post,
                 q_mark):
        self.q_mark = self._compare_expert(q_mark, self.experts_marks)
        self.q_you_pre = self._compare_expert(q_you_pre, self.experts)
        self.q_you_post = self._compare_expert(q_you_post, self.experts)
        self.q_expert_pre = self._compare_expert(q_expert_pre, self.experts)
        self.q_expert_post = self._compare_expert(q_expert_post, self.experts)

    def _likert_reduce(self, responses):
        translation = {1 : -1, 2: -1, 3: 0, 4: 1, 5: 1, -998: -998, -997: -998,
                       -999: -998}
        likert = np.vectorize(translation.get)(responses)
        return likert

    def _compare_expert(self, q_student, a_expert):
        compared = []
        q_student = self._likert_reduce(q_student)
        for response_student, response_experts in zip(q_student, a_expert):
            if response_student == -998:
                compared.append(-998)
            else:
                compared.append(int(response_student == response_experts))
        return np.array(compared)


class ResponseAggregate:
    """Aggregate of multiple responses to one category, e.g. q_mark."""
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
        return len(self.responses)


class QuestionnaireResponses:
    """Aggregate of all responses."""
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
        return len(self.q_mark.responses)

    def _append_responses(self, responses, attr):
        if getattr(self, attr).responses.size == 0:
            return np.copy(getattr(responses, attr).responses)
        if getattr(responses, attr).responses.size == 0:
            return getattr(self, attr).responses
        return np.append(getattr(self, attr).responses, getattr(responses, attr).responses, axis=0)

    def append(self, responses):
        self.q_mark.responses = self._append_responses(responses, 'q_mark')
        self.q_you_pre.responses = self._append_responses(responses, 'q_you_pre')
        self.q_you_post.responses = self._append_responses(responses, 'q_you_post')
        self.q_expert_pre.responses = self._append_responses(responses, 'q_expert_pre')
        self.q_expert_post.responses = self._append_responses(responses, 'q_expert_post')
