from database.DataBaseManager import DataBaseManager
import pandas as pd

"""
    The ClassRoomFinder class is responsible for providing user
    the class room and tutorial locator feature.
"""

class ClassRoomFinder:
    def __init__(self, data_base_manager=DataBaseManager()):
        self.data_base_manager = data_base_manager
        self.data = None

    def get_all_classroom(self):
        query = "SELECT * from classroom"
        result = self.data_base_manager.execute_query(query)
        self.data = pd.DataFrame(data=result, columns=['course', 'location'])
        self.data.set_index('course', inplace=True)

    def find_class_room(self, cid):
        if self.data is None:
            self.get_all_classroom()
        return self.data.loc[cid].values[0] if cid in self.data.index else 'No information for the course queried'


if __name__ == '__main__':
    class_room_finder = ClassRoomFinder()
    class_room_finder.get_all_classroom()
    result = class_room_finder.find_class_room("COMP9900")
    print(result)
