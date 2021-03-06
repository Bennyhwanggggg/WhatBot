from query_module.QueryModule import QueryModule
import time

TIME_BETWEEN_API = 1.5


def test_clean_message():
    query_module = QueryModule()
    test_messages = ['COMP9900?',
                     '&Comp9900?!!',
                     'comp9900???',
                     "Comp9900''''s",
                     'COmp9900!!!!',
                     "~~Comp9900's?",
                     '>COMP9900?[<',
                     "...comp9900's",
                     "*comp9900's's",
                     "COMP9900''s",
                     'the COMP9900',
                     'For COMP9900',
                     'The comp9900']
    for test_message in test_messages:
        result = query_module.clean_message(test_message)
        assert result.upper() == 'COMP9900'


def test_detect_intent():
    query_module = QueryModule()
    test_messages = ['I want to know the outline for COMP9900',
                     "What is COMP9900's course name?",
                     'IsComp9900 a good course?',
                     'Who is the lecturer fo COMP9900?']
    for test_message in test_messages:
        result = query_module.detect_entity(test_message)
        assert result.upper() == 'COMP9900'

    test_messages = ['COMP9900 11/12/2019 11am',
                     '11/12/2019 COMP9900 11am',
                     '11/12/2019, coMp9900 11am']
    for test_message in test_messages:
        result = query_module.detect_entity(test_message)
        assert result.upper() == 'COMP9900 @@@ 11:00:00 @@@ 2019-12-11'

    test_messages = ['I want COMP9321 7/12/2019 11:11am',
                     '07/12/2019 COMP9321 11:11am',
                     '07/12/2019, coMp9321 11:11am?']
    for test_message in test_messages:
        result = query_module.detect_entity(test_message)
        assert result.upper() == 'COMP9321 @@@ 11:11:00 @@@ 2019-12-07'


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


def test_all_courses_queries():
    query_module = QueryModule()
    test_messages = ['I wanna know all the courses of postgraduate',
                     'I want to know the list of postgraduate courses',
                     "I want to get all the courses of postgraduate",
                     'I want to get all the courses',
                     'Can I get all postgraduate courses',
                     'Can I know all postgraduate courses',
                     'Can you show me all courses']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'all_courses_queries'
        assert result.message == 'Sure! These are all the courses of CSE!'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_wam_admin_queries():
    query_module = QueryModule()
    test_messages = ['I want to know the wam of z1234567',
                     'I want to get the wam of z1234567',
                     "Can I get the wam for z1234567",
                     'Can I know the wam for z1234567',
                     'Please tell me the wam for z1234567',
                     'Show me the wam for z1234567',
                     'The wam of z1234567']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'wam_admin_queries'
        assert result.message == 'z1234567'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_wam_student_queries():
    query_module = QueryModule()
    test_messages = ['I want to know my grades',
                     'Tell me about my WAM',
                     "Tell me about my grades",
                     'Show me my course results',
                     'My wam',
                     'What is my WAM',
                     'What are my grades right now?']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'wam_student_queries'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_course_timetable_queries():
    query_module = QueryModule()
    test_messages = ['I want to see COMP9321 timetable',
                     'Timetable for COMP9321',
                     "Tell me COMP9321's timetable",
                     'Show me COMP9321 timetable',
                     'COMP9321 timetable',
                     'When are the classes for COMP9321',
                     'Give me the timetable for comp9321 thanks']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'course_timetable_queries'
        assert result.message.upper() == 'COMP9321'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_announcement_queries():
    query_module = QueryModule()
    test_messages = ['COMP9900 announcement',
                     "COMP9900's announcement",
                     "Show me COMP9900's announcement",
                     'Give me COMP9900 announcement',
                     'announcement for COMP9900',
                     'What is the latest announcement for COMP9900',
                     'Give me the announcement for COMP9900 thanks']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'announcement_queries'
        assert result.message.upper() == 'COMP9900'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_consultation_cancelling_command():
    query_module = QueryModule()
    test_messages = ['Cancel my booking for COMP9334 at 06:45 at on 20/05/2019',
                     'Cancel my appointment with LiC for COMP9334 at 20/05/2019 06:45',
                     'Please cancel my consultation for COMP9334 at 06:45 on 20/05/19',
                     'Cancel my consultation at 06:45 on 20/05/19 for COMP9334',
                     'Can I cancel the consultation for COMP9334 on 20/05/19 06:45?',
                     'Can I cancel my consultation for COMP9334 at 06:45 on 20/05/2019?',
                     'Cancel course consultation booking for COMP9334 at 06:45 20/05/19',
                     'Cancel booking for COMP9334 on 06:45 20/05/19',
                     'Cancel my course consultation for COMP9334 at 06:45 on 20/05/19',
                     'I want to cancel my course consultation booking for COMP9334 on 20/05/19 at 06:45']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'consultation_cancel'
        assert result.message.upper() == 'COMP9334 @@@ 06:45:00 @@@ 2019-05-20'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded

        
def test_adk_queries():
    query_module = QueryModule()
    test_messages = ['Could you please tell me COMP9900 a ADK or not',
                     "ADK COMP9900?",
                     "COMP9900 ADK?",
                     'Tell me if COMP9900 a ADK course or not',
                     'Could you please tell me COMP9900 a ADK or not',
                     'Could you please tell me if COMP9900 an ADK',
                     'Could you please tell me if COMP9900 a ADK or not?']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'adk_course_queries'
        assert result.message.upper() == 'COMP9900'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded


def test_consultation_view():
    query_module = QueryModule()
    test_messages = ['May I check my consultation booking',
                     'What are my consultation bookings right now?',
                     'I want to see my list of consultation bookings',
                     'Show me my consultation booking',
                     'View my consultation bookings',
                     'Check my consultation bookings',
                     'See my consultation bookings',
                     'Show me my consultation booking history ']
    for test_message in test_messages:
        result = query_module.detect_intent_texts(test_message)
        assert result.intent == 'consultation_view'
        time.sleep(TIME_BETWEEN_API)  # set gap so Google API doesn't get overloaded
