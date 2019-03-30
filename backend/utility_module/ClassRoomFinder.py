from database.DataBaseManager import DataBaseManager

"""
    The ClassRoomFinder class is responsible for providing user
    the class room and tutorial locator feature.
"""


class ClassRoomFinder:
    def __init__(self, data_base_manager=DataBaseManager()):
        self.data_base_manager = data_base_manager

    def find_class_room(self, cid):
        query = "SELECT * from classroom where cid like %s"
        inputs = (cid, )
        return self.data_base_manager.execute_query(query, inputs)


if __name__ == '__main__':
    data_base_manager = ClassRoomFinder()
    result = data_base_manager.find_class_room("COMP990")
