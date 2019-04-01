from database.DataBaseManager import DataBaseManager
from conf.Logger import Logger
"""
    Logger setup
"""
logger = Logger(__name__).log


class ManagementModule:
    def __init__(self):
        self.data_base_manager = DataBaseManager()

    def upload_new_file(self, file):
        self.data_base_manager.upload_file(file, file)

    def read_file_from_storage(self, file):
        self.data_base_manager.read_file(file)

    def get_storage_content(self):
        return self.data_base_manager.get_list_of_files_from_storage()


if __name__ == '__main__':
    management_module = ManagementModule()
