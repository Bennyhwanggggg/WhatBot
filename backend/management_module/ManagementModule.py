from database.DataBaseManager import DataBaseManager
from conf.Logger import Logger
from query_module.train import QueryModuleTrainer
import os
"""
    Logger setup
"""
logger = Logger(__name__).log


class ManagementModule:
    def __init__(self):
        self.data_base_manager = DataBaseManager()
        self.trainer = QueryModuleTrainer()

    def upload_new_file(self, file):
        """Upload a file to AWS S3. The file will be stored using the same name provided
        on S3.

        :param file: file to store
        :type: str
        :return: None
        """
        # verify the format
        self.data_base_manager.upload_file(file, os.path.basename(file))

    def train_new_intent(self, file_path):
        display_name, message_texts, intent_types, parent_followup, input_contexts, output_contexts, action, data, reset_contexts = self.trainer.read_intents_data(file_path)
        self.trainer.create_intent(display_name=display_name,
                                           message_texts=message_texts,
                                           intent_types=intent_types,
                                           training_data=data,
                                           input_contexts=input_contexts,
                                           output_contexts=output_contexts,
                                           action=action,
                                           data_is_parsed=True,
                                           reset_contexts=reset_contexts,
                                           parent_followup=parent_followup)


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
