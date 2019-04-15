"""
    The CourseTimeTableFinder class is responsible for providing user
    the class time table features and number of spots available for that course
"""
from database.DataBaseManager import DataBaseManager


class CourseTimeTableFinder:
    def __init__(self, database_manager=DataBaseManager()):
        self.database_manager = database_manager

    def get_course_timetable(self, cid):
        """ Get the timetable of the course

        :param cid: course code of the course
        :type: str
        :return: location of the course
        :rtype: str
        """
        query = "SELECT * from coursetimetable where cid = %s"
        inputs = (cid, )
        result = self.database_manager.execute_query(query, inputs)
        return result
