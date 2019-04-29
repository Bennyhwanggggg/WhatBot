"""
    Consultation Booking Manager. This class is responsible for all
    operations relating to the consultation booking feature.
"""
from database.DataBaseManager import DataBaseManager
from utility_module.emailer.EmailSender import EmailSender
import datetime
from conf.Logger import Logger
from conf.Error import ConsultationError

logger = Logger(__name__).log


class ConsultationManager:
    def __init__(self, database_manager=DataBaseManager(), emailer=EmailSender()):
        """Instantiate the class with a database instance and also an SMTP instance which
        is responsible for sending confirmation emails. Also set available timeslots that
        people can book for.

        :param database_manager: Database instance
        :type: DataBaseManager
        :param emailer: SMTP email server instance
        :type: EmailSender
        """
        self.database_manager = database_manager
        self.emailer = emailer
        # Set available timeslots
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
        inputs = (cid.upper(), sid, time, date)
        return self.database_manager.execute_query(query, inputs)

    def delete_consultation(self, cid, sid, time, date):
        if not self.check_course_exist(cid):
           return ConsultationError.INVALID_COURSE.value
        check_empty = "Select * FROM consultation WHERE cid = %s and sid = %s and time = %s and date = %s"
        query = "DELETE FROM consultation WHERE cid = %s and sid = %s and time = %s and date = %s"
        inputs = (cid.upper(), sid, time, date)
        data_exist = self.database_manager.execute_query(check_empty, inputs)
        if not data_exist:
            return ConsultationError.INVALID_CANCEL.value
        self.emailer.send_confirm_cancelling(cid=cid, time=time, date=date, receiver='whatbot9900@gmail.com')
        return self.database_manager.execute_query(query, inputs)

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
        return self.database_manager.execute_query(query, inputs)

    def get_the_weekday(self,date):
        """Convert a date into weekday string form

        :param date: date to convert
        :type: str
        :return: week day
        :rtype: str
        """
        date_convert = date.split('-')
        week_days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        date_list = [int(i) for i in date_convert]
        day = datetime.date(date_list[0], date_list[1], date_list[2])
        # convert weekday into digit (eg Mon -> 0,)
        num_day = day.weekday()
        day_as_string = week_days[num_day]
        return day_as_string

    def check_weekday(self, date):
        """Check if a given date is a weekday and if not, we tell user they cannot book that day.
        Also check if the booking day is inside our allowed range which is one week.

        :param date: date to check
        :type: str
        :return: success or fail message
        :rtype: str
        """
        week_next = self.next_seven_day()
        today = datetime.date.today().strftime('%Y-%m-%d')
        if not date or date > week_next or date < today:  # check the date is within one week
            return False, "Sorry you can only booking consultation up to next one week. Your booking date must before {}".format(week_next)
        try:
            day_as_string = self.get_the_weekday(date)
            if day_as_string == "Saturday" or day_as_string == "Sunday":
                logger.info("Sorry, there is no consultation on weekends")
                return False, "Sorry, there is no consultation on weekends"
            else:
                logger.info("It is on next {}".format(day_as_string))
                return True, "Your booking has been made on {} {}".format(day_as_string, date)
        except ValueError as e:
            logger.error(str(e))
            return False, "Please try again"

    def get_time_slots(self, cid, date):
        """Get list of available times that are booked for a given date and course

        :param cid: course id
        :type: str
        :param date: date of booking
        :type: str
        :return: list of booked times
        :rtype: list
        """
        query = "SELECT time from consultation where cid = %s and date = %s"
        inputs = (cid, date)
        array_book = self.database_manager.execute_query(query, inputs)
        array_book = [e[0] for e in array_book]
        booked = array_book if array_book else []
        return booked

    def get_avail_time_slots(self, cid, date):
        """Given a course id and a date, get the list of not booked time on that date for that
        course

        :param cid: course id
        :type: str
        :param date: date to check
        :type: str
        :return: list of available times
        :rtype: list
        """
        booked = self.get_time_slots(cid, date)
        avail_time_slots = []
        for time in self.initial_time_slots:
            if time not in booked:
                avail_time_slots.append(time)
        return avail_time_slots

    def consultation_booking_query(self, cid, sid, time, date):
        """Main function for handling consultation booking query. Use the other helper function
        in this class to perform checks. First check the date and time to book is valid and then
        check if that time slot is free for booking. If successful, send the confirmation email to
        user

        :param cid: course id
        :type: str
        :param sid: student id
        :type: str
        :param time: time to book
        :type: str
        :param date: date to book
        :type: str
        :return: success status
        :rtype: str
        """
        if not self.check_course_exist(cid):
            return ConsultationError.INVALID_COURSE.value
        is_weekday, feedback = self.check_weekday(date)
        time = self.round_time(time)
        if is_weekday:
            try:
                avail_list = self.get_avail_time_slots(cid.upper(), date)  # return available time slot list
                logger.debug(avail_list)
                if time in avail_list:
                    self.add_consultation(cid, sid, time, date)  # add into database
                    self.emailer.send_confirm_booking(cid=cid, time=time, date=date, receiver='whatbot9900@gmail.com')
                    return "{}".format(feedback)
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

    def view_my_consultation(self, sid):
        """Function to see list of consultations

        :param sid: student id to check
        :type: str
        :return: list of consultations student has booked
        :rtype: list
        """
        query = "Select cid, time, date FROM consultation WHERE sid = %s "
        inputs = (sid, )
        return self.database_manager.execute_query(query, inputs)

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

    def check_course_exist(self, cid):
       course_codes = ['COMP9900', 'comp9321', 'COMP9945', 'COMP9101', 'COMP9041', 'COMP9331', 'COMP9311',
                      'COMP9414', 'COMP9841', 'COMP6451', 'COMP9024', 'COMP9021', 'COMP9020', 'COMP9322',
                      'COMP6714', 'COMP6771', 'COMP9153', 'COMP9313', 'COmp9417', 'COMP9444', 'COMP9334',
                      'COMP9517', 'COMP9201', 'COMP9102', 'COMP9315', 'COMP4121', 'COMP9323', 'COMP9318',
                      'COMP6441', 'comp9511', 'ComP9032', 'Comp4418', 'comP6324', 'CoMp9415', 'ComP4141',
                      'COmP6752', 'comP9211', 'comP9319', 'cOMP9336', 'comP6471', 'COMP9243', 'COMP9283',
                      'COMP5752', 'comp9814', 'GSOE9210', 'GSOE9220', 'GSOE9820', 'COMP9801', 'COMP9222',
                      'COMP9447', 'COMP4161', 'COMP6452', 'COMP6733', 'COMP6841', 'COMP9151', 'COMP9161',
                      'COMP9332', 'COMP9333', 'COMP9337', 'COMP9431', 'COMP6443', 'COMP6445', 'COMP6447',
                      'COMP6448', 'COMP6741', 'COMP6843', 'COMP6845', 'COMP9242', 'COMP9418', 'COMP9596',
                       'COMP6721', 'COMP9154', 'COMP9164', 'COMP9434', 'COMP9424', 'COMP9423']
       course_codes = [e.upper() for e in course_codes]
       if(cid.upper() in course_codes):
           return True
       return False

