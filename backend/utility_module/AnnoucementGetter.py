from database.DataBaseManager import DataBaseManager

"""
    This class is responsible for the lecturer announcements feature
    so students can see the latest announcements from LiC
"""

class AnnouncementsGetter:
    def __init__(self, ):
        self.data_base_manager = DataBaseManager()
        #self.announcements = announcements

    def delete_anncouncement(self, cid):
        query = "DELETE FROM announcement WHERE cid = %s"
        inputs = (cid, )
        return self.data_base_manager.execute_query(query, inputs)

    def add_anncounement(self, cid, c_name, content, date):
        """Update the anncouncement of a course for a student in the databse

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
        return self.data_base_manager.execute_query(query, inputs)

    def get_anncounement(self, cid):
        query = "SELECT * from announcement where cid = %s"
        inputs = (cid, )
        result = self.data_base_manager.execute_query(query, inputs)
        announcment = "No Annoucement for this {}".format(cid)
        announcment = "Anncouncement for {} ({}): {}".format(result[0][0], result[0][3], result[0][2]) if result else announcment
        return announcment



if __name__ == '__main__':
    anncouncement_finder = AnnouncementsGetter()
    #result = anncouncement_finder.add_anncounement("COMP9101", "Design & Analysis of Algorithms", "Please do come for tomorrow's class", "2019-04-02")
    #result = anncouncement_finder.delete_anncouncement("COMP914")
    result = anncouncement_finder.get_anncounement("COMP9020")
    print(result)
