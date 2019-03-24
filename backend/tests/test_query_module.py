from query_module.QueryModule import QueryModule
import time

TIME_BETWEEN_API = 1.5


def test_clean_message():
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


def test_course_outline_queries():
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


def test_send_outline_queries():
    query_module = QueryModule()
    test_messages = ['Email me the outline for COMP9331',
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


def test_offering_term_queries():
    query_module = QueryModule()
    test_messages = ['When is COMP9101 offered?',
                     'When can I take COMP9101',
                     "What are COMP9101's offering term",
                     'Which semester can I take comp9101?',
                     'Which semester is comp9101 offered in',
                     'Can I take COMP9101 in semester 1?',
                     'When can I enroll in COMP9101?']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'offering_term_queries'
        assert result.message.upper() == 'COMP9101'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_course_location_queries():
    query_module = QueryModule()
    test_messages = ['Where is COMP9321?',
                     'Where is COMP9321 at?',
                     "COMP9321's campus?",
                     'Where is COMP9321 offered?',
                     'Which campus is COMP9321 going to be in?',
                     'Where to go for COMP9321',
                     'Campus for COMP9321?']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'course_location_queries'
        assert result.message.upper() == 'COMP9321'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_course_fee_queries():
    query_module = QueryModule()
    test_messages = ['How much is COMP9318?',
                     'Cost of COMP9318??',
                     "COMP9318's cost?",
                     "How much is COMP9318's course fee?",
                     'How much do I need to pay for COMP9318',
                     'The cost of COMP9318???',
                     'Course fee for COMP9318 thanks']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'course_fee_queries'
        assert result.message.upper() == 'COMP9318'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_consultation_booking_command_1():
    query_module = QueryModule()
    test_messages = ['Show me the available time slot on 06/09/19 18:13 for COMP9334',
                     'May I book the time slot starts from 06/09/19 18:13 for COMP9334?',
                     'May I book the time slot starts from 18:13 on 06/09/19 for COMP9334?',
                     'Show me the available time slot on 06/09/19 at 18:13 for COMP9334',
                     'Reserve the time slot starts from 06/09/19 18:13 for COMP9334',
                     'Book a consultation for COMP9334 on 06/09/19 at 18:13',
                     'Make consultation booking for COMP9334 on 06/09/19 at 18:13',
                     'Make a consultation booking on 06/09/19 at 18:13 for COMP9334',
                     'Make a consultation booking for COMP9334 on 06/09/19 at 18:13',
                     'May I book the time slot starts from 06/09/2019 18:13 for COMP9334?',
                     'Book an consultation for COMP9334 on 06/09/2019 at 18:13',
                     'May I book a consultation for COMP9334 at 06/09/2019 18:13',
                     'May I book consultation for COMP9334 from 06/09/2019 18:13',
                     'May I book a consultation for COMP9334 on 06/09/2019 at 18:13',
                     'Reserve course consultation for COmp9334 on 06/09/2019 at 18:13']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'consultation_booking'
        assert result.message.upper() == 'COMP9334 @@@ 18:13:00 @@@ 2019-09-06'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_consultation_booking_command_2():
    query_module = QueryModule()
    test_messages = ['May I book the a course consultation on 11/11/19 06:13 for COMP9334?',
                     'May I book the time slot starts from 11/11/19 06:13 for COMP9334?',
                     'May I book the time slot starts from 06:13 on 11/11/19 for COMP9334?',
                     'Show me the available time slot on 11/11/2019 at 06:13 for COMP9334',
                     'Reserve the time slot starts from 2019/11/11 6:13 for COMP9334',
                     'Book a consultation for COMP9334 on 11/11/2019 at 6:13',
                     'Make a consultation booking for COMP9334 on 11/11/19 at 6:13',
                     'Make a consultation booking on 2019/11/11 at 6:13 for COMP9334',
                     'Make consultation booking for COMP9334 on 11/11/19 at 6:13',
                     'May I book the time slot starts from 11/11/2019 6:13 for COMP9334?',
                     'Book an consultation for COMP9334 on 11/11/2019 at 6:13',
                     'May I book a consultation for COMP9334 at 11/11/2019 6:13',
                     'May I book a consultation for COMP9334 from 11/11/2019 6:13',
                     'May I book consultation for COMP9334 on 2019/11/11 at 6:13',
                     'Reserve a course consultation for COmp9334 on 11/11/2019 at 6:13']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'consultation_booking'
        assert result.message.upper() == 'COMP9334 @@@ 06:13:00 @@@ 2019-11-11'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_consultation_booking_command_3():
    query_module = QueryModule()
    test_messages = ['I want to book a course consultation on 1/11/19 at 06:13 for COMP9334?',
                     'May I book the time slot starts from 1/11/19 06:13 for COMP9334?',
                     'May I book the time slot starts from 06:13 on 1/11/19 for COMP9334?',
                     'Show me the available time slot on 1/11/2019 at 06:13 for COMP9334',
                     'Reserve the time slot starts from 2019/11/1 6:13 for COMP9334',
                     'Book consultation for COMP9334 on 1/11/2019 at 6:13',
                     'Make a consultation booking for COMP9334 on 1/11/19 at 6:13',
                     'Make a consultation booking on 2019/11/1 at 6:13 for COMP9334',
                     'Make consultation booking for COMP9334 on 1/11/19 at 6:13',
                     'May I book the time slot starts from 1/11/2019 6:13 for COMP9334?',
                     'Book an consultation for COMP9334 on 1/11/2019 at 6:13',
                     'May I book a consultation for COMP9334 at 1/11/2019 6:13',
                     'May I book consultation for COMP9334 from 1/11/2019 6:13',
                     'May I book a consultation for COMP9334 on 2019/11/1 at 6:13',
                     'Reserve a course consultation for COmp9334 on 1/11/2019 at 6:13']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'consultation_booking'
        assert result.message.upper() == 'COMP9334 @@@ 06:13:00 @@@ 2019-11-01'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_indicative_hours_queries():
    query_module = QueryModule()
    test_messages = ['How long will I spend on COMP9517?',
                     'Indicative hour for COMP9517??',
                     'Work load for COMP9517??',
                     'Number of hours for COMP9517',
                     'Expected workload for COMP9517',
                     'Give me the indicative hours for COMP9517',
                     'How many hours a week for COMP9517']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'indicative_hours_queries'
        assert result.message.upper() == 'COMP9517'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_prerequisites_queries():
    query_module = QueryModule()
    test_messages = ['Prerequisites for COMP9444',
                     'Prerequisites for COMP9444??',
                     'What courses do I need to take before COMP9444??',
                     "COMP9444's prerequisites",
                     'What are the prerequisites for COMP9444',
                     'Requirements for COMP9444',
                     "COMP9444's requirements",
                     'Are there any classes I need to take before doing COMP9444?',
                     'Give me the prerequisites for COMP9444',
                     'What are the prerequisites for COMP9444??',
                     'What are the requirements for COMP9444??']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'prerequisites_queries'
        assert result.message.upper() == 'COMP9444'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded
