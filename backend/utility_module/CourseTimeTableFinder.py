"""
    The CourseTimeTableFinder class is responsible for providing user
    the class time table features and number of spots available for that course
"""
from database.DataBaseManager import DataBaseManager


class CourseTimeTableFinder:
    def __init__(self, data_base_manager=DataBaseManager()):
        self.data_base_manager = data_base_manager

    def get_course_timetable(self, cid):
        """ Get the timetable of the course

        :param cid: course code of the course
        :type: str
        :return: location of the course
        :rtype: str
        """
        query = "SELECT * from coursetimetable where cid = %s"
        inputs = (cid, )
        result = self.data_base_manager.execute_query(query, inputs)
        return result


if __name__ == '__main__':
    course_time_finder = CourseTimeTableFinder()
    result = course_time_finder.get_course_timetable("COMP9101")
    print(result)
