"""
    This file contains the main ManagementModule class which is responsible
    for automation training and also data analytics features.
"""
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
        """Initialise the Management Module class with a database instance and also Query
        Trainer instance. The given instances will be the main instance that is responsible
        for the core features in this module.
        """
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
        query_result = self.database_manager.execute_query(query)
        data = [res[0] for res in query_result]
        result = Counter(data)
        total_queries = sum(result.values())
        most_common = result.most_common(n)
        # Get the top n result and categorise everything else into others
        others = total_queries - sum(intent[1] for intent in most_common)
        most_common.append(('others', others))
        return most_common

    def get_intent_timeline(self, n=5):
        """Retrieve intent usage against time. Only retrieve the last 7 day.

        :return: each intent and their usage for last 7 days
        :rtype: defaultdict(list) with intent being the key and the list contains last 7 day usage
        :return: last 7 day as datetime
        :rtype: list of datetime
        """
        query = "SELECT intent, timestamp FROM intent_data WHERE timestamp > current_date - interval '7 days'"
        data = self.database_manager.execute_query(query)
        result = [(res[0], res[1].date()) for res in data]
        intents = set([res[0] for res in result])
        # Get last seven days
        last_seven_days = [datetime.datetime.today() - datetime.timedelta(days=i) for i in range(7, 0, -1)]
        counts = Counter(result)
        # Get top results
        top_n = Counter([d[0] for d in data]).most_common(n)
        top_n = [a[0] for a in top_n]
        timeline_data = defaultdict(list)
        # form intents list
        for intent in intents:
            if intent in top_n:
                timeline_data.setdefault(intent, [])
        day_num = 1
        # Backward calculate and get the required data
        for date in reversed(last_seven_days):
            seen = set()
            for intent, timestamp in result:
                if intent not in top_n:
                    continue
                if intent not in seen and timestamp == date.date():
                    timeline_data[intent].append(counts[intent, date.date()])
                    seen.add(intent)
            for intent in timeline_data.keys():
                if len(timeline_data[intent]) != day_num:
                    timeline_data[intent].append(0)
            day_num += 1
        return timeline_data, last_seven_days

    def get_avg_confidence(self, n=8):
        """Get the average confidence level of each intent. Return bottom n

        :param n: top n result to get
        :type: int
        :return: Bottom n intents and their average confidence value
        :rtype: list of tuples of (intent, float)
        """
        query = "SELECT intent, AVG(confidence) FROM intent_data WHERE intent Not Like '%Missing%' GROUP BY intent"
        result = self.database_manager.execute_query(query)
        result = sorted(result, key=lambda x: x[1])  # filter the result
        result = [(res[0], float(res[1])) for res in result]
        return result[:n]

    def get_3d_chart_data(self, top_n=5, day_range=7, n_sample=75):
        """
        NOTE: corner-case, what if there isn't top 5 intents?
            -- it can be auto handled by python slice syntax
        Complexity: O(N*log(N)), N is the total visit number within day_range

        :param top_n: top n result to get
        :type: int
        :param day_range: number of days data
        :type: int
        :param n_sample: number of sample points
        :type: int
        :return: 3d data
        :rtype: dict
        """

        query = 'SELECT intent,timestamp FROM intent_data'
        ret = self.database_manager.execute_query(query)
        cnt = Counter([x[0] for x in ret])
        sorted_cnt = sorted(cnt.items(), key=lambda x: x[1])
        n_most_common_intent = {x[0] for x in sorted_cnt[-top_n:]}
        ret = [x for x in ret if x[0] in n_most_common_intent]
        sorted_ret = sorted(ret, key=lambda x: x[1])

        now = datetime.datetime.now()
        one_week = datetime.timedelta(days=day_range)
        ago = now - one_week
        total_seconds = one_week.total_seconds()

        # convert time attribute to total seconds from `ago`
        bus_timeline_data = [[x[0], (x[1] - ago).total_seconds()] for x in sorted_ret]

        # one list fan-out to be multiple list, each list corresponds with one intent
        timeline_data = dict()
        for x in bus_timeline_data:
            intent = x[0]
            if intent not in timeline_data:
                timeline_data[intent] = list()
            timeline_data[intent].append(x[1])

        # sampling for e.g 100 time points for the top N intents
        sample_timepoints = [total_seconds * (i / n_sample) for i in range(1, n_sample + 1)]
        sampled_timeline_data = dict()
        for intent in timeline_data:
            sampled_timeline_data[intent] = []
            cur_timeline = timeline_data[intent]
            i = 0
            for sample_point in sample_timepoints:
                while i < len(cur_timeline) and sample_point >= cur_timeline[i]:
                    i += 1
                day_range_point = day_range * (sample_point / total_seconds)
                sampled_timeline_data[intent].append((day_range_point, i + 1))

        # convert it to the form that 3D chart consumes
        ret = [
            [
                "Usage",
                "Time",
                "Intent"
            ],
        ]
        for intent in sampled_timeline_data:
            cur_sampled_timeline = sampled_timeline_data[intent]
            for x in cur_sampled_timeline:
                ret.append([x[1], x[0], intent])
        return ret
