"""
    This file contains the Wam Calculator which is responsible for WAM related operations.
"""
from database.DataBaseManager import DataBaseManager
from conf.Logger import Logger
from conf.Error import QueryError
import pandas as pd

"""
    Logger setup
"""
logger = Logger(__name__).log


class WamCalculator:
    def __init__(self, database_manager=DataBaseManager()):
        """Initialise the WamCalculator with list of dict of
        [{course_name: string, number_of_credits: int, score: float}]

        :param courses: list of courses with their score and number of credits as shown above
        :type list of dict
        """
        self.database_manager = database_manager

    def add_mark(self, sid, cid, mark, credit):
        """Update the mark of a course for a student in the databse

        :param sid: student ID
        :type: str
        :param cid: course code
        :type: str
        :param mark: result of that course
        :type: float
        :param credit: number of credit for that course
        :type: int
        :return: database operation result
        :rtype: str
        """
        sid, cid = sid.lower(), cid.lower()
        query = "INSERT INTO wam(sid, cid, mark, credit) VALUES (%s, %s, %s, %s)"
        inputs = (sid, cid, mark, credit, )
        return self.database_manager.execute_query(query, inputs)

    def delete_sid(self, sid):
        sid = sid.lower()
        query = "DELETE FROM wam WHERE sid = %s"
        inputs = (sid, )
        return self.database_manager.execute_query(query, inputs)

    def get_student_wam(self, sid):
        sid = sid.lower()
        query = "SELECT * from wam where sid = %s"
        inputs = (sid, )
        result = self.database_manager.execute_query(query, inputs)
        df = pd.DataFrame(data=result, columns=['sid', 'cid', 'mark', 'credit'])
        return df

    def calculate_wam(self, sid):
        """Calculate wam using the preloaded data from self.courses and
        give a result string which is a summary of their course results and
        final calculated WAM

        :return: result summary string
        :rtype: str
        """
        sid = sid.lower()
        data = self.get_student_wam(sid)
        if data.empty:
            return QueryError.NO_STUDENT.value
        logger.debug(data)
        wam, total_credits = 0, 0
        result_string = ''
        for index, row in data.iterrows():
            course_name, num_of_credits, mark = row['cid'], row['credit'], row['mark']
            result_string += 'Course name: {}\nNumber of credits: {}\nResult: {}\n'.format(course_name,
                                                                                           num_of_credits,
                                                                                           round(float(mark), 1))
            wam += float(row['mark'])*int(row['credit'])
            total_credits += int(row['credit'])
        wam /= total_credits
        result_string += 'Wam is: {}\nGrade is: {}'.format(round(wam, 1), self.determine_grade(wam))
        logger.debug(result_string)
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
