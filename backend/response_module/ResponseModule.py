from database.DataBaseManager import DataBaseManager
from conf.Error import QueryError


class ResponseModule:
    def __init__(self):
        self.data_base_manager = DataBaseManager()
        # query map contains list of queries that are offered in our Dialogflow agent.
        # The keys should match the intent names on Dialogflow
        self.query_map = {
            'course_outline_queries': self.respond_to_course_outline_queries,
            'course_fee_queries': self.respond_to_course_fee_queries,
            'course_location_queries': self.respond_to_course_location_queries,
            'indicative_hours_queries': self.respond_to_course_indicative_hours_queries,
            'offering_term_queries': self.respond_to_course_offering_term_queries,
            'prerequisites_queries': self.respond_to_course_prerequisites_queries,
            'school_and_faculty_queries': self.respond_to_course_school_and_faculty_queries,
            'send_outline_queries': self.respond_to_course_send_outline_queries,
            'study_level_queries': self.respond_to_course_study_level_queries
        }

    def respond(self, message):
        """ This function should be the entry point into ResponseModule.
        Messages from the query module is passed into here for information search
        and responses.

        :param message: message from Dialogflow
        :type dict
        :return: response
        :rtype str
        """
        if message.intent not in self.query_map.keys():
            return QueryError.UNKNOWN_QUERY_TYPE
        elif message.intent == 'Default Welcome Intent' or message.intent == 'Default Fallback Intent':
            return message.message
        return self.query_map[message.intent](message.message)

    def respond_to_course_outline_queries(self, cid):
        response = self.data_base_manager.get_course_outline(cid)
        # TODO: format result
        return response

    def respond_to_course_fee_queries(self, cid):
        pass

    def respond_to_course_location_queries(self, cid):
        pass

    def respond_to_course_indicative_hours_queries(self, cid):
        pass

    def respond_to_course_offering_term_queries(self, cid):
        pass

    def respond_to_course_prerequisites_queries(self, cid):
        pass

    def respond_to_course_school_and_faculty_queries(self, cid):
        pass

    def respond_to_course_send_outline_queries(self, cid):
        pass

    def respond_to_course_study_level_queries(self, cid):
        pass


if __name__ == '__main__':
    response_module = ResponseModule()