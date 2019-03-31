import os
import dialogflow_v2 as dialogflow
from uuid import uuid4
from conf.Response import IntentResponse, FallbackResponse
from conf.Logger import Logger
import re

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
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials

        self.project_id, self.session_id = project_id, session_id
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(project_id, session_id)
        logger.info('Session path: {}\n'.format(self.session))

        # the information regarding this map should match what is on DialogFlow setup
        self.intent_regex_map = {
            'course_fee_queries': [{'$course': re.compile('.*COMP\d{4}.*', re.IGNORECASE)}],
            'course_outline_queries': [{'$course': re.compile('.*COMP\d{4}.*', re.IGNORECASE)}],
            'course_location_queries': [{'$course': re.compile('.*COMP\d{4}.*', re.IGNORECASE)}],
            'indicative_hours_queries': [{'$course': re.compile('.*COMP\d{4}.*', re.IGNORECASE)}],
            'offering_term_queries': [{'$course': re.compile('.*COMP\d{4}.*', re.IGNORECASE)}],
            'prerequisites_queries': [{'$course': re.compile('.*COMP\d{4}.*', re.IGNORECASE)}],
            'school_and_faculty_queries': [{'$course': re.compile('.*COMP\d{4}.*', re.IGNORECASE)}],
            'send_outline_queries': [{'$course': re.compile('.*COMP\d{4}.*', re.IGNORECASE)}],
            'study_level_queries': [{'$course': re.compile('.*COMP\d{4}.*', re.IGNORECASE)}],
            'consultation_booking': [{'$course': re.compile('.*COMP\d{4}.*', re.IGNORECASE)},
                                     {'$date': re.compile('.*\d{4}-\d{2}-\d{2}.*')},
                                     {'$time': re.compile('.*\d{2}:\d{2}:\d{2}.*')}]
        }

        self.entity_intent_fall_backs = {
            'course_fee_queries': "My apologise, could you rephrase and tell me again tell me the course code of the course "
                                  "you would like to know the course fee for?",
            'course_outline_queries': "Sorry, I didn't quite understand that. Could you rephrase and tell me "
                                      "again which course's course outline would you like to know?",
            'course_location_queries': "My apologise, could you rephrase and tell me again which course's "
                                       "course location would you like to know?",
            'indicative_hours_queries': "Sorry, could you rephrase and tell me again and tell me the course code of the course you "
                                        "would like to know the amount of indicative hours for?",
            'offering_term_queries': "My apologise, could you please rephrase and tell me again the course code of the course you "
                                     "would like to know the offering term for?",
            'prerequisites_queries': "Sorry, could you rephrase and tell me again what is the course code of the course you "
                                     "would like to know the prerequisites for?",
            'school_and_faculty_queries': "My apologise, could you rephrase and tell me again what is the course code of the course you "
                                          "would like to know the school and faculty for?",
            'send_outline_queries': "Sorry, could you rephrase and tell me again what is the course code of the course "
                                    "you would like me to send outline for?",
            'study_level_queries': "Sorry, could you please rephrase and tell me the course code of the course "
                                   "you would like to know the study level for?",
            'consultation_booking': "Sorry, could you please rephrase your sentence and tell me what is the course code, "
                                    "time and date of the course consultation you want to book?"
        }

    def query(self, text):
        result = self.detect_intent_texts(text=text)
        logger.debug('Intent detection returned:\n\tIntent: {}\n\tFullfillment text: {}'.format(result.intent, result.message))
        if not isinstance(result, FallbackResponse):
            if self.detect_missing_parameters(result.intent, result.message) or result.confidence < 0.5:
                result = self.handle_missing_parameters(result)
        logger.debug('After checking state:\nIntent detection returned:\n\tIntent: {}\n\tFullfillment text: {}'.format(result.intent, result.message))
        return result

    def detect_intent_texts(self, text, language_code='en'):
        """Returns the result of detect intent with texts as inputs.

        Using the same `session_id` between requests allows continuation
        of the conversation.
        :param text: message
        :type str
        :param language_code: the language code of the language
        :type: str
        """
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = self.session_client.detect_intent(session=self.session, query_input=query_input)

        logger.info('Query text: {}'.format(response.query_result.query_text))
        logger.info('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        logger.info('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))

        if response.query_result.intent.display_name == 'Default Fallback Intent':
            return FallbackResponse(intent=response.query_result.intent.display_name,
                                    message=response.query_result.fulfillment_text,
                                    confidence=response.query_result.intent_detection_confidence)

        if not response.query_result.intent.display_name.endswith('with_followup'):
            query_response_message = self.clean_message(response.query_result.fulfillment_text)
        else:
            query_response_message = response.query_result.fulfillment_text

        query_response = IntentResponse(intent=response.query_result.intent.display_name,
                                        message=query_response_message,
                                        confidence=response.query_result.intent_detection_confidence)

        return query_response

    def check_relevance_to_state(self, prev, new):
        regexs = self.intent_regex_map[prev.intent]
        for regex in regexs:
            for key, val in regex.items():
                if val.match(new.message):
                    return True
        return False

    def detect_missing_parameters(self, intent, text):
        if intent not in self.intent_regex_map.keys():
            return []
        regexs = self.intent_regex_map[intent]
        missing = []
        for regex in regexs:
            for key, val in regex.items():
                if not val.match(text):
                    missing.append(key)
        return missing

    def handle_missing_parameters(self, response):
        if response.intent in self.entity_intent_fall_backs:
            return FallbackResponse(intent=response.intent,
                                    message=self.entity_intent_fall_backs[response.intent],
                                    confidence=response.confidence)
        return FallbackResponse(intent=response.intent,
                                message="Sorry, I didn't quite understand that. Could you please rephrase your question?",
                                confidence=response.confidence)

    def clean_message(self, message):
        message = message.replace("'s", '')
        translator = str.maketrans('', '', "#!?()[]{}=+`~$%&*,.'\\|><")
        message = message.translate(translator)
        return message


if __name__ == '__main__':
    query_module = QueryModule()
    query_module.query('hi')
