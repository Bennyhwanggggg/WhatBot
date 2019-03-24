from query_module.QueryModule import QueryModule
import time

TIME_BETWEEN_API = 1.5


def test_course_fee_queries_followup_1():
    query_module = QueryModule()

    test_message = 'I want to find out the course fee for a course'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'course_fee_queries_with_followup'
    assert result.message == 'Sure! What is the course code of the course you want to know course fee for?'

    time.sleep(TIME_BETWEEN_API)

    test_message = 'COMP9900 thanks'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'course_fee_queries_with_followup-user_input_course_code' or 'course_fee_queries'
    assert result.message == 'COMP9900'


def test_course_fee_queries_followup_2():
    query_module = QueryModule()

    test_message = 'I want to know how much a course cost'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'course_fee_queries_with_followup'
    assert result.message == 'Sure! What is the course code of the course you want to know course fee for?'

    time.sleep(TIME_BETWEEN_API)

    test_message = 'COMP9321 please'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'course_fee_queries_with_followup-user_input_course_code' or 'course_fee_queries'
    assert result.message == 'COMP9321'


def test_course_outline_queries_followup_1():
    query_module = QueryModule()

    test_message = 'I want to find out more about a course'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'course_outline_queries_with_followup'
    assert result.message == 'Of course! What is the course code of the course you want to know the outline for?'

    time.sleep(TIME_BETWEEN_API)

    test_message = "COMP9444's outline please"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'course_outline_queries_with_followup-user_input_course_code' or 'course_outline_queries'
    assert result.message == 'COMP9444'


def test_course_outline_queries_followup_2():
    query_module = QueryModule()

    test_message = 'Show me the course description for a course'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'course_outline_queries_with_followup'
    assert result.message == 'Of course! What is the course code of the course you want to know the outline for?'

    time.sleep(TIME_BETWEEN_API)

    test_message = 'Show me COMP9415 thanks'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'course_outline_queries_with_followup-user_input_course_code' or 'course_outline_queries'
    assert result.message == 'COMP9415'


def test_indicative_hours_queries_followup():
    query_module = QueryModule()

    test_message = 'I want to find the workload for a course'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'indicative_hours_queries_with_followup'
    assert result.message == 'Of course! What is the course code of the course you want to know the indicative hours for?'

    time.sleep(TIME_BETWEEN_API)

    test_message = 'COMP9517'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'indicative_hours_queries_with_followup-user_input_course_code' or 'indicative_hours_queries'
    assert result.message == 'COMP9517'


def test_offering_term_queries_followup():
    query_module = QueryModule()

    test_message = 'I want to know when I can take a course'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'offering_term_queries_with_followup'
    assert result.message == 'Of course! What is the course code of the course you want to know the offering terms for?'

    time.sleep(TIME_BETWEEN_API)

    test_message = 'COMP9318'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'offering_term_queries_with_followup-user_input_course_code' or 'offering_term_queries'
    assert result.message == 'COMP9318'


def test_prerequisites_queries_followup():
    query_module = QueryModule()

    test_message = 'I want to see the requirements for a course'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'prerequisites_queries_with_followup'
    assert result.message == 'Sure! Please tell me the course code of the course you want to find out prerequisites for.'

    time.sleep(TIME_BETWEEN_API)

    test_message = "COMP9331's requirements thanks"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'prerequisites_queries_with_followup-user_input_course_code' or 'prerequisites_queries'
    assert result.message == 'COMP9331'


def test_study_level_queries_followup_1():
    query_module = QueryModule()

    test_message = 'I want to know if a course is for postgrad'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'study_level_queries_with_followup'
    assert result.message == 'Sure! What is the course code of the course you would like to find study level for?'

    time.sleep(TIME_BETWEEN_API)

    test_message = "COMP9322"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'study_level_queries_with_followup-user_input_course_code' or 'study_level_queries'
    assert result.message == 'COMP9322'


def test_study_level_queries_followup_2():
    query_module = QueryModule()

    test_message = 'I want to know if a course is for undergrad'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'study_level_queries_with_followup'
    assert result.message == 'Sure! What is the course code of the course you would like to find study level for?'

    time.sleep(TIME_BETWEEN_API)

    test_message = "COMP9323 please"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'study_level_queries_with_followup-user_input_course_code' or 'study_level_queries'
    assert result.message == 'COMP9323'


def test_consultation_booking_user_input_course_code_first_followup_1():
    query_module = QueryModule()

    test_message = 'I want to book a course consultation'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'consultation_booking_with_followup'
    assert result.message == 'Sure! What is the course code of the course you would like to book it for? Also, what time and date?'

    time.sleep(TIME_BETWEEN_API)

    test_message = "COMP9334 please"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'consultation_booking_with_followup-user_input_course_code_with_followup'
    assert result.message == 'Sure! Please tell me which date and time you would like to book a course consultation for COMP9334.'

    time.sleep(TIME_BETWEEN_API)

    test_message = "3pm on 2/11/2019 thanks"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'consultation_booking_with_followup-user_input_course_code_with_followup-user_input_time_and_date'
    assert result.message == 'COMP9334 @@@ 15:00:00 @@@ 2019-11-02'


def test_consultation_booking_user_input_course_code_first_followup_2():
    query_module = QueryModule()

    test_message = 'Book a course consultation'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'consultation_booking_with_followup'
    assert result.message == 'Sure! What is the course code of the course you would like to book it for? Also, what time and date?'

    time.sleep(TIME_BETWEEN_API)

    test_message = "COMP9101"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'consultation_booking_with_followup-user_input_course_code_with_followup'
    assert result.message == 'Sure! Please tell me which date and time you would like to book a course consultation for COMP9101.'

    time.sleep(TIME_BETWEEN_API)

    test_message = "3:30pm on 2/11/2019"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'consultation_booking_with_followup-user_input_course_code_with_followup-user_input_time_and_date'
    assert result.message == 'COMP9101 @@@ 15:30:00 @@@ 2019-11-02'


def test_consultation_booking_user_input_time_date_first_followup_1():
    query_module = QueryModule()

    test_message = 'Book a consultation'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'consultation_booking_with_followup'
    assert result.message == 'Sure! What is the course code of the course you would like to book it for? Also, what time and date?'

    time.sleep(TIME_BETWEEN_API)

    test_message = "Book for 10:15 on 2/3/2019"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'consultation_booking_with_followup-user_input_time_and_date_with_followup'
    assert result.message == 'Sure! Please tell me the course code of the course you want to book consultation for?'

    test_message = "COMP6774"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'consultation_booking_with_followup-user_input_time_and_date_with_followup-user_input_course_code'
    assert result.message == 'COMP6774 @@@ 10:15:00 @@@ 2019-03-02'


def test_consultation_booking_user_input_time_date_first_followup_2():
    query_module = QueryModule()

    test_message = 'Please book a course consultation for me'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'consultation_booking_with_followup'
    assert result.message == 'Sure! What is the course code of the course you would like to book it for? Also, what time and date?'

    time.sleep(TIME_BETWEEN_API)

    test_message = "Make a booking at 11am on 04/09/19"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'consultation_booking_with_followup-user_input_time_and_date_with_followup'
    assert result.message == 'Sure! Please tell me the course code of the course you want to book consultation for?'

    test_message = "COMP9020"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'consultation_booking_with_followup-user_input_time_and_date_with_followup-user_input_course_code'
    assert result.message == 'COMP9020 @@@ 11:00:00 @@@ 2019-09-04'
