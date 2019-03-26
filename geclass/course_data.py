import numpy as np
import scipy.stats


class CourseData:

    expert_responses = np.random.randint(low=-1, high=2, size=30)

    def __init__(self, course_id, test_data = None):
        # somehow get the data
        if test_data:
            data_1, data_2, data_3 = test_data
        self.geclass = self._compare_to_experts(data_1)
        self.mark_importance = self._reduce_likert_scale(data_2)
        self.meta = data_3

        self.mean = self.geclass.mean(axis=0)
        self.confidence = self._confidence()

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

    def _compare_to_experts(self, responses):
        reduced_responses = self._reduce_likert_scale(responses)
        expert_like = np.zeros(responses.shape, dtype=np.int8)
        for indx, student in enumerate(reduced_responses):
            expert_like[indx] = np.array(
                student == self.expert_responses, dtype=np.int8)
        return expert_like

    def _confidence(self, size=0.95):
        """Calculate the confidence interval for the data."""
        confidence = np.zeros((self.geclass.shape[1], 2))
        for indx, question in enumerate(self.geclass.transpose()):
            interval = scipy.stats.t.interval(
                size, question.shape[0]-1, loc=0,
                scale=scipy.stats.sem(question))
            confidence[indx] = np.abs(np.array(interval))
        return confidence



if __name__ == "__main__":
    data_1 = np.random.randint(low=1, high=6, size=(50, 30))
    data_2 = np.random.randint(low=1, high=6, size=(50, 10))
    data_3 = np.random.randint(low=1, high=6, size=(50, 5))
    course_data = CourseData(course_id=1, test_data=(data_1, data_2, data_3))
    print(course_data.mean, course_data.confidence)

