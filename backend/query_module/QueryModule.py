import os
import dialogflow_v2 as dialogflow
from uuid import uuid4
from conf.Response import IntentResponse, FallbackResponse
from conf.Logger import Logger

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

    def query(self, text):
        result = self.detect_intent_texts(text=text)
        logger.debug('Intent detection returned:\n\tIntent: {}\n\tFullfillment text: {}'.format(result.intent, result.message))
        if not isinstance(result, FallbackResponse):
            if result.confidence < 0.5:
                pass  # TODO: collect log
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

        missing_parameters = self.detect_missing_parameters(response.query_result.parameters.fields)
        if len(missing_parameters):
            return FallbackResponse(intent='Missing parameters: {}'.format(response.query_result.intent.display_name),
                                    message='Sorry, I cannot understand your question. Could you please rephrase your question?'
                                            'I also need the following information to assist you more efficiently: {}'.format(' '.join(missing_parameters)),
                                    confidence=response.query_result.intent_detection_confidence)
        if response.query_result.intent.display_name == 'Default Fallback Intent':
            return FallbackResponse(intent=response.query_result.intent.display_name,
                                    message=response.query_result.fulfillment_text,
                                    confidence=response.query_result.intent_detection_confidence)

        if response.query_result.intent.display_name.endswith('with_followup') or \
           not len(response.query_result.parameters.keys()):
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

    def clean_message(self, message):
        message = message.replace("'s", '')
        translator = str.maketrans('', '', "#!?()[]{}=+`~$%&*,.'\\|><")
        message = message.translate(translator)
        return message


if __name__ == '__main__':
    query_module = QueryModule()
    res = query_module.detect_intent_texts('I want to see all courses')
    print(res.message)
