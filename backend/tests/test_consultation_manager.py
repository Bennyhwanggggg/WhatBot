from utility_module.ConsultationManager import ConsultationManager
from tests.MockDatabase import MockDatabase
import datetime


def test_time_rounding():
    consultation_manager = ConsultationManager()
    test_cases = ['00:11:22', '00:13:33', '00:30:44', '11:29:50', '14:59:30', '17:45:11']
    expected = ['00:00:00', '00:00:00', '01:00:00', '11:00:00', '15:00:00', '18:00:00']
    for test, expect in zip(test_cases, expected):
        result = consultation_manager.round_time(test)
        assert expect == result


def test_valid_booking_time():
    consultation_manager = ConsultationManager()
    test_cases = ['00:11:22', '00:13:33', '08:30:44', '11:29:50', '14:59:30', '17:45:11', '17:25:11']
    expected = [False, False, True, True, True, False, True]
    for test, expect in zip(test_cases, expected):
        test = consultation_manager.round_time(test)
        result = consultation_manager.check_valid_booking_time(test)
        assert expect == result

        
def test_check_weekday():
    consultation_manager = ConsultationManager()
    tests_date = ["2019-04-10", "2019-04-13", "2119-04-18"]
    expected = ["Your booking is on Wednesday 2019-04-10", "Sorry, there is no consultation on weekends", "It may be beyond the range, your booking date must before {}".format(datetime.date.today().strftime('%Y-%m-%d'))]
    for idx, test_case in enumerate(tests_date):
        is_weekday, feedback = consultation_manager.check_weekday(test_case)
        assert feedback == expected[idx]

    
def test_make_booking():
    inputs = [["COMP9900", "z5111111", "09:00:00", "2019-04-10"], ["COMP9900", "z5111111", "09:00:00", "2019-04-10"]]
    expected = ["Your booking is on Wednesday 2019-04-10", "Sorry this time slot has been booked, please choose another one from following time slots on 2019-04-10: 10:00:00, 11:00:00, 12:00:00, 13:00:00, 14:00:00, 15:00:00, 16:00:00, 17:00:00"]
    consultation_manager = ConsultationManager()
    consultation_manager.data_base_manager = MockDatabase('CONSULTATION', ['cid', 'sid', 'time', 'date'])
    consultation_manager.get_time_slots = consultation_manager.data_base_manager.get_time_slots
    consultation_manager.add_consultation = consultation_manager.data_base_manager.add_consultation
    test_case = 0
    for cid, sid, time, date in inputs:
        s = consultation_manager.consultation_booking_query(cid, sid, time, date)
        s = s.lstrip()
        assert s == expected[test_case]
        test_case += 1

