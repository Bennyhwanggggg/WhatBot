import os
import dialogflow_v2 as dialogflow
from uuid import uuid4
from conf.Response import IntentResponse, FallbackResponse


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

        self.fall_backs = {
            '$course': self.course_missing_fallback
        }

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
                                        message=self.clean_message(response.query_result.fulfillment_text))

        if '$' not in response.query_result.fulfillment_text:
            return query_response

        else:
            return self.fall_backs[response.query_result.fulfillment_text](query_response)

    def course_missing_fallback(self, query_response):
        if query_response.intent == 'course_fee_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="Please tell me the course code of the course "
                                            "you would like to know the course fee for")
        elif query_response.intent == 'course_outline_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="Which course's course outline would you like to know?")
        elif query_response.intent == 'course_location_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="Which course's course location would you like to know?")
        elif query_response.intent == 'indicative_hours_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="Please tell me the course code of the course you would like "
                                            "to know the amount of indicative hours for")
        elif query_response.intent == 'offering_term_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="Please tell me the course code of the course you would like "
                                            "to know the offering term for")
        elif query_response.intent == 'prerequisites_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="What is the course code of the course you would like to know"
                                            "the prerequisites for")
        elif query_response.intent == 'school_and_faculty_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="What is the course code of the course you would like to know"
                                            "the school and faculty for")
        elif query_response.intent == 'send_outline_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="What is the course code of the course you would like me to send outline"
                                            "for?")
        elif query_response.intent == 'study_level_queries':
            return FallbackResponse(intent=query_response.intent,
                                    message="Could you please tell me the course you would like to know "
                                            "the study level for?")
        return FallbackResponse(intent=query_response.intent,
                                message='Sorry, I am not sure how to helpe you with that.')

    def clean_message(self, message):
        message = message.replace("'s", '')
        translator = str.maketrans('', '', "#!?()[]{}=+`~$%&*,.'\\|><")
        message = message.translate(translator)
        return message


if __name__ == '__main__':
    query_module = QueryModule()
    query_module.detect_intent_texts('hi')