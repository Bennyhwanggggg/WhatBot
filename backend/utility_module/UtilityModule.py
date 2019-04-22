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
from utility_module.AnnoucementGetter import AnnouncementsGetter
from utility_module.CourseTimeTableFinder import CourseTimeTableFinder
from database.DataBaseManager import DataBaseManager
from emailer.EmailSender import EmailSender


class UtilityModule:
    def __init__(self, database_manager=DataBaseManager()):
        """
            Initialise the UtilityModule class. This uses a single data base manager instance to manage
            all database connection related work. Upon initialisation, we preload data that are often fix
            like class room location information and student marks into memory so we don't need to keep
            accessing the database everytime.
        """
        self.data_base_manager = database_manager
        self.wam_calculator = WamCalculator(database_manager=self.data_base_manager)
        self.consultation_manager = ConsultationManager(database_manager=self.data_base_manager)
        self.class_room_finder = ClassRoomFinder(database_manager=self.data_base_manager)
        self.announcement_getter = AnnouncementsGetter(database_manager=self.data_base_manager)
        self.course_timetable_finder = CourseTimeTableFinder(database_manager=self.data_base_manager)
        self.class_room_finder.get_all_classroom()
        self.emailer = EmailSender()
