from database.DataBaseManager import DataBaseManager
from utility_module.ConsultationManager import ConsultationManager
from conf.Error import QueryError
from conf.Response import FallbackResponse
from conf.Logger import Logger
import re

"""
    Logger setup
"""
logger = Logger(__name__).log


class ResponseModule:
    def __init__(self):
        """
            Initialize the Response module class which act as a search engine as well.
            It contains a data base connection and query_map is responsible for handling different types
            of data retrieval functions. The keys inside query_map have to match an intent name on Dialogflow.
        """
        self.data_base_manager = DataBaseManager()
        self.consultation_manager = ConsultationManager()
        self.query_map = {
            'all_courses_queries': self.respond_to_all_course,
            'course_outline_queries': self.respond_to_course_outline_queries,
            'course_outline_queries_with_followup-user_input_course_code': self.respond_to_course_outline_queries,
            'course_fee_queries': self.respond_to_course_fee_queries,
            'course_fee_queries_with_followup-user_input_course_code': self.respond_to_course_fee_queries,
            'course_location_queries': self.respond_to_course_location_queries,
            'course_location_queries_with_followup-user_input_course_code': self.respond_to_course_location_queries,
            'indicative_hours_queries': self.respond_to_course_indicative_hours_queries,
            'indicative_hours_queries_with_followup-user_input_course_code': self.respond_to_course_indicative_hours_queries,
            'offering_term_queries': self.respond_to_course_offering_term_queries,
            'offering_term_queries_with_followup-user_input_course_code': self.respond_to_course_offering_term_queries,
            'prerequisites_queries': self.respond_to_course_prerequisites_queries,
            'prerequisites_queries_with_followup-user_input_course_code': self.respond_to_course_prerequisites_queries,
            'school_and_faculty_queries': self.respond_to_course_school_and_faculty_queries,
            'school_and_faculty_queries_with_followup-user_input_course_code': self.respond_to_course_school_and_faculty_queries,
            'send_outline_queries': self.respond_to_course_send_outline_queries,
            'send_outline_queries_with_followup-user_input_course_code': self.respond_to_course_send_outline_queries,
            'study_level_queries': self.respond_to_course_study_level_queries,
            'study_level_queries_with_followup-user_input_course_code': self.respond_to_course_study_level_queries,
            'consultation_booking': self.respond_to_course_consultation_booking,
            'consultation_booking_with_followup-user_input_course_code_with_followup-user_input_time_and_date': self.respond_to_course_consultation_booking,
            'consultation_booking_with_followup-user_input_time_and_date_with_followup-user_input_course_code': self.respond_to_course_consultation_booking,
            'consultation_cancel': self.respond_to_course_consultation_cancel,
            'wam_admin_queries': self.respond_to_wam_admin_queries,
            'wam_student_queries': self.respond_to_wam_student_queries,
            'is_adk_queries': self.respond_to_course_isadk_queries
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
        logger.info('Response module recieved:\n\tIntent: {}\n\tFullfillment text: {}'.format(message.intent, message.message))
        if message.intent == 'Default Welcome Intent' or \
            message.intent == 'Default Fallback Intent' or \
            message.intent.endswith('followup') or \
            isinstance(message, FallbackResponse):
            return message.message
        elif message.intent not in self.query_map.keys():
            return QueryError.UNKNOWN_QUERY_TYPE.value
        return self.query_map[message.intent](message.message)

    def respond_to_course_outline_queries(self, cid):
            response = self.data_base_manager.get_course_outline(cid)
            if not response:
                return "Sorry, there is no such course"
            return response[0][0]

    def respond_to_course_fee_queries(self, cid):
            response = self.data_base_manager.get_tuition_fee(cid)
            if not response:
                return "Sorry, there is no such course"
            return "commonwealth student: {}\ndomestic student: {}\ninternational student: {}".format(response[0][0], response[0][1], response[0][2])

    def respond_to_course_location_queries(self, cid):
        response = self.data_base_manager.get_location(cid)
        if not response:
            return "Sorry, there is no such course"
        return response[0][0]

    def respond_to_course_indicative_hours_queries(self, cid):
        response = self.data_base_manager.get_indicative_hours(cid)
        if not response:
            return "Sorry, there is no such course"
        return response[0][0]

    def respond_to_course_offering_term_queries(self, cid):
        response = self.data_base_manager.get_offer_term(cid)
        if not response:
            return "Sorry, there is no such course"
        return response[0][0]

    def respond_to_course_prerequisites_queries(self, cid):
        response = self.data_base_manager.get_prerequisites(cid)
        if not response:
            return "Sorry, there is no such course"
        if not response[0][0]:
            return "There is no prerequisite for this course, it is 0 level"
        return response[0][0]

    def respond_to_course_school_and_faculty_queries(self, cid):  # TODO: finish
        response = self.data_base_manager.get_faculty(cid)
        if not response:
            return "Sorry, there is no such course"
        return "The detail for faculty: {}".format(response[0][0])

    def respond_to_course_send_outline_queries(self, cid):
        response = self.data_base_manager.get_pdf_url(cid)
        if not response:
            return "Sorry, there is no such course"
        return response[0][0]

    def respond_to_course_study_level_queries(self, cid):
        pass  # TODO: finish, if not in database, we say no

    def respond_to_course_isadk_queries(self, cid):
        response = self.data_base_manager.get_course(cid)
        if not response:
            return "Sorry, there is no such course"
        answer = "Yes, it is an ADK course" if response[0][3] else "Sorry, it is not an ADK"
        return answer

    def respond_to_course_consultation_booking(self,cid, sid, time, date):
        response = self.consultation_manager.consultation_booking_query(cid, sid, time, date)
        return response

    def respond_to_course_consultation_cancel(self, cid, sid, time, date):
        response = self.consultation_manager.delete_consultation(cid, sid, time, date)
        return "{}, you have relase the time slot at {} on {}".format(response, time, date)

    def respond_to_all_course(self, _):
        response = self.data_base_manager.get_all_courses()
        courses = [result[0] for result in response]
        return 'The list of courses is:\n{}'.format('\n'.join(courses))

    def respond_to_wam_admin_queries(self):
        pass  # TODO:

    def respond_to_wam_student_queries(self):
        pass  # TODO:
