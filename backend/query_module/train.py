"""
    This class is responsible for training the Dialogflow agents using the data provided
    in the training_data folder. It can train intents and entities using different
    command line arguments.
    Usage:
        To train entities and intents: python3 train.py --retrain_all
        To train just intents: python3 train.py --retrain_intents
        To train just entities: python3 train.py --retrain_entities

        If no arguments is passed in, --retrain_intents is used

    Note: If just training entities and an entity being trained is currently being used
          by another intent, Dialogflow will throw an error, so make sure you delete that
          intent first.
"""

import dialogflow_v2 as dialogflow
import os
import re
import random
import datetime

PATH = os.path.dirname(os.path.realpath(__file__))
DIALOGFLOW_PROJECT_ID = 'whatbot-v1'
GOOGLE_APPLICATION_CREDENTIALS = 'whatbot-v1-7a84dc8485c1.json'


class QueryModuleTrainer:
    def __init__(self, project_id, credentials=GOOGLE_APPLICATION_CREDENTIALS):
        """ Initialise the query module trainer that trains NLP intents on Dialogflow.
        To retrain the whole model, must retrain entities first before intents. Otherwise,
        issue with entities being used will arise.

        Following config should be updated along with more functionality
        intent_entity_map: Add more to this field when you want to support
                          more entity for an intent. E.g time, course code
        entity_map: Update when you want to detect more entity in query strings.
                    Use regex, entity_type and alias should match what is on Dialogflow


        :param project_id: id of the project
        :type str
        :param credentials: Google application credential obtained from json file from Google Developer Platform
        :type json file
        """
        # Setup environment to login to Dialogflow
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials
        self.project_id = project_id
        self.intents_client = dialogflow.IntentsClient()
        self.entity_types_client = dialogflow.EntityTypesClient()

        self.intents_parent = self.intents_client.project_agent_path(self.project_id)
        self.entity_types_parent = self.entity_types_client.project_agent_path(project_id)

        self.data_map = {
            'course code': self._get_training_course_codes,
            'time': self._set_training_time,
            'date': self._set_training_time
        }

        # the information regarding this map should match what is on DialogFlow setup
        self.intent_entity_map = {
            'course_fee': {'parse_key': ['course code']},
            'course_outline': {'parse_key': ['course code']},
            'prerequisites': {'parse_key': ['course code']},
            'school_and_faculty': {'parse_key': ['course code']},
            'study_level': {'parse_key': ['course code']},
            'offering_term': {'parse_key': ['course code']},
            'course_location': {'parse_key': ['course code']},
            'indicative_hours': {'parse_key': ['course code']},
            'send_outline': {'parse_key': ['course code']},
            'consultation_booking': {'parse_key': ['course code', 'time', 'date']}
        }

        self.entity_map = {
            'course code': {'regex': re.compile('^COMP\d{4}', re.IGNORECASE),
                            'entity_type': '@course',
                            'alias': 'course'},
            'date': {'regex': re.compile('\d{1,4}\/\d{1,2}\/\d{1,4}'),
                     'entity_type': '@sys.date',
                     'alias': 'date'},
            'time': {'regex': re.compile('\d{1,2}:\d{1,2}|\d(pm|am)'),
                     'entity_type': '@sys.time',
                     'alias': 'time'}
        }

        self.course_codes = ['COMP9900', 'comp9321', 'COMP9945', 'COMP9101', 'COMP9041', 'COMP9331', 'COMP9311',
                             'COMP9414', 'COMP9841', 'COMP6451', 'COMP9024', 'COMP9021', 'COMP9020', 'COMP9322',
                             'COMP6714', 'COMP6771', 'COMP9153', 'COMP9313', 'COMP9322', 'COmp9417', 'COMP9444',
                             'COMP9517', 'COMP9201', 'COMP9102', 'COMP9315', 'COMP4121', 'COMP9323', 'COMP9318',
                             'COMP6441', 'comp9511', 'ComP9032', 'Comp4418', 'comP6324', 'CoMp9415', 'ComP4141',
                             'COmP6752', 'ComP9153', 'comP9211', 'comP9319', 'cOMP9336', 'comP6471', 'COMP9243']

    def read_intents_data(self, data_file):
        """ Read intents data from our training data set. Data files should be configured to have
        display_name, message_texts, intent_type respectively at their own line. Otherwise,
        an error is raised.
        e.g
        display_name course_fee_queries
        message_texts course_fee_queries: $course
        intent_types course_fee

        :param data_file: file name
        :return: display_name
        :rtype: display_name: str
        :return: message_texts: responses configuration
        :rtype: message_texts: list
        :return: intent_types: the entity that the intent wil use. Should match one of the key in self.intent_entity_map
        :rtype: display_name: list
        """
        from collections import deque
        data_file = open(data_file, 'r')
        data = data_file.read().split('\n')
        data_file.close()
        display_name, message_texts, intent_types, clean_data = None, [], [], []
        if not data or not data[0]:
            print('Empty intents data file:\n{}\n'.format(data_file))
            return None, [], [], []
        data = deque(data)
        while data:
            line = data.popleft()
            if line.startswith('display_name'):
                display_name = ' '.join(line.split()[1:])
            elif line.startswith('message_texts'):
                message_texts.append(' '.join(line.split()[1:]))
            elif line.startswith('intent_type'):
                intent_types.append(' '.join(line.split()[1:]))
            else:
                clean_data.append(line)
        if not clean_data or not display_name or not message_texts or not intent_types:
            print('Error in intents data file configuration: {}'.format(data_file))
            return None, [], [], []
        return display_name, message_texts, intent_types, clean_data

    def _get_training_course_codes(self, size):
        return [random.choice(self.course_codes) for _ in range(size)]

    def _set_training_time(self, size):
        def random_date(start, l):
            current = start
            for i in range(l):
                curr = current + datetime.timedelta(days=random.randrange(200),
                                                    hours=random.randrange(24),
                                                    minutes=random.randrange(60))
                yield curr
        return [x.strftime("%d/%m/%y %H:%M") for x in random_date(datetime.datetime.now(), size)]

    def parse_data(self, data, types):
        """ Randomize the data with different entity types. Like changing the course
        codes for the training data. It will randomize the contents inside the training
        data themselves.

        E.g
        types = [course code]
        data = ['How much does {course code} cost?']
        and {course code} will be randomize to one of the course code we support

        :param data: data to parse
        :type: list
        :param types: entities to change.
        :type: list
        :return: new_data
        :rtype: list
        """
        size = 15//len(types) + 1
        for type in types:
            sub_string = '{%s}' % type
            regex = re.compile("{}".format(sub_string), re.IGNORECASE)
            new_data = []
            for line in data:
                samples = self.data_map[type](size)
                new_data.extend([regex.sub(sample, line) for sample in samples])
            data = new_data
        return data

    def create_intent(self, display_name, training_data, message_texts, intent_types, data_is_parsed=False):
        """ Method for creating an intent. However, if the display_name already exist
        in dialogflow, it will be run into an error

        :param display_name: name you want the intent to be called
        :type: str
        :param training_data: file that contains all the training data or the data itself with each lines in a list
        :type: str if data_is_parsed=False or list if data_is_parsed=True
        :param message_texts: response you want the intent to use
        :type: list
        :param intent_types: type of intent. e.g course_fee, course_outline
        :type: list
        :param data_is_parsed: whether if the data file provided has already been read or not
        :type: bool
        :return: None
        """
        training_phrases = []
        if not data_is_parsed:
            _, _, _, training_data = self.read_intents_data(training_data)
            if not training_data:
                print('No training data provided')
                return
        training_data_entities = [self.intent_entity_map[intent_type] for intent_type in intent_types]

        # Get the list of entity parse keys
        training_data_entities_parse_keys = []
        for training_data_entity in training_data_entities:
            training_data_entities_parse_keys.extend(training_data_entity['parse_key'])
        training_data_entities_parse_keys = list(set(training_data_entities_parse_keys))

        # parse the data with the entites
        training_phrases_parts = self.parse_data(training_data, training_data_entities_parse_keys)

        # Process training phrases
        for training_phrases_part in training_phrases_parts:
            parts = []
            for word in training_phrases_part.split():
                is_entity, part = False, None
                for training_data_entities_parse_key in training_data_entities_parse_keys:
                    entity = self.entity_map[training_data_entities_parse_key]
                    regex, entity_type, alias = entity['regex'], entity['entity_type'], entity['alias']
                    if regex.match(word):
                        part = dialogflow.types.Intent.TrainingPhrase.Part(text=word, entity_type=entity_type, alias=alias)
                        is_entity = True
                        break
                # classify each word in a phrase
                if not is_entity:
                    part = dialogflow.types.Intent.TrainingPhrase.Part(text=word)
                space = dialogflow.types.Intent.TrainingPhrase.Part(text=' ')
                parts.extend([part, space])

            # Create a new training phrase for each provided part.
            training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=parts)
            training_phrases.append(training_phrase)

        text = dialogflow.types.Intent.Message.Text(text=message_texts)
        message = dialogflow.types.Intent.Message(text=text)

        intent = dialogflow.types.Intent(display_name=display_name, training_phrases=training_phrases, messages=[message])

        response = self.intents_client.create_intent(self.intents_parent, intent)
        print('Intent created: {}'.format(response))

    def _get_intent_ids(self, display_name):
        """ Helper to get an id of an intent using display name

        :param display_name: name of the intent
        :return: id of the intent in a list
        """
        intents = self.intents_client.list_intents(self.intents_parent)
        intent_names = [intent.name for intent in intents if intent.display_name == display_name]
        # This gets the intent_ids
        return [intent_name.split('/')[-1] for intent_name in intent_names] if intent_names else []

    def delete_intent(self, display_name):
        """ Delete an intent using display name

        :param display_name: name of the intent
        :return: None
        """
        intent_ids = self._get_intent_ids(display_name)
        for intent_id in intent_ids:
            intent_path = self.intents_client.intent_path(self.project_id, intent_id)
            self.intents_client.delete_intent(intent_path)

    def delete_all_intents(self):
        """ Delete all intents. Used to reset so entities can be retrained.

        :return: None
        """
        intents = self.intents_client.list_intents(self.intents_parent)
        intent_names = [intent.name for intent in intents]
        intent_ids = [intent_name.split('/')[-1] for intent_name in intent_names]
        for intent_id in intent_ids:
            intent_path = self.intents_client.intent_path(self.project_id, intent_id)
            self.intents_client.delete_intent(intent_path)

    def retrain_intents(self, training_data_folder='training_data/intents/'):
        """ Retrains every model using the training data provided.
        Will delete existing intent if name overlaps

        :param training_data_folder: folder to read training data from
        :return: None
        """
        training_data_folder = os.path.join(PATH, training_data_folder)
        for training_data_file in os.listdir(training_data_folder):
            path_to_read = os.path.join(training_data_folder, training_data_file)
            display_name, message_texts, intent_types, data = self.read_intents_data(path_to_read)
            if not data:
                continue
            try:
                if self._get_intent_ids(display_name):
                    self.delete_intent(display_name)
                self.create_intent(display_name, data, message_texts, intent_types, data_is_parsed=True)
            except Exception as e:
                print(str(e))

    def read_entities_data(self, data_file):
        from collections import deque
        data_file = open(data_file, 'r')
        data = data_file.read().split('\n')
        data_file.close()
        if not data or not data[0]:
            print('Empty entity data file: {}'.format(data_file))
            return None, [], []
        data = deque(data)
        entity_values, synonyms = [], []
        # first line must be entity display_name
        display_name = data.popleft()
        while data:
            line = data.popleft().split('@@@')
            if len(line):
                entity_values.append(line[0])
                if len(line) > 1:
                    # synomoys should be separated by $$$
                    all_synonyms = line[1].split('$$$')
                    synonyms.append(all_synonyms)
        if not entity_values:
            print('Empty entity data file configuration: {}'.format(data_file))
            return None, [], []
        return display_name, entity_values, synonyms

    def create_entity(self, display_name, entity_values, synonyms=[]):
        """ Create an entity. However, if the entity itself is currently being used, an
        error will occur. In this case, you need to delete/disable the intent that is using
        that entity before retrying.

        :param display_name: name of entity
        :type str
        :param entity_values: list of values for the entity
        :type list
        :param synonyms: list of synomym for the entity values. This must be same length as entity_values if used
        :type list
        :return: None
        """
        entity_type = dialogflow.types.EntityType(display_name=display_name, kind='KIND_MAP', auto_expansion_mode=True)
        response = self.entity_types_client.create_entity_type(self.entity_types_parent, entity_type)
        print('Entity type created: \n{}'.format(response))
        entity_type_ids = self._get_entity_ids(display_name)
        for entity_type_id in entity_type_ids:
            entity_type_path = self.entity_types_client.entity_type_path(self.project_id, entity_type_id)

            training_entities = []
            synonyms = synonyms or entity_values
            for entity_value, synonym in zip(entity_values, synonyms):
                entity = dialogflow.types.EntityType.Entity()
                entity.value = entity_value
                for syn in synonym:
                    entity.synonyms.append(syn)
                training_entities.append(entity)
            response = self.entity_types_client.batch_create_entities(entity_type_path, training_entities)
            print('Entity created: {}'.format(response))

    def _get_entity_ids(self, display_name):
        """ Helper to get an id of an entity using display name

        :param display_name: name of the intent
        :return: id of the entity in a list
        """
        entities = self.entity_types_client.list_entity_types(self.entity_types_parent)
        entity_names = [entity.name for entity in entities if entity.display_name == display_name]
        return [entity_name.split('/')[-1] for entity_name in entity_names] if entity_names else []

    def delete_entity(self, display_name):
        """ Delete an entity using display_name. However, will not work if entity is
        currently being used by another intent. In this case, you need to delete that
        intent first.

        :param display_name: name of entity to delete
        :return: None
        """
        entity_type_ids = self._get_entity_ids(display_name)
        for entity_type_id in entity_type_ids:
            entity_type_path = self.entity_types_client.entity_type_path(self.project_id, entity_type_id)
            self.entity_types_client.delete_entity_type(entity_type_path)

    def retrain_entities(self, training_data_folder='training_data/entities'):
        """ Retrains every model using the training data provided.
        Will delete existing intent if name overlaps

        :param training_data_folder: folder to read training data from
        :return: None
        """
        training_data_folder = os.path.join(PATH, training_data_folder)
        for training_data_file in os.listdir(training_data_folder):
            path_to_read = os.path.join(training_data_folder, training_data_file)
            display_name, entity_values, synonyms = self.read_entities_data(path_to_read)
            if not entity_values:
                continue
            try:
                if self._get_entity_ids(display_name):
                    self.delete_entity(display_name)
                self.create_entity(display_name, entity_values, synonyms)
            except Exception as e:
                print(str(e))


if __name__ == '__main__':
    query_module_trainer = QueryModuleTrainer(DIALOGFLOW_PROJECT_ID)

    # Argument parser setup
    import argparse
    parser = argparse.ArgumentParser(description="Dialogflow Agent Trainer")
    parser.add_argument("--retrain_all", default=False,
                        help="Retrain Dialogflow agent completely by retraining the entities first then the intents")

    parser.add_argument("--retrain_intents", default=False,
                        help="Retrain all of Dialogflow agent's intents")

    parser.add_argument("--retrain_entities", default=False,
                        help="Retrain all of Dialogflow agent's entties")

    args = parser.parse_args()

    if args.retrain_all:
        query_module_trainer.delete_all_intents()
        query_module_trainer.retrain_entities()
        query_module_trainer.retrain_intents()
    elif args.retrain_intents:
        query_module_trainer.retrain_intents()
    elif args.retrain_entities:
        query_module_trainer.retrain_entities()
    else:
        # For development use
        display_name, message_texts, intent_types, data = query_module_trainer.read_intents_data('./training_data/intents/consultation_booking_commands.txt')
        query_module_trainer.create_intent(display_name=display_name, message_texts=message_texts, intent_types=intent_types, training_data=data, data_is_parsed=True)
