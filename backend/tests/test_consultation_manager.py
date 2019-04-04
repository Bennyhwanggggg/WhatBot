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


def test_consultation_booking_query():
    consultation_manager = ConsultationManager()
    inputs = [["COMP9900", "z5111111", "09:00", "2019-04-10"], ["COMP9900", "z5111111", "09:00", "2019-04-10"],["COMP9900", "z5111111", "10:00", "2019-04-07"]]
    expected_1 = "execute successfully Your booking is on next Wednesday"
    expected_2 = "Sorry this time slot has been booked, please choose another one from following time slots on 2019-04-1010:00:00, 11:00:00, 12:00:00, 13:00:00, 14:00:00, 15:00:00, 16:00:00, 17:00:00"#availabale tiemslot list
    expected_3 = "Sorry, there is no consultation on weekends"
    compare = [expected_1, expected_2, expected_3]
    for i in range(len(inputs)):

        result = consultation_manager.consultation_booking_query(inputs[i][0], inputs[i][1], inputs[i][2], inputs[i][3])
        print(result)
        assert result == compare[i]

