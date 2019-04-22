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
from utility_module.emailer import EmailSender
from database.DataBaseManager import DataBaseManager


class UtilityModule:
    def __init__(self, database_manager=DataBaseManager()):
        """
            Initialise the UtilityModule class. This uses a singleton class that uses single data base manager
            instance to manage all database connection related work. Upon initialisation, we preload data that are
            often fix ike class room location information and student marks into memory so we don't need to keep
            accessing the database every time.
        """
        self.data_base_manager = database_manager
        self.emailer = EmailSender()
        self.wam_calculator = WamCalculator(database_manager=self.data_base_manager)
        self.consultation_manager = ConsultationManager(database_manager=self.data_base_manager, emailer=self.emailer)
        self.class_room_finder = ClassRoomFinder(database_manager=self.data_base_manager)
        self.announcement_getter = AnnouncementsGetter(database_manager=self.data_base_manager)
        self.course_timetable_finder = CourseTimeTableFinder(database_manager=self.data_base_manager)
        self.class_room_finder.get_all_classroom()
