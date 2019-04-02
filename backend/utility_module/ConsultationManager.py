"""
    Consultation Booking Manager. This class is responsible for all
    operations relating to the consultation booking feature.
"""
from database.DataBaseManager import DataBaseManager


class ConsultationManager:
    def __init__(self, data_base_manager=DataBaseManager()):
        self.data_base_manager = data_base_manager

    def add_consultation(self, cid, sid, time, date):
        time = self.round_time(time)
        if not self.check_valid_booking_time(time):
            return "Consultation can only be booked between 9AM to 5PM"
        query = "INSERT INTO consultation(cid, sid, time, date) VALUES (%s, %s, %s, %s)"
        inputs = (cid, sid, time, date)
        return self.data_base_manager.execute_query(query, inputs)

    def delete_consultation(self, cid, sid, time):
        query = "DELETE FROM consultation WHERE cid = %s and sid = %s and time = %s"
        inputs = (cid, sid, time)
        return self.data_base_manager.execute_query(query, inputs)

    def check_avail_time_slots(self, cid):
        initial_time_slots = ['9:00',
                              '10:00',
                              '11:00',
                              '12:00',
                              '13:00',
                              '14:00',
                              '15:00',
                              '16:00',
                              '17:00']
        key_part = '%' + cid
        inputs = (key_part,)
        query = "SELECT time from consultation where cid like %s"
        booked = list(self.data_base_manager.execute_query(query, inputs)[0])
        avail_time_slots = []
        for time in initial_time_slots:
            if time not in booked:
                avail_time_slots.append(time)
        return avail_time_slots

    def check_valid_booking_time(self, time):
        """ Check if a valid booking time. Time should be in 24 hour format of hh:mm:ss

        :param time: time to check:
        :type: str
        :return: whether it is valid time or not
        :rtype: bool
        """
        hour, _, _ = time.split(":")
        return True if 9 <= int(hour) <= 17 else False

    def round_time(self, time):
        """Time rounding function to convert time to nearest hour

        :param time: current time in format of hh:mm:ss
        :type: str
        :return: the rounded time in format of hh:mm:ss
        :rtype: str
        """
        hour, mins, _ = time.split(":")
        return '{:02d}:00:00'.format(int(hour)+1) if int(mins) >= 30 else '{:02d}:00:00'.format(int(hour))
