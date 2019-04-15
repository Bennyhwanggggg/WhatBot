from response_module.ResponseModule import ResponseModule
from conf.Response import IntentResponse


def test_respond_to_course_outline():
    response_module = ResponseModule()
    course = "comp9900"
    message = IntentResponse(intent='course_outline_queries', confidence=1, message=course)
    course_outline = response_module.respond_to_course_outline_queries(message)
    assert course_outline == "A capstone software project. Students work in teams to define, implement and evaluate a real-world software system. Most of the work in this course is team-based project work, although there are some introductory lectures on software project management and teamwork strategies. Project teams meet fortnightly with project mentors to report on the progress of the project. Assessment is based on a project proposal, a final project demonstration and report, and on the quality of the software system itself. Students are also required to reflect on their work and to provide peer assessment of their team-mates' contributions to the project."


def test_respond_to_course_indicative_hours():
    response_module = ResponseModule()
    course = "comp9900"
    message = IntentResponse(intent='course_indicative_hours_queries', confidence=1, message=course)
    indicative_hours = response_module.respond_to_course_indicative_hours_queries(message)
    assert indicative_hours == "10"


def test_respond_to_course_fee():
    response_module = ResponseModule()
    course = "comp9900"
    message = IntentResponse(intent='course_fee_queries', confidence=1, message=course)
    course_fee = response_module.respond_to_course_fee_queries(message)
    assert course_fee == "Commonwealth student: $1170\nDomestic student: $4350\nInternational student: $5730"


def test_respond_to_course_isadk():
    response_module = ResponseModule()
    course = "comp9900"
    message = IntentResponse(intent='is_adk_queries', confidence=1, message=course)
    course_isadk = response_module.respond_to_course_isadk_queries(message)
    assert course_isadk == "Yes, it is an ADK course"


def test_respond_to_course_offering_term():
    response_module = ResponseModule()
    course = "comp9900"
    message = IntentResponse(intent='offering_term_queries', confidence=1, message=course)
    course_offering_term = response_module.respond_to_course_offering_term_queries(message)
    assert course_offering_term == "Term 1, Term 2, Term 3"


def test_respond_to_course_send_outline():
    response_module = ResponseModule()
    course = "comp9900"
    message = IntentResponse(intent='send_outline_queries', confidence=1, message=course)
    course_send_outline = response_module.respond_to_course_send_outline_queries(message)
    assert course_send_outline == "https://itq9q5ny14.execute-api.ap-southeast-2.amazonaws.com/prod/pdf?url=https://www.handbook.unsw.edu.au/postgraduate/courses/2019/COMP9900/"


def test_respond_to_course_school_and_faculty():
    response_module = ResponseModule()
    course = "comp9900"
    message = IntentResponse(intent='school_and_faculty_queries', confidence=1, message=course)
    course_school_and_faculty = response_module.respond_to_course_school_and_faculty_queries(message)
    assert "Faculty of Engineering" in course_school_and_faculty


def test_respond_to_course_location():
    response_module = ResponseModule()
    course = "comp9900"
    message = IntentResponse(intent='course_location_queries', confidence=1, message=course)
    course_location = response_module.respond_to_course_location_queries(message)
    assert course_location == "Kensington"


def test_respond_to_course_prerequisites():
    response_module = ResponseModule()
    course = "comp9900"
    message = IntentResponse(intent='prerequisites_queries', confidence=1, message=course)
    course_prerequisites = response_module.respond_to_course_prerequisites_queries(message)
    assert course_prerequisites == "Prerequisite: Completion of at least 72 UOC towards MIT program 8543.  Students must be in their final semester of study."
