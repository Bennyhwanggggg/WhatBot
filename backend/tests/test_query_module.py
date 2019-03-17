from query_module.QueryModule import QueryModule
import time

TIME_BETWEEN_API = 2


def test_query_module_clean_message():
    query_module = QueryModule()
    test_messages = ['COMP9900?',
                     'Comp9?900?',
                     'comp9900???',
                     'Comp9900??',
                     'COmp9900!!!!',
                     'Comp~!9+900?',
                     '>COMP9900?[<',
                     "comp9900's",
                     "comp9900's's",
                     "COMP9900''s"]
    for test_message in test_messages:
        result = query_module.clean_message(test_message)
        assert result.upper() == 'COMP9900'


def test_query_module_course_outline_queries():
    query_module = QueryModule()
    test_messages = ['What is the outline for COMP9900?',
                     'What is COMP9900 about?',
                     'What is COMP9900 about?',
                     'Tell me more about COMP9900',
                     'Give me the outline for comp9900',
                     'Course description for COMP9900 thanks',
                     'What can I learn in COMP9900?']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'course_outline_queries'
        assert result.message.upper() == 'COMP9900'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_query_module_send_outline_queries():
    query_module = QueryModule()
    test_messages = ['Can I have the outline for COMP9331?',
                     'Email me the outline for COMP9331',
                     'Send me the pdf outline for Comp9331',
                     "Send me comp9331's course outline pdf",
                     'Provide me the outline for COMP9331',
                     'Provide me the course outline for COMP9331 thanks',
                     'Provide me the course outline pdf for COMP9331 thanks']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'send_outline_queries'
        assert result.message.upper() == 'COMP9331'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_query_module_offering_term_queries():
    query_module = QueryModule()
    test_messages = ['When is COMP9101 offered?',
                     'When can I take COMP9101',
                     "What are COMP9101's offering term",
                     'Which semester can I take comp9101?',
                     'Which semester is comp9101 offered in',
                     'Can I take COMP9101 in semester 1?',
                     'When Can I enroll in COMP9101?']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'offering_term_queries'
        assert result.message.upper() == 'COMP9101'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


# def test_query_module_offering_term_queries():
