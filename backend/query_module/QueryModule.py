"""
    This file contains the main QueryModule which handles user inputs from outside
    and passes it to Dialogflow for intent detection. It then analyse the result from
    Dialogflow and do processing (e.g if wrong entity detected) if required before passing the
    result to SearchModule.
"""
import os
import dialogflow_v2 as dialogflow
import re
import random
from uuid import uuid4
from conf.Response import IntentResponse, FallbackResponse
from conf.Logger import Logger
from dateutil.parser import parse

"""
    Logger setup
"""
logger = Logger(__name__).log

PATH = os.path.dirname(os.path.realpath(__file__))
DIALOGFLOW_PROJECT_ID = 'whatbot-v1'
GOOGLE_APPLICATION_CREDENTIALS = 'whatbot-v1-7a84dc8485c1.json'
GOOGLE_APPLICATION_CREDENTIALS_PATH = os.path.join(PATH, GOOGLE_APPLICATION_CREDENTIALS)


class QueryModule:
    def __init__(self, project_id=DIALOGFLOW_PROJECT_ID,
                 session_id=uuid4(),
                 credentials=GOOGLE_APPLICATION_CREDENTIALS_PATH):
        """Initialise the QueryModule with the given credentials from Google to
        connect to our AI agent on Dialogflow.

        :param project_id: project ID from Google Developer console
        :type: str
        :param session_id: session we want to create
        :type: uuid4
        :param credentials: file with all the API key given from Google
        :type: os.path
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials

        self.project_id, self.session_id = project_id, session_id
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(project_id, session_id)
        logger.info('Session path: {}\n'.format(self.session))

        """
            Mappings setup which is used for data cleansing.
        """
        self.entity_map = {
            'course code': {'regex': re.compile(r'.*COMP\d{4}.*', re.IGNORECASE),
                            'capture': re.compile(r'.*(COMP\d{4}).*', re.IGNORECASE)},
            'time': {'regex': re.compile(r'.*\d{1,2}:\d{1,2}.*|.*\d+(pm|am).*', re.IGNORECASE),
                     'capture': re.compile(r'(\d{1,2}:\d{1,2}.*|\d+(pm|am))', re.IGNORECASE)},
            'date': {'regex': re.compile(r'.*\d{1,4}\/\d{1,2}\/\d{1,4}.*'),
                     'capture': re.compile(r'(\d{1,4}\/\d{1,2}\/\d{1,4})')},
            'student': {'regex': re.compile(r'z\d{7}', re.IGNORECASE),
                        'capture': re.compile(r'(z\d{7})', re.IGNORECASE)}
        }

        self.low_confidence_fallbacks = [
            'Sorry, I could not understand your question, can you please rephrase that?',
            'My apologies, I am not quite sure what you are asking, could you please say that again?',
            'I am not sure if I understood your question correctly, can you please rephrase your question?'
        ]

    def query(self, text):
        """Use the provided input and send it to Dialogflow and then process the result.
        If the result is not a fallback and Dialogflow is not confident. We force it into
        a fallback since low confidence result from Dialogflow is ususally not accurate.

        :param text: user input
        :return: response data from Dialogflow
        :rtype: IntentResponse or FallbackReponse from conf
        """
        result = self.detect_intent_texts(text=text)
        logger.debug('Intent detection returned:\n\tIntent: {}\n\tFullfillment text: {}'.format(result.intent, result.message))
        if not isinstance(result, FallbackResponse):
            # force fallback if low confidence
            if result.confidence < 0.5:
                result = FallbackResponse(intent=result.intent,
                                          message=random.choice(self.low_confidence_fallbacks),
                                          confidence=result.confidence,
                                          username=result.username)
        logger.debug('After checking state:\nIntent detection returned:\n\tIntent: {}\n\tFullfillment text: {}'.format(result.intent, result.message))
        return result

    def detect_intent_texts(self, text, language_code='en'):
        """Call the Dialogflow API with the given text. Returns the result of detect intent
        with texts as inputs. Also detect if parameters are missing from Dialogflow's result
        and do our own entity extraction if there is missing parameter. Finally, clean response
        message by removing unnecessary punctuations.

        If a fallback is received or missing parmeter is detected, we force into a
        FallbackResponse type.

        Using the same `session_id` between requests allows continuation
        of the conversation.
        :param text: message
        :type str
        :param language_code: the language code of the language
        :type: str
        :return: response from Dialogflow
        :rtype: IntentResponse or FallbackResponse
        """
        # convert text into Dialogflow Text and Query type
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        # call Dialogflow API
        response = self.session_client.detect_intent(session=self.session, query_input=query_input)

        logger.info('Query text: {}'.format(response.query_result.query_text))
        logger.info('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        logger.info('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))

        # Check if missing parameters in response
        missing_parameters = self.detect_missing_parameters(response.query_result.parameters.fields)
        if len(missing_parameters):
            # Perform entity detection ourselves to see if we can make up for Dialogflow's failure
            response.query_result.fulfillment_text = self.detect_entity(text)
            if not response.query_result.fulfillment_text:
                return FallbackResponse(intent='Missing parameters: {}'.format(response.query_result.intent.display_name),
                                        message='Sorry, I cannot understand your question. Could you please rephrase your question? '
                                                'I also need the following information to assist you more efficiently: {}'.format(' '.join(missing_parameters)),
                                        confidence=response.query_result.intent_detection_confidence)
        if response.query_result.intent.display_name == 'Default Fallback Intent':
            return FallbackResponse(intent=response.query_result.intent.display_name,
                                    message=response.query_result.fulfillment_text,
                                    confidence=response.query_result.intent_detection_confidence)

        logger.debug(response.query_result)
        if response.query_result.intent.display_name.endswith('with_followup'):
            query_response_message = response.query_result.fulfillment_text
        else:
            query_response_message = self.clean_message(response.query_result.fulfillment_text)

        query_response = IntentResponse(intent=response.query_result.intent.display_name,
                                        message=query_response_message,
                                        confidence=response.query_result.intent_detection_confidence)

        return query_response

    def detect_missing_parameters(self, parameters):
        """Receives a dict from Dialogflow's response.query_result.parameter.fields
        and check if the list values are empty for anyone of them and return the missing
        fields

        :param parameters: Dialogflow response of query result parameter fields
        :type: response.query_result.parameter.fields
        :return: list of missing paramters
        :rtype: list
        """
        result = []
        for entity in parameters.keys():
            if not len(parameters[entity].list_value.values):
                result.append(entity)
        logger.debug(result)
        return result

    def detect_entity(self, text):
        """Receives a query string and find if the missing parameter is missed due to
        Dialogflow failing to detect it or it is really missing. If it is really missing
        return the missing parameters

        :param text: query text
        :type: str
        :return: missing parameters
        :rtype: str
        """
        result = []
        for entity in self.entity_map.keys():
            matches = self.entity_map[entity]['capture'].search(text)
            if matches:
                # we only use the first match as we only expect one entity
                match_result = self.convert_to_24_hours(matches.group(1)) if entity == 'time' else matches.group(1)
                match_result = self.convert_date_format(match_result) if entity == 'date' else match_result
                logger.debug('Found entity {} in {}: {}'.format(entity, text, match_result))
                result.append(match_result)
        return ' @@@ '.join(result)

    def clean_message(self, message):
        """Given a string, remove unnecessary punctuations from it and also remove noise words
        from it.

        :param message: message to clean
        :type: str
        :return: cleaned message
        :rtype: str
        """
        logger.debug(message)
        if not any([self.entity_map[entity]['regex'].search(message) for entity in self.entity_map.keys()]):
            return message
        message = message.replace("'s", '')
        translator = str.maketrans('', '', "#!?()[]{}=+`~$%&*,.'\\|><")
        message = message.translate(translator)
        message_words = message.split()
        noise_words = ['the', 'for', 'is']
        message = [word for word in message_words if word.lower() not in noise_words]
        message = ' '.join(message)
        logger.debug(message)
        return message

    def convert_date_format(self, date):
        """Convert all date strings from any format to YY-MM-DD

        :param date: date string to convert
        :type: str
        :return: date string in YY-MM-DD format
        :type: str
        """
        try:
            result = parse(date, dayfirst=True)
        except ValueError as e:
            logger.error(e)
            return date
        result = result.strftime('%Y-%m-%d')
        return result

    def convert_to_24_hours(self, time):
        """Convert a 12 hour in am or pm format into 24 hour string

        :param time: 12 hour time string
        :type: str
        :return: 24 hour time string
        :rtype: str
        """
        if not re.search(r'(am|pm)', time, re.IGNORECASE):
            logger.error('not time string')
            return time
        t = time.strip()
        time_parts = re.split(r'(am|pm)', t, re.IGNORECASE)
        if len(time_parts) < 2:
            logger.error('Time is of invalid format: {}'.format(time))
            return time
        t, state = time_parts[:2]
        t, state = t.strip(), state.strip()
        # case when user have semicolon in time. e.g 3:15am
        if ':' not in t:
            hr, min = int(t), 0
        else:
            hr, min = list(map(int, t.split(':')))
        if state.upper() == 'AM':
            return '{:02d}:{:02d}:{:02d}'.format(hr, min, 0)
        elif state.upper == 'PM':
            hr += 12
            if hr == 24:
                hr = 0
            return '{:02d}:{:02d}:{:02d}'.format(hr, min, 0)
        else:
            return time
