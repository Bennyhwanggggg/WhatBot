"""
    This file contains the Response objects that will be used to pass
    messages between the modules for the program to use.
"""


class IntentResponse:
    def __init__(self, intent, message, confidence, username=None):
        """Initialise the IntentResponse class which carries information on
        how Dialogflow responded to an intent and also the user who triggered it

        :param intent: intent name
        :type: str
        :param message: message returned from Dialogflow
        :type: str
        :param confidence: confidence level Dialogflow showed
        :type: float
        :param username: username of the user who triggered the intent
        :type: str
        """
        self.intent = intent
        self.message = message
        self.confidence = confidence
        self.username = username

    def set_username(self, username):
        """Setter for username
        """
        self.username = username


class FallbackResponse:
    def __init__(self, intent, message, confidence, username=None):
        """Initialise the FallbackResponse class which carries information on
        how Dialogflow responded to an intent and also the user who triggered it and
        forces to be classified as a fallback

        :param intent: intent name
        :type: str
        :param message: message returned from Dialogflow
        :type: str
        :param confidence: confidence level Dialogflow showed
        :type: float
        :param username: username of the user who triggered the intent
        :type: str
        """
        self.intent = intent
        self.message = message
        self.confidence = confidence
        self.username = username

    def set_username(self, username):
        """Setter for username
        """
        self.username = username
