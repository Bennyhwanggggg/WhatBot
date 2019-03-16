from database.DataBaseManager import DataBaseManager
from conf.Error import ErrorMessages


class ResponseModule:
    def __init__(self):
        self.data_base_manager = DataBaseManager()
        self.query_map = {
            'course_outline': self.respond_to_course_outline_queries
        }

    def respond(self, message):
        if message['Intent'] not in self.query_map.keys():
            return ErrorMessages.UNKNOWN_QUERY_TYPE
        return self.query_map[message['Intent']](message)

    def respond_to_course_outline_queries(self, cid):
        response = self.data_base_manager.get_course_outline(cid)
        # TODO: format result
        return response


if __name__ == '__main__':
    response_module = ResponseModule()