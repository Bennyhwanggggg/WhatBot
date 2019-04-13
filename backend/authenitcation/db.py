from database.DataBaseManager import DataBaseManager
from conf.Logger import Logger

"""
    Logger setup
"""
logger = Logger(__name__).log


class Authentication:
    def __init__(self):
        self.database_manager = DataBaseManager()

    def check_is_admin(self, username, password):
        query = "SELECT type FROM users WHERE username = %s AND password = %s"
        inputs = (username, password, )
        result = self.database_manager.execute_query(query, inputs)
        return True if len(result) == 1 and result[0][0] == 'admin' else False

    def check_is_student(self, username, password):
        query = "SELECT type FROM users WHERE username = %s AND password = %s"
        inputs = (username, password,)
        result = self.database_manager.execute_query(query, inputs)
        return True if len(result) == 1 and result[0][0] == 'student' else False
