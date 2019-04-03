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
        """Upload a file to AWS S3. The file will be stored using the same name provided
        on S3.

        :param file: file to store
        :type: str
        :return: None
        """
        self.data_base_manager.upload_file(file, file)

    def read_file_from_storage(self, file):
        """Read a file on AWS S3 and load its content into memory

        :param file: file to read
        :type: str
        :return: content of the file
        :rtype: list[str]
        """
        return self.data_base_manager.read_file(file)

    def get_all_storage_content(self):
        """Get list of files in AWS S3 storage

        :return: list of file names
        :type: list[str]
        """
        return self.data_base_manager.get_list_of_files_from_storage()


if __name__ == '__main__':
    management_module = ManagementModule()
