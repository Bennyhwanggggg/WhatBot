import dialogflow_v2 as dialogflow
from uuid import uuid4
import os

DIALOGFLOW_PROJECT_ID = 'whatbot-v1'
GOOGLE_APPLICATION_CREDENTIALS = 'whatbot-v1-7a84dc8485c1.json'


class QueryModule():
    def __init__(self, project_id=DIALOGFLOW_PROJECT_ID, session_id=uuid4(), credentials=GOOGLE_APPLICATION_CREDENTIALS):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials

        self.project_id, self.session_id = project_id, session_id
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(project_id, session_id)
        print('Session path: {}\n'.format(self.session))
        print(vars(self.session_client)['_method_configs'])
        print(self.session_client.__dir__)

    def detect_intent_texts(self, texts, language_code='en'):
        """Returns the result of detect intent with texts as inputs.

        Using the same `session_id` between requests allows continuation
        of the conversation."""

        for text in texts:
            text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)

            query_input = dialogflow.types.QueryInput(text=text_input)

            response = self.session_client.detect_intent(
                session=self.session, query_input=query_input)

            print('=' * 20)
            print(response)
            print('Query text: {}'.format(response.query_result.query_text))
            print('Detected intent: {} (confidence: {})\n'.format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence))
            print('Fulfillment text: {}\n'.format(
                response.query_result.fulfillment_text))

            return response.query_result.fulfillment_text




if __name__ == '__main__':
    query_module = QueryModule()
    query_module.detect_intent_texts(['Can I have the outline for COMP9900?'])