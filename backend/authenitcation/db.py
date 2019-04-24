"""
    This file contains the Authenticator class which is responsible
    for checking if a credential entered is correct or not and also
    give authority level to the user logging in.
"""

from database.DataBaseManager import DataBaseManager
from conf.Logger import Logger

"""
    Logger setup
"""
logger = Logger(__name__).log


class Authenticator:
    def __init__(self, database_manager=DataBaseManager()):
        """Initialise the Authenticator using the provided database instance

        :param database_manager: Database instance
        :type: DatabaseManager
        """
        self.database_manager = database_manager

    def check_is_admin(self, username, password):
        """Check if user is an admin or not by using an SQL query against the
        database with the given credentials

        :param username: username
        :type: str
        :param password: password
        :type: str
        :return: if user is admin or not
        :rtype: bool
        """
        query = "SELECT type FROM users WHERE username = %s AND password = %s"
        inputs = (username, password, )
        result = self.database_manager.execute_query(query, inputs)
        return True if len(result) == 1 and result[0][0] == 'admin' else False

    def check_is_student(self, username, password):
        """Check if user is an student or not by using an SQL query against the
        database with the given credentials

         :param username: username
         :type: str
         :param password: password
         :type: str
         :return: if user is student or not
         :rtype: bool
         """
        query = "SELECT type FROM users WHERE username = %s AND password = %s"
        inputs = (username, password, )
        result = self.database_manager.execute_query(query, inputs)
        return True if len(result) == 1 and result[0][0] == 'student' else False
