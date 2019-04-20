import numpy
# import sys
# import os
import datetime
import random
from data_tool._data_source import *
from management_module.ManagementModule import ManagementModule
from database.DataBaseManager import DataBaseManager


def get_random_index():
    return numpy.random.choice(numpy.arange(0, 5),
                               p=[0.02, 0.12, 0.16, 0.25, 0.45])


def get_random_amp():
    return random.choice(range(-5, 5)) / 100


def main():
    database_manager = DataBaseManager()
    management_module = ManagementModule(database_manager=database_manager)
    n_timeslot = 10000
    for i in range(n_timeslot):
        ts = datetime.datetime.now() - datetime.timedelta(seconds=i * 42)
        idx = get_random_index()
        intent = intent_list[idx][0]
        template_sentence_list = intent_list[idx][1]
        base_confidence = intent_list[idx][2]
        confidence = base_confidence + get_random_amp()
        course_name = random.choice(course_list)[0]
        query_text = random.choice(template_sentence_list).format(course_code=course_name)
        management_module.add_intent_data(intent, query_text, confidence, str(ts))
        print("[DEBUG] ", intent, query_text, confidence, str(ts))


if __name__ == "__main__":
    # print("hello")
    main()

