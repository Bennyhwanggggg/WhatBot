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
    assert result.intent == 'course_fee_queries_with_followup-user_input_course_code'
    assert result.message == 'COMP9900'


def test_course_fee_queries_followup_2():
    query_module = QueryModule()

    test_message = 'I want to know how much a course cost'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'course_outline_queries_with_followup'
    assert result.message == 'Sure! What is the course code of the course you want to know course fee for?'

    time.sleep(TIME_BETWEEN_API)

    test_message = 'COMP9321 please'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'course_fee_queries_with_followup-user_input_course_code'
    assert result.message == 'COMP9321'


def test_course_outline_queries_followup_1():
    query_module = QueryModule()

    test_message = 'I want to find out more about a course'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'course_outline_queries_with_followup'
    assert result.message == 'Of course! What is the course code of the course you want to know the outline for?'

    time.sleep(TIME_BETWEEN_API)

    test_message = 'I want to see COMP9444'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'course_outline_queries_with_followup-user_input_course_code'
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
    assert result.intent == 'course_outline_queries_with_followup-user_input_course_code'
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
    assert result.intent == 'indicative_hours_queries_with_followup-user_input_course_code'
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
    assert result.intent == 'offering_term_queries_with_followup-user_input_course_code'
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
    assert result.intent == 'prerequisites_queries_with_followup-user_input_course_code'
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
    assert result.intent == 'study_level_queries_with_followup-user_input_course_code'
    assert result.message == 'COMP9332'


def test_study_level_queries_followup_2():
    query_module = QueryModule()

    test_message = 'I want to know if a course is for undergrad'
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'study_level_queries_with_followup'
    assert result.message == 'Sure! What is the course code of the course you would like to find study level for?'

    time.sleep(TIME_BETWEEN_API)

    test_message = "COMP9323 please"
    result = query_module.detect_intent_texts(test_message)
    assert result.intent == 'study_level_queries_with_followup-user_input_course_code'
    assert result.message == 'COMP9323'