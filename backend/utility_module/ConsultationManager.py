from database.DataBaseManager import DataBaseManager
import datetime


class ConsultationManager:
    def __init__(self, data_base_manager=DataBaseManager()):
        self.data_base_manager = data_base_manager

    def add_consultation(self, cid, sid, time, date):
        query = "INSERT INTO consultation(cid, sid, time, date) VALUES (%s, %s, %s, %s)"
        inputs = (cid, sid, time, date)
        return self.data_base_manager.execute_query(query, inputs)

    def delete_consultation(self, cid, sid, time):
        query = "DELETE FROM consultation WHERE cid = %s and sid = %s and time = %s"
        inputs = (cid, sid, time)
        return self.data_base_manager.execute_query(query, inputs)

    def check_avail_time_slots(self, cid):
        initial_time_slots = ['9:00AM',
                              '10:00AM',
                              '11:00AM',
                              '12:00AM',
                              '1:00PM',
                              '2:00PM',
                              '3:00PM',
                              '4:00PM',
                              '5:00PM']
        key_part = '%' + cid
        inputs = (key_part,)
        query = "SELECT time from consultation where cid like %s"
        booked = list(self.data_base_manager.execute_query(query, inputs)[0])
        avail_time_slots = []
        for time in initial_time_slots:
            if time not in booked:
                avail_time_slots.append(time)
        return avail_time_slots

    def round_time(self, time):
        # TODO: time rounding, input of time is 06:13:00
        timeSplit = time.split(":")
        hour = timeSplit[0]
        mins = timeSplit[1]
        if 9 <= int(hour) <= 12 or 1 <= int(hour) <= 5:
            if int(mins) >= 30:
                return str(int(hour)+1) + ":" + "00"
            if int(mins) < 30:
                return hour + ":" + "00"
        else:
            return "Please book consultation between 9AM to 5PM"


