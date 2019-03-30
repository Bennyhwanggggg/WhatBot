from database.DataBaseManager import DataBaseManager
import pandas as pd

"""
    The ClassRoomFinder class is responsible for providing user
    the class room and tutorial locator feature.
"""

class ClassRoomFinder:
    def __init__(self, data_base_manager=DataBaseManager()):
        self.data_base_manager = data_base_manager

    def find_all_classroom(self):
        query = "SELECT * from classroom"
        result = self.data_base_manager.execute_query(query)
        df = pd.DataFrame(data = result, columns=['course', 'location'])
        df.to_csv('classRoom.csv')

    def find_class_room(self, cid):
        location = pd.read_csv('classRoom.csv')
        isCourse = location['course'] == cid
        result = location[isCourse].location.head().values
        if result:
            final = location[isCourse].location.head().values[0]
            return final
        else:
            return "No such course"


if __name__ == '__main__':
    data_base_manager = ClassRoomFinder()
    result = data_base_manager.find_class_room("COMP9900")
    #result = data_base_manager.find_all_classroom()
    #print(result)
