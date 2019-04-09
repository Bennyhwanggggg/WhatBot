from utility_module.ConsultationManager import ConsultationManager
from database.DataBaseManager import DataBaseManager
import pandas as pd
from pandas import DataFrame


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
    tests_date = ["2019-04-10", "2019-04-13", "2019-04-18"]
    expected = ["Your booking is on Wednesday 2019-04-10", "Sorry, there is no consultation on weekends", "It may be beyond the range, your booking date must before 2019-04-16"]
    for i in range(len(tests_date)):
    is_weekday, feedback = consultation_manager.check_weekday(tests_date[i])
    assert feedback == expected[i]

    
class Consultation_Test():
    def __init__(self):
        self.data_base_manager = DataBaseManager()
        self.consultation_manager = ConsultationManager()
        self.data = None

    def get_consultation(self, cid, sid):
        query = "SELECT * from consultation where cid = %s and sid = %s"
        inputs = (cid, sid)
        result = self.data_base_manager.execute_query(query, inputs)
        df = pd.DataFrame(data=result, columns=['cid', 'sid', 'time', 'date'])
        self.data = df
        print(df)
        return df

    def avail_timeslot_query(self, cid, sid, time, date):
        if self.data is None:
            self.get_consultation(cid, sid)
        for index, row in self.data.iterrows():
            course_id, student_id, timeslot, year_m_d = row['cid'], row['sid'], row['time'], row['date']
            if course_id == cid and student_id == sid and year_m_d == date and timeslot == time:
                result_string = "Sorry this time slot has been booked"
                return result_string
        return "This timeslot is available"

    
def test_consultation():
    inputs = [["COMP9900", "z5111111", "09:00:00", "2019-04-10"],["COMP9900", "z5111111", "10:00:00", "2019-04-10"]]
    expected = ["Sorry this time slot has been booked", "This timeslot is available"]#Sorry this time slot has been booked
    consultation_test = Consultation_Test()
    for i in range(len(inputs)):
        s = consultation_test.avail_timeslot_query(inputs[i][0],inputs[i][1],inputs[i][2],inputs[i][3])
        assert s == expected[i]


