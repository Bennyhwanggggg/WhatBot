from database.DataBaseManager import DataBaseManager
from conf.Error import QueryError
from conf.Response import FallbackResponse
from response_module.ResponseModule import ResponseModule




if __name__ == '__main__':
    response_module = ResponseModule()
    data_base_manager = DataBaseManager()
    course = "comp9900"
    s1 = response_module.respond_to_course_outline_queries(course)
    s2 = response_module.respond_to_course_indicative_hours_queries(course)
    s3 = response_module.respond_to_course_fee_queries(course)
    s4 = response_module.respond_to_course_isadk_queries(course)
    s5 = response_module.respond_to_course_offering_term_queries(course)
    s6 = response_module.respond_to_course_send_outline_queries(course)
    s7 = response_module.respond_to_course_school_and_faculty_queries(course)
    s8 = response_module.respond_to_course_location_queries(course)
    s9 = response_module.respond_to_course_prerequisites_queries(course)
    a = [s1,s2,s3,s4,s5,s6,s7,s8,s9]
    for e in a:
        print("s: ",e)
        print('\n')