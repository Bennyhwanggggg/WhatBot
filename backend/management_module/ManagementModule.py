from database.DataBaseManager import DataBaseManager
from conf.Logger import Logger
from query_module.train import QueryModuleTrainer
import os
import datetime
from collections import Counter, defaultdict
"""
    Logger setup
"""
logger = Logger(__name__).log

"""
    Path setup
"""
PATH = os.path.dirname(os.path.realpath(__file__))
INTENT_PATH = os.path.join(PATH, '../query_module/training_data/intents/')
ENTITY_PATH = os.path.join(PATH, '../query_module/training_data/entities/')


class ManagementModule:
    def __init__(self, database_manager=DataBaseManager(), trainer=QueryModuleTrainer()):
        self.database_manager = database_manager
        self.trainer = trainer

    def train(self, file_path):
        """Given a file path, check if it is a valid file and whether the file
        is supposed to be used for training intent or entity then performs the
        relevant training if the file is valid. If training successful, we upload
        the file to AWS S3 for storage. Returns true when everything is successful
        otherwise false.

        :param file_path: path to file to train
        :type: str
        :return: whether training is successful or not
        :rtype: bool
        """
        if self.check_intent_file_format(file_path):
            intent_file_path = os.path.join(INTENT_PATH, os.path.basename(file_path))
            os.rename(file_path, intent_file_path)
            if self.train_new_intent(intent_file_path):
                return self.upload_new_file(intent_file_path)
        elif self.check_entity_file_format(file_path):
            entity_file_path = os.path.join(ENTITY_PATH, os.path.basename(file_path))
            os.rename(file_path, entity_file_path)
            if self.train_new_entity(entity_file_path):
                return self.upload_new_file(entity_file_path)
        return False

    def upload_new_file(self, file):
        """Upload a file to AWS S3. The file will be stored using the same name provided
        on S3.

        :param file: file to store
        :type: str
        :return: None
        """
        try:
            self.database_manager.upload_file(file, os.path.basename(file))
        except Exception as e:
            logger.error(str(e))
            return False
        return True

    def check_intent_file_format(self, file_path):
        """Check if the file is a correct intent training data file format. Format should follow the directions provided at:
        https://github.com/comp3300-comp9900-term-1-2019/capstone-project-whatbot/tree/master/backend/query_module

        :param file_path: path to file
        :type: str
        :return: whether it is a valid file or not
        :rtype: bool
        """
        invalid_result = [(None, [], [], [], [], [], [], [], False)]
        return False if invalid_result == [self.trainer.read_intents_data(file_path)] else True

    def check_entity_file_format(self, file_path):
        """Check if the file is a correct entity training data file format. Format should follow the directions provided at:
        https://github.com/comp3300-comp9900-term-1-2019/capstone-project-whatbot/tree/master/backend/query_module

        :param file_path: path to file
        :type: str
        :return: whether it is a valid file or not
        :rtype: bool
        """
        invalid_result = [(None, [], [])]
        return False if invalid_result == [self.trainer.read_entities_data(file_path)] else True

    def train_new_intent(self, file_path):
        """Train a new intent using trainer. If the intent already exist, old one will be replaced

        :param file_path: path to file to train
        :type: str
        :return: success status
        :rtype: bool
        """
        try:
            display_name, message_texts, intent_types, parent_followup, input_contexts, output_contexts, action, data, reset_contexts = self.trainer.read_intents_data(file_path)
            if self.trainer.get_intent_ids(display_name):
                self.trainer.delete_intent(display_name)
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
        except Exception as e:
            logger.error(str(e))
            return False
        return True

    def train_new_entity(self, file_path):
        """Train a new entity using trainer. If the entity exist, the newly uploaded one
        will take effect and old one will be deleted.

        :param file_path: path to the data file
        :type: str
        :return: success status
        :rtype: bool
        """
        try:
            display_name, entity_values, synonyms = self.trainer.read_entities_data(file_path)
            if self.trainer.get_entity_ids(display_name):
                self.trainer.delete_entity(display_name)
            self.trainer.create_entity(display_name, entity_values, synonyms)
        except Exception as e:
            logger.error(str(e))
            return False
        return True

    def read_file_from_storage(self, file):
        """Read a file on AWS S3 and load its content into memory

        :param file: file to read
        :type: str
        :return: content of the file
        :rtype: list[str]
        """
        return self.database_manager.read_file(file)

    def get_all_storage_content(self):
        """Get list of files in AWS S3 storage

        :return: list of file names
        :type: list[str]
        """
        return self.database_manager.get_list_of_files_from_storage()

    def add_intent_data(self, intent, query_text, confidence, timestamp=datetime.datetime.now()):
        """Collect user data and upload it to database

        :param intent: intent that the user triggered
        :type: str
        :param query_text: user's query text
        :type: str
        :param confidence: the confidence level from Dialogflow
        :type: float
        :param: timestamp: timestamp when the query is entered
        :type: datetime
        :return: query execution status
        :rtype: str
        """
        query = "INSERT INTO intent_data(intent, query_text, confidence, timestamp) VALUES (%s, %s, %s, %s)"
        inputs = (intent, query_text, confidence, timestamp)
        return self.database_manager.execute_query(query, inputs)

    def get_intent_percentages(self, n=8):
        """Retrieve intent usage and calculate their percentage use

        :param: number of top intents to get
        :type: int
        :return: intent usage percentage data
        :rtype: list of tuples of (intent, value)
        """
        query = "SELECT intent FROM intent_data"
        data = [result[0] for result in self.database_manager.execute_query(query)]
        result = Counter(data)
        total_queries = sum(result.values())
        most_common = result.most_common(n)
        others = total_queries - sum(intent[1] for intent in most_common)
        most_common.append(('others', others))
        return most_common

    def get_intent_timeline(self):
        """Retrieve intent usage against time. Only retrieve the last 7 day.

        :return: each intent and their usage for last 7 days
        :rtype: defaultdict(list) with intent being the key and the list contains last 7 day usage
        """
        query = "SELECT intent, timestamp FROM intent_data WHERE timestamp > current_date - interval '7 days'"
        result = self.database_manager.execute_query(query)
        result = [(res[0], res[1].date()) for res in result]
        intents = set([res[0] for res in result])
        last_seven_days = [datetime.datetime.today() - datetime.timedelta(days=i) for i in range(1, 8)]
        counts = Counter(result)
        timeline_data = defaultdict(list)
        for intent in intents:
            timeline_data.setdefault(intent, [])
        day_num = 1
        for date in reversed(last_seven_days):
            seen = set()
            for intent, timestamp in result:
                if intent not in seen and timestamp == date.date():
                    timeline_data[intent].append(counts[intent, date.date()])
                    seen.add(intent)
            for intent in timeline_data.keys():
                if len(timeline_data[intent]) != day_num:
                    timeline_data[intent].append(0)
            day_num += 1
        return timeline_data


a = ManagementModule()
print(a.get_intent_timeline())
