import numpy as np
import scipy.stats


class CoursePartData:

    def __init__(self, mean, confidence):
        self.mean = mean
        self.confidence = confidence


class CourseData:

    expert_responses = np.random.randint(low=-1, high=2, size=30)
    expert_importance = np.random.randint(low=-1, high=2, size=27)

    def __init__(self, course_id, test_data=None):
        # somehow get the data
        if test_data:
            data_you, data_expert, data_importance, data_meta = test_data
        self._you = self._compare_to_experts(data_you, self.expert_responses)
        self._expert = self._compare_to_experts(
            data_expert, self.expert_responses)
        self._importance = self._compare_to_experts(
            data_importance, self.expert_importance)
        self.meta_data = data_meta

        self.questions_you = CoursePartData(
            self._you.mean(axis=0), self._confidence(self._you))

        self.questions_expert = CoursePartData(
            self._expert.mean(axis=0), self._confidence(self._expert))

        self.questions_importance = CoursePartData(
            self._importance.mean(axis=0), self._confidence(self._importance))

    def _likert_reduction(self, response):
        if response in [1, 2]:
            return -1
        elif response == 3:
            return 0
        return 1

    def _reduce_likert_scale(self, responses):
        reduced = np.zeros(responses.shape)
        for indx_1, student in enumerate(responses):
            for indx_2, response in enumerate(student):
                reduced[indx_1][indx_2] = self._likert_reduction(response)
        return reduced

    def _compare_to_experts(self, responses, expert):
        reduced_responses = self._reduce_likert_scale(responses)
        expert_like = np.zeros(responses.shape, dtype=np.int8)
        for indx, student in enumerate(reduced_responses):
            expert_like[indx] = np.array(
                student == expert, dtype=np.int8)
        return expert_like

    def _confidence(self, data, size=0.95):
        """Calculate the confidence interval for the data."""
        confidence = np.zeros((data.shape[1], 2))
        for indx, question in enumerate(data.transpose()):
            interval = scipy.stats.t.interval(
                size, question.shape[0]-1, loc=0,
                scale=scipy.stats.sem(question))
            confidence[indx] = np.abs(np.array(interval))
        return confidence


if __name__ == "__main__":
    data_you = np.random.randint(low=1, high=6, size=(50, 30))
    data_expert = np.random.randint(low=1, high=6, size=(50, 30))
    data_importance = np.random.randint(low=1, high=6, size=(50, 27))
    data_meta = np.random.randint(low=1, high=6, size=(50, 5))
    course_data = CourseData(course_id=1, test_data=(
        data_you, data_expert, data_importance, data_meta))
    print(course_data.questions_you.mean, course_data.questions_you.confidence)
