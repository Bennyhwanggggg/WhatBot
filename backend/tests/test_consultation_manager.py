from utility_module.ConsultationManager import ConsultationManager


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
