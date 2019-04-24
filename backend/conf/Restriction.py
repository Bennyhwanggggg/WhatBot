"""
    This file contains the Rules class which sets restrictions for access
"""


class Rules:
    def __init__(self):
        """Initialise the Rule class which restrict access to parts of the programs
        for security purpose.
        """
        self.restricted = set(['consultation_booking_with_followup.txt',
                               'consultation_booking_with_followup-user_input_course_code_with_followup.txt',
                               'consultation_booking_with_followup-user_input_course_code_with_followup-user_input_time_and_date.txt',
                               'consultation_booking_with_followup-user_input_time_and_date_with_followup.txt',
                               'consultation_booking_with_followup-user_input_time_and_date_with_followup-user_input_course_code.txt'])
