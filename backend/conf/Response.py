class IntentResponse:
    def __init__(self, intent, message, confidence, username=None):
        self.intent = intent
        self.message = message
        self.confidence = confidence
        self.username = username

    def set_username(self, username):
        self.username = username


class FallbackResponse:
    def __init__(self, intent, message, confidence, username=None):
        self.intent = intent
        self.message = message
        self.confidence = confidence
        self.username = username

    def set_username(self, username):
        self.username = username
