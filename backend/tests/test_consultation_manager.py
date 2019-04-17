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


def test_make_booking():
    consultation_manager = ConsultationManager()
    today = datetime.datetime.today()
    date = today.strftime('%Y-%m-%d')
    day_as_string = consultation_manager.get_the_weekday(date)
    while day_as_string == 'Saturday' or day_as_string == 'Sunday':
        today = datetime.datetime.today() + datetime.timedelta(days=2)
        date = today.strftime('%Y-%m-%d')
        day_as_string = consultation_manager.get_the_weekday(date)
    inputs = [["COMP9900", "z5111111", "09:00:00", date], ["COMP9900", "z5111111", "09:00:00", date]]
    expected = ["Your booking is on {} {}".format(day_as_string, date),
                "Sorry this time slot has been booked, please choose another one from following time slots on {}: 10:00:00, 11:00:00, 12:00:00, 13:00:00, 14:00:00, 15:00:00, 16:00:00, 17:00:00".format(date)]
    consultation_manager = ConsultationManager()
    consultation_manager.database_manager = MockDatabase('CONSULTATION', ['cid', 'sid', 'time', 'date'])
    consultation_manager.get_time_slots = consultation_manager.database_manager.get_time_slots
    consultation_manager.add_consultation = consultation_manager.database_manager.add_consultation
    test_case = 0
    for cid, sid, time, date in inputs:
        s = consultation_manager.consultation_booking_query(cid, sid, time, date)
        assert s == expected[test_case]
        test_case += 1
