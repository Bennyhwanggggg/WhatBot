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
            Initialise the UtilityModule class. This uses a single data base manager instance to manage
            all database connection related work.
        """
        self.data_base_manager = DataBaseManager()
        self.wam_calculator = WamCalculator(courses=self.get_student_academic_results())
        self.consultation_manager = ConsultationManager(data_base_manager=self.data_base_manager)
        self.class_room_finder = ClassRoomFinder()

    def get_student_academic_results(self):
        """ Get a list of course name and their result for a student

        :return: course result list
        :type: [{course_name: string, number_of_credits: int, score: float}, {course_name: string, number_of_credits: int, score: float}]
        """
        # TODO: get student courses and results from database
        pass
