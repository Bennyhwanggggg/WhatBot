from database.DataBaseManager import DataBaseManager

"""
    This class is responsible for the lecturer announcements feature
    so students can see the latest announcements from LiC
"""


class AnnouncementsGetter:
    def __init__(self, database_manager=DataBaseManager()):
        self.database_manager = database_manager

    def delete_announcement(self, cid):
        query = "DELETE FROM announcement WHERE cid = %s"
        inputs = (cid, )
        return self.database_manager.execute_query(query, inputs)

    def add_announcement(self, cid, c_name, content, date):
        """Update the announcement of a course for a student in the databse

        :param cid: course code
        :type: str
        :param content: anncouncement
        :type: str
        :param date: the date of published anncouncement
        :type: var
        :return: database operation result
        :rtype: str
        """
        query = "INSERT INTO announcement(cid, c_name, content, date) VALUES (%s, %s, %s, %s)"
        inputs = (cid, c_name, content, date, )
        return self.database_manager.execute_query(query, inputs)

    def get_announcement(self, cid):
        query = "SELECT * from announcement where cid = %s"
        inputs = (cid, )
        result = self.database_manager.execute_query(query, inputs)
        if result:
            announcement = "Announcement for {} ({}): {}".format(result[0][0], result[0][3], result[0][2])
        else:
            announcement = "No announcement for this {}".format(cid)
        return announcement
