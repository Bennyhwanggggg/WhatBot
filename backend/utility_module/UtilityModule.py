"""
    This class contains the main Utility Module. It will be responsible
    for managing the classes that provide its features.
    Features include:
        - A WAM calculator
        - Get lecturer announcements.
        - Classroom and tutorial locator
        - Consultation Booking
"""
from utility_module.WamCalculator import WamCalculator
from utility_module.ConsultationManager import ConsultationManager
from utility_module.ClassRoomFinder import ClassRoomFinder
from database.DataBaseManager import DataBaseManager


class UtilityModule:
    def __init__(self):
        """
            Initialise the UtilityModule class. This module should contain
            the following features:
                1. Consultation booking calendar
                2. WAM Calculator
                3. Class room finder
                And possibly more
        """
        self.data_base_manager = DataBaseManager()
        self.wam_calculator = WamCalculator()
        self.consultation_manager = ConsultationManager(data_base_manager=self.data_base_manager)
        self.class_room_finder = ClassRoomFinder()

    def get_student_academic_results(self):
        # TODO: get student courses and results from database
        pass
