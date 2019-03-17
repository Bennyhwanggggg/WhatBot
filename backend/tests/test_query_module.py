from query_module.QueryModule import QueryModule
import time


def test_query_module_clean_message():
    query_module = QueryModule()
    test_messages = ['COMP9900?',
                     'Comp9?900?',
                     'comp9900???',
                     'Comp9900??',
                     'COmp9900!!!!',
                     'Comp~!9+900?',
                     '>COMP9900?[<']
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
        time.sleep(3)  # set gap so Google API doesn't get overloaded


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
        time.sleep(3)  # set gap so Google API doesn't get overloaded


