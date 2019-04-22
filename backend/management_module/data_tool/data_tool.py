import numpy as np
import datetime
import random
from management_module.data_tool._data_source import *
from management_module.ManagementModule import ManagementModule
from database.DataBaseManager import DataBaseManager
from conf.Logger import Logger

"""
    Logger setup
"""
logger = Logger(__name__).log


class DataTool:
    def __init__(self, database_manager=DataBaseManager()):
        self.database_manager = database_manager
        self.management_module = ManagementModule(database_manager=self.database_manager)

    def get_random_index(self, n=6):
        probs = np.random.dirichlet(np.ones(n), size=1)
        return np.random.choice(np.arange(0, n), p=probs[0])

    def get_random_amp(self):
        return random.choice(range(-5, 5)) / 100

    def generate(self, n_timeslot=10000):
        for i in range(n_timeslot):
            ts = datetime.datetime.now() - datetime.timedelta(seconds=i * 42)
            idx = self.get_random_index()
            intent = intent_list[idx][0]
            template_sentence_list = intent_list[idx][1]
            base_confidence = intent_list[idx][2]
            confidence = base_confidence + self.get_random_amp()
            course_name = random.choice(course_list)[0]
            query_text = random.choice(template_sentence_list).format(course_code=course_name)
            self.management_module.add_intent_data(intent, query_text, confidence, str(ts))
            logger.debug("{} {} {} {}".format(intent, query_text, confidence, str(ts)))


if __name__ == "__main__":
    data_tools = DataTool()
    data_tools.generate()

