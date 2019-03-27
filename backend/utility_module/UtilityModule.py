from utility_module.WamCalculator import WamCalculator
from utility_module.ConsultationManager import ConsultationManager
from utility_module.ClassRoomFinder import ClassRoomFinder

"""
A WAM calculator
Assignments and projects due date tracker
Latest progress made in lecture.
Get lecturer announcements. 
Classroom and tutorial locator

"""

class UtilityModule:
    def __init__(self):
        """
            Initialise the UtilityModule class. This module should contain
            the following features:
                1. Consultation booking calendar
                2. WAM Calculator
                3. Class room finder TODO: Can someone clarify how this should be done..?
                And possibly more
        """
        self.courses = dict()  # TODO: Will this be based on some user in the database? @Wayne can you confirm?
        self.wam_calculator = WamCalculator()
        self.consultation_manager = ConsultationManager()
        self.class_room_finder = ClassRoomFinder()
