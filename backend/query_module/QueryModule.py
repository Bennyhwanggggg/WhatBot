import os
import dialogflow_v2 as dialogflow
from uuid import uuid4
from conf.Response import IntentResponse, FallbackResponse
import re

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
        print('Session path: {}\n'.format(self.session))

        self.state = []

        self.fall_backs = {
            '$course': self.course_missing_fallback
        }

        # the information regarding this map should match what is on DialogFlow setup
        self.intent_regex_map = {
            'course_fee_queries': [{'$course': re.compile('COMP\d{4}', re.IGNORECASE)}],
            'course_outline_queries': [{'$course': re.compile('COMP\d{4}', re.IGNORECASE)}],
            'course_location_queries': [{'$course': re.compile('COMP\d{4}', re.IGNORECASE)}],
            'indicative_hours_queries': [{'$course': re.compile('COMP\d{4}', re.IGNORECASE)}],
            'offering_term_queries': [{'$course': re.compile('COMP\d{4}', re.IGNORECASE)}],
            'prerequisites_queries': [{'$course': re.compile('COMP\d{4}', re.IGNORECASE)}],
            'school_and_faculty_queries': [{'$course': re.compile('COMP\d{4}', re.IGNORECASE)}],
            'send_outline_queries': [{'$course': re.compile('COMP\d{4}', re.IGNORECASE)}],
            'study_level_queries': [{'$course': re.compile('COMP\d{4}', re.IGNORECASE)}],
            'consultation_booking': [{'$course': re.compile('COMP\d{4}', re.IGNORECASE)},
                                     {'$date': re.compile('\d{1,4}\/\d{1,2}\/\d{1,4}')},
                                     {'$time': re.compile('\d{1,2}:\d{1,2}|\d(pm|am)')}]
        }

    def query(self, text):
        result = self.detect_intent_texts(text=text)
        print('Intent detection returned:\n\tIntent: {}\n\tFullfillment text: {}'.format(result.intent, result.message))
        if isinstance(result, FallbackResponse):
            self.state.append(result)
        else:
            if result.confidence < 0.6 and self.state:
                prev = self.state.pop()
                if self.check_relevance_to_state(prev, result):
                    result.intent = prev.intent
        print('After checking state:\nIntent detection returned:\n\tIntent: {}\n\tFullfillment text: {}'.format(result.intent, result.message))
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

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))

        query_response = IntentResponse(intent=response.query_result.intent.display_name,
                                        message=self.clean_message(response.query_result.fulfillment_text),
                                        confidence=response.query_result.intent_detection_confidence)

        if '$' in response.query_result.fulfillment_text:
            return self.fall_backs[response.query_result.fulfillment_text](query_response)
        else:
            missing = self.detect_missing_parameters(response.query_result.intent.display_name,
                                                     response.query_result.fulfillment_text)
            if missing:
                return self.fall_backs[missing[0]](query_response) if len(missing) == 1 else \
                        self.handle_multiple_missing()
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

    def course_missing_fallback(self, query_response):
        if query_response.intent == 'course_fee_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="Please tell me the course code of the course "
                                            "you would like to know the course fee for",
                                    confidence=query_response.confidence)
        elif query_response.intent == 'course_outline_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="Which course's course outline would you like to know?",
                                    confidence=query_response.confidence)
        elif query_response.intent == 'course_location_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="Which course's course location would you like to know?",
                                    confidence=query_response.confidence)
        elif query_response.intent == 'indicative_hours_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="Please tell me the course code of the course you would like "
                                            "to know the amount of indicative hours for",
                                    confidence=query_response.confidence)
        elif query_response.intent == 'offering_term_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="Please tell me the course code of the course you would like "
                                            "to know the offering term for",
                                    confidence=query_response.confidence)
        elif query_response.intent == 'prerequisites_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="What is the course code of the course you would like to know"
                                            "the prerequisites for",
                                    confidence=query_response.confidence)
        elif query_response.intent == 'school_and_faculty_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="What is the course code of the course you would like to know"
                                            "the school and faculty for",
                                    confidence=query_response.confidence)
        elif query_response.intent == 'send_outline_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="What is the course code of the course you would like me to send outline"
                                            "for?",
                                    confidence=query_response.confidence)
        elif query_response.intent == 'study_level_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="Could you please tell me the course you would like to know "
                                            "the study level for?",
                                    confidence=query_response.confidence)
        return FallbackResponse(intent=query_response.intent,
                                message='Sorry, I am not sure how to help you with that.',
                                confidence=query_response.confidence)

    def handle_multiple_missing(self):
        pass

    def clean_message(self, message):
        message = message.replace("'s", '')
        translator = str.maketrans('', '', "#!?()[]{}=+`~$%&*,.'\\|><")
        message = message.translate(translator)
        return message


if __name__ == '__main__':
    query_module = QueryModule()
    query_module.detect_intent_texts('hi')