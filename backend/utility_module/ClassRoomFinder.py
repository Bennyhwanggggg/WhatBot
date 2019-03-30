from database.DataBaseManager import DataBaseManager
import pandas as pd

"""
    The ClassRoomFinder class is responsible for providing user
    the class room and tutorial locator feature.
"""

class ClassRoomFinder:
    def __init__(self, data_base_manager=DataBaseManager(), data='data'):
        self.data_base_manager = data_base_manager
        self.data = data

    def find_all_classroom(self):
        query = "SELECT * from classroom"
        result = self.data_base_manager.execute_query(query)
        df = pd.DataFrame(data = result, columns=['course', 'location'])
        self.data = df
        return df

    def find_class_room(self, cid):
        listLocation = self.data
        isCourse = listLocation['course'] == cid
        result = listLocation[isCourse].head().values
        if result.any():
            final = listLocation[isCourse].head().values[0][1]
            return final
        else:
            return "No such course"


if __name__ == '__main__':
    data_base_manager = ClassRoomFinder()
    #result = data_base_manager.find_all_classroom()
    #result = data_base_manager.find_class_room("COMP93")
