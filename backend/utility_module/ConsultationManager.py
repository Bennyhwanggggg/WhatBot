"""
    Consultation Booking Manager. This class is responsible for all
    operations relating to the consultation booking feature.
"""
from database.DataBaseManager import DataBaseManager
import datetime
from conf.Logger import Logger

logger = Logger(__name__).log


class ConsultationManager:
    def __init__(self, data_base_manager=DataBaseManager()):
        self.data_base_manager = data_base_manager
        self.initial_time_slots = ['09:00:00',
                                   '10:00:00',
                                   '11:00:00',
                                   '12:00:00',
                                   '13:00:00',
                                   '14:00:00',
                                   '15:00:00',
                                   '16:00:00',
                                   '17:00:00']

    def add_consultation(self, cid, sid, time, date):
        time = self.round_time(time)
        if not self.check_valid_booking_time(time):
            return "Consultation can only be booked between 9:00 to 17:00"
        query = "INSERT INTO consultation(cid, sid, time, date) VALUES (%s, %s, %s, %s)"
        inputs = (cid, sid, time, date)
        return self.data_base_manager.execute_query(query, inputs)

    def delete_consultation(self, cid, sid, time, date):
        query = "DELETE FROM consultation WHERE cid = %s and sid = %s and time = %s and date = %s"
        inputs = (cid, sid, time, date)
        return self.data_base_manager.execute_query(query, inputs)

    def next_seven_day(self):
        """Getting the date of 7 days later from current day.

        :return: next week's date of current day
        :rtype: str
        """
        today = datetime.date.today()
        week_next = today + datetime.timedelta(days=7)
        return week_next.strftime('%Y-%m-%d')

    def update_consultation(self):
        """ Update consultation database

        :return: SQL execution status
        """
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        key_part = '%' + date
        query = "DELETE FROM consultation WHERE date < %s"
        inputs = (key_part, )
        return self.data_base_manager.execute_query(query, inputs)

    def check_weekday(self, date):
        week_next = self.next_seven_day()
        today = datetime.date.today().strftime('%Y-%m-%d')
        if not date or date > week_next or date < today:  # check the date is within one week
            return False, "It may be beyond the range, your booking date must before {}".format(week_next)

        week_days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        date_convert = date.split('-')
        date_list = [int(i) for i in date_convert]
        try:
            day = datetime.date(date_list[0], date_list[1], date_list[2])
            num_day = day.weekday()  # convert weekday into digit (eg Mon -> 0,)
            if num_day == 5 or num_day == 6:
                logger.info("Sorry, there is no consultation on weekends")
                return False, "Sorry, there is no consultation on weekends"
            else:
                day_as_string = week_days[num_day]
                logger.info("It is on next {}".format(day_as_string))
                return True, "Your booking is on {} {}".format(day_as_string, date)
        except ValueError as e:
            logger.error(str(e))
            return False, "Please try again"

    def get_time_slots(self, cid, date):
        query = "SELECT time from consultation where cid = %s and date = %s"
        inputs = (cid, date)
        array_book = self.data_base_manager.execute_query(query, inputs)
        array_book = [e[0] for e in array_book]
        booked = array_book if array_book else []
        return booked

    def get_avail_time_slots(self, cid, date):
        booked = self.get_time_slots(cid, date)
        avail_time_slots = []
        for time in self.initial_time_slots:
            if time not in booked:
                avail_time_slots.append(time)
        return avail_time_slots

    def consultation_booking_query(self, cid, sid, time, date):
        is_weekday, feedback = self.check_weekday(date)
        if is_weekday:
            try:
                avail_list = self.get_avail_time_slots(cid, date)  # return available time slot list
                logger.debug(avail_list)
                if time in avail_list:
                    result = self.add_consultation(cid, sid, time, date)  # add into database
                    return "{} {}".format(result, feedback)
                else:
                    if not avail_list:
                        return "Sorry, there is no available time slot on date"
                    result = "Sorry this time slot has been booked, " \
                             "please choose another one from following time slots on {}".format(date)
                    return '{}: {}'.format(result, ', '.join(avail_list))
            except ValueError:
                logger.error("Invalid Input")
                return
        else:
            logger.debug(feedback)
            return feedback

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
        return '{:02d}:00:00'.format(int(hour)+1 ) if int(mins) >= 30 else '{:02d}:00:00'.format(int(hour))

