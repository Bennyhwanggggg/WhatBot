import dialogflow_v2 as dialogflow
from uuid import uuid4
import os
import re
import random

DIALOGFLOW_PROJECT_ID = 'whatbot-v1'
GOOGLE_APPLICATION_CREDENTIALS = 'whatbot-v1-7a84dc8485c1.json'


class QueryTrainer():
    def __init__(self, project_id, credentials=GOOGLE_APPLICATION_CREDENTIALS):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
        self.project_id = project_id
        self.intent_client = dialogflow.IntentsClient()

        self.data_map = {
            'course code': self.get_training_course_codes
        }

        # the information regarding this map should match what is on DialogFlow setup
        self.intent_entity_map = {
            'course_fee': {'parse_key': ['course code'], 'entity_type': '@course', 'alias': 'course'},
            'course_outline': 'course code'
        }

        self.course_codes = ['COMP9900', 'comp9321', 'COMP9945', 'COMP9101', 'COMP9041', 'COMP9331', 'COMP9311',
                             'COMP9414', 'COMP9841', 'COMP6451', 'COMP9024', 'COMP9021', 'COMP9020', 'COMP9322',
                             'COMP6714', 'COMP6771', 'COMP9153', 'COMP9313', 'COMP9322', 'COmp9417', 'COMP9444',
                             'COMP8517', 'COMP9201', 'COMP9102', 'COMP9315', 'COMP4121', 'COMP9323', 'COMP9318']

    def read_data(self, data_file):
        data_file = open(data_file, 'r')
        data = data_file.read().split('\n')
        data_file.close()
        return data

    def get_training_course_codes(self, size):
        return [random.choice(self.course_codes) for _ in range(size)]

    def parse_data(self, data, types):
        """ Randomize the data with different entity types. Like changing the course
        codes for the training data. It will randomize the contents inside the training
        data themselves.

        E.g
        types = [course code]
        data = ['How much does {course code} cost?']
        and {course code} will be randomize to one of the course code we support

        :param data: data to parse
        :param types: list of entities to change.
        :return: None
        """
        new_data = []
        for type in types:
            sub_string = '{%s}' % type
            regex = re.compile("{}".format(sub_string), re.IGNORECASE)
            for line in data:
                samples = self.data_map[type](10)
                new_data.extend([regex.sub(sample, line) for sample in samples])
        return new_data

    def create_intent(self, display_name, training_data, message_texts, intent_type):
        parent = self.intent_client.project_agent_path(self.project_id)
        training_phrases = []

        training_data_entity = self.intent_entity_map[intent_type]
        training_phrases_parts = self.parse_data(self.read_data(training_data), training_data_entity['parse_key'])
        regex = re.compile('^COMP\d{4}', re.IGNORECASE)
        for training_phrases_part in training_phrases_parts:
            parts = []
            for word in training_phrases_part.split():
                part = dialogflow.types.Intent.TrainingPhrase.Part(
                        text=word,
                        entity_type=training_data_entity['entity_type'],
                        alias=training_data_entity['alias']) if regex.match(word) else \
                        dialogflow.types.Intent.TrainingPhrase.Part(text=word)
                space = dialogflow.types.Intent.TrainingPhrase.Part(text=' ')
                parts.extend([part, space])

            # Here we create a new training phrase for each provided part.
            training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=parts)
            training_phrases.append(training_phrase)

        text = dialogflow.types.Intent.Message.Text(text=message_texts)
        message = dialogflow.types.Intent.Message(text=text)

        intent = dialogflow.types.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=[message])

        response = self.intent_client.create_intent(parent, intent)

        print('Intent created: {}'.format(response))


if __name__ == '__main__':
    query_trainer = QueryTrainer(DIALOGFLOW_PROJECT_ID)
    query_trainer.create_intent(display_name='course_fee_queries', training_data='training_data/course_fees.txt',
                                message_texts=['course_fee_queries: $course'], intent_type='course_fee')
    # print(data)
    # query_trainer.parse_data(data, ['course code'])
