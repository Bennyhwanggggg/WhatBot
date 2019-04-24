"""
    The ClassRoomFinder class is responsible for providing user
    the lecture room locator feature for their courses.
"""
from database.DataBaseManager import DataBaseManager
import pandas as pd


class ClassRoomFinder:
    def __init__(self, database_manager=DataBaseManager()):
        """Instantiate the class with a database instance

        :param database_manager: database instance
        :type: DataBaseManger
        """
        self.database_manager = database_manager
        self.data = None

    def get_all_classroom(self):
        """Get all class room location data and set it into memory as
        they do not change often

        :return: None
        """
        query = "SELECT * from classroom"
        result = self.database_manager.execute_query(query)
        self.data = pd.DataFrame(data=result, columns=['course', 'location'])
        self.data.set_index('course', inplace=True)

    def find_class_room(self, cid):
        """ Get the classroom of the course

        :param cid: course code of the course
        :type: str
        :return: location of the course
        :rtype: str
        """
        if self.data is None:
            self.get_all_classroom()
        cid = cid.upper()
        return self.data.loc[cid].values[0] if cid in self.data.index else 'No information for the course queried'
