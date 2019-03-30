from database.DataBaseManager import DataBaseManager


class WamCalculator:
    def __init__(self, courses):
        """Initialise the WamCalculator with list of dict of
        [{course_name: string, number_of_credits: int, score: float}]

        :param courses: list of courses with their score and number of credits as shown above
        :type list of dict
        """
        self.courses = courses
        self.data_base_manager = DataBaseManager()

    def calculate_wam(self):
        wam, total_credits = 0, 0
        result_string = ''
        for course in self.courses:
            course_name, num_of_credits, score = course['course_name'], course['number_of_credits'], course['score']
            result_string += 'Course name: {}\nNumber of credits: {}\nResult: {}\n'.format(course_name,
                                                                                           num_of_credits,
                                                                                           round(score, 1))
            wam += float(score)*int(num_of_credits)
            total_credits += int(num_of_credits)
        wam /= total_credits
        result_string += 'Wam is: {}\nGrade is: {}'.format(round(wam, 1), self.determine_grade(wam))
        print(result_string)
        return result_string

    def determine_grade(self, wam):
        wam = float(wam)
        if wam > 90:
            return 'HD'
        if wam > 75:
            return 'D'
        if wam > 65:
            return 'CR'
        if wam > 50:
            return 'P'
        return 'F'
