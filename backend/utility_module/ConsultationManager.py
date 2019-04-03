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
            return "Consultation can only be booked between 9:00 to 17:00"
        query = "INSERT INTO consultation(cid, sid, time, date) VALUES (%s, %s, %s, %s)"
        inputs = (cid, sid, time, date)
        return self.data_base_manager.execute_query(query, inputs)

    def delete_consultation(self, cid, sid, time):
        query = "DELETE FROM consultation WHERE cid = %s and sid = %s and time = %s"
        inputs = (cid, sid, time)
        return self.data_base_manager.execute_query(query, inputs)

    def update_consultation(self):#update the consultation database everyday
            date = datetime.datetime.today().strftime('%Y-%m-%d')#eg. 2019-03-28
            key_part = '%' + date
            query = "DELETE FROM consultation WHERE date < %s"
            inputs = (key_part, )
            return self.data_base_manager.execute_query(query, inputs)

    def check_weekday(self,date):#check whether the booking day is valid, date like 2019-03-28
        week_next = self.next_seven_day()#get the date of 7 days later from current date
        today = datetime.date.today().strftime('%Y-%m-%d')
        if not date or date > week_next or date < today:#check the date is within one week
            return False, "It may be beyond the range, your booking date must before " + week_next

        weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
        date_convert = date.split('-')
        date_list = [int(i) for i in date_convert]
        try:
            day = datetime.date(date_list[0], date_list[1], date_list[2])# eg. should be 2017,12,25 integer parameters; <class 'datetime.date'>
            num_day = day.weekday()# convert weekday into digit (eg Mon -> 0,)
            if num_day == 5 or num_day == 6:# check whether it is on weekend
                print("Sorry, there is no consultation on weekends")
                return False, "Sorry, there is no consultation on weekends"
            else:
                DayAsString = weekDays[num_day]
                print("It is on next", DayAsString)
                return True, "It is on next " + DayAsString
        except ValueError:
            print("Wrong input date")
            return False, "Please try again"

    def consultation_booking_query(self, cid, sid, time, date):
        is_weekday, feedback = self.check_weekday(date)
        if is_weekday:
            try:
                avail_list = self.check_avail_timeslot(cid, date)#return available timeslot list
                if time in avail_list:
                    result = self.add_consultation(cid, sid, time, date)# add into database
                    print(result +"\n" +feedback)
                    return result +"\n"+ feedback
                else:
                    if not avail_list:
                        return "Sorry, there is no available time slot on date"
                    result = "Sorry this time slot has been booked, please choose another one from following time slots on " + date
                    print(avail_list)
                    return result + ', '.join(avail_list)
            except ValueError:
                print("Invalid Input")
                return
        else:
            print(feedback)
            return feedback


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
